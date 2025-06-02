import os
import re

from typing import Any
from collections.abc import Iterable

import mistune
from mistune.directives import RSTDirective, TableOfContents


class TailwindRenderer(mistune.HTMLRenderer):
    def heading(self, text: str, level: int, **attrs) -> str:
        margin_bottom = max(3, 6 - level)
        margin_top = 2 * margin_bottom
        classes = (
            [
                'font-bold',
                'font-sans',
                f'mt-{margin_top}',
                f'mb-{margin_bottom}'
            ]
            if level > 1
            else [
                'font-bold', 'font-sans'
            ]
        )

        if level == 1:
            classes += ['text-4xl', 'text-center', 'text-balance', 'my-10']
        elif level == 2:
            classes += ['text-3xl']
        elif level == 3:
            classes += ['text-2xl']
        elif level == 4:
            classes += ['text-xl']
        elif level == 5:
            classes += ['text-lg']
        else:  # level 6 and any others
            classes += ['text-base']

        class_str = ' '.join(classes)
        return f'<h{level} class="{class_str}">{text}<h{level}>'
    
    def paragraph(self, text: str) -> str:
        class_str = 'font-sans tracking-tight text-slate-900 mb-2'
        return f'<p class="{class_str}">{text}</p>'
    
    def block_quote(self, text: str) -> str:
        class_str = 'border-l-4 pl-4'
        return f'<blockquote class="{class_str}">{text}</blockquote>'


def render_toc_ul(toc: Iterable[tuple[int, str, str]]) -> str:
    if not toc:
        return ""

    s = ""
    levels = []
    for level, heading_id, text in toc:
        item = (
            (
                '<p class="line-clamp-2 mb-2">'
                if level == 2
                else f'<p class="line-clamp-2 mb-2 pl-{(level-2)*3}">'
            )
            + f'<a href="#{heading_id}"'
            + 'class="text-slate-900 font-light text-sm/5">'
            + f'{text}</a></p>'
        )
        if not levels:
            s += '<li>' + item
            levels.append(level)
        elif level == levels[-1]:
            s += '</li><li>' + item
        elif level > levels[-1]:
            s += '<ul><li>' + item
            levels.append(level)
        else:
            levels.pop()
            while levels:
                last_level = levels.pop()
                if level == last_level:
                    s += '</li></ul></li><li>' + item
                    levels.append(level)
                    break
                elif level > last_level:
                    s += '</li><li>' + item
                    levels.append(last_level)
                    levels.append(level)
                    break
                else:
                    s += '</li></ul>'
            else:
                levels.append(level)
                s += "</li>\n<li>" + item

    while len(levels) > 1:
        s += "</li></ul>"
        levels.pop()

    if not s:
        return ""
    return "<ul>\n" + s + "</li></ul>"


def render_html_toc(renderer, title: str, collapse: bool = False, **attrs: Any) -> str:
    if not title:
        title = "Table of Contents"
    content = render_toc_ul(attrs["toc"])

    html = (
        '<p class="font-bold text-lg text-slate-900 mb-2 truncate">'
        f'{title}'
        "</p>"
        f'{content}'
    )
    return f'{html}::truncate_point"'


class CustomTOC(TableOfContents):
    def generate_heading_id(self, token: dict[str, Any], index: int) -> str:
        heading_text = str(token.get('text'))
        heading_text_normalized = re.sub(
            r'[^a-z0-9]+',
            '-',
            heading_text.lower()
        ).strip('-')
        return heading_text_normalized
    
    def __call__(self, directive, md) -> None:
        if md.renderer and md.renderer.NAME == "html":
            # only works with HTML renderer
            directive.register("toc", self.parse)
            md.before_render_hooks.append(self.toc_hook)
            md.renderer.register("toc", render_html_toc)


def iterate_files_in_subdir(subdir_path):
    """
    Iterates through all files in a specified subdirectory using the os module.

    Args:
        subdirectory_path (str): The path to the subdirectory.
    """
    try:
        for item_name in os.listdir(subdir_path):
            item_path = os.path.join(subdir_path, item_name)
            if os.path.isfile(item_path):
                convert_md_to_html(item_path)
                print(f"Converted file: {item_path}")
    except FileNotFoundError:
        print(f"Error: Subdirectory '{subdir_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def convert_md_to_html(md_file_path: str) -> None:
    filename_without_ext = md_file_path[
        md_file_path.rfind('\\') : -3                   
    ]
    with (
        open(md_file_path, 'r') as md_file,
        open(f'templates/{filename_without_ext}.html', 'w') as html_file
    ):
        markdown = mistune.create_markdown(
            renderer=TailwindRenderer(),
            plugins=[RSTDirective([CustomTOC(min_level=2, max_level=4)])] # type: ignore
        )
        md_lines = md_file.readlines()
        html = ''
        html += str(markdown(md_lines[0]))
        html += (
            '<section class="flex">'
            '<div class="w-2/10">'
            '<nav class="sticky top-50">'
        )
        html += str(markdown('\n'.join(md_lines[1:])))
        truncate_point = html.find('::truncate_point')
        html = html[:truncate_point]
        html += (
            '</nav>'
            '</div>'
            '<div class="w-8/10 pl-5">'
        )
        html += str(markdown('\n'.join(md_lines[2:])))
        html += '</div></section>'
        html_file.write(html)


iterate_files_in_subdir('articles')
