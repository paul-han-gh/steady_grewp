import os

import mistune


class TailwindRenderer(mistune.HTMLRenderer):
    def heading(self, text: str, level: int, **attrs):
        classes = ['font-bold']

        if level == 1:
            classes += ['text-4xl', 'my-6', 'text-center', 'text-balance']
        elif level == 2:
            classes += ['text-3xl', 'my-5']
        elif level == 3:
            classes += ['text-2xl', 'my-4']
        elif level == 4:
            classes += ['text-xl', 'my-3']
        elif level == 5:
            classes += ['text-lg', 'my-2']
        else:  # level 6 and any others
            classes += ['text-base', 'my-2']

        class_str = ' '.join(classes)
        return f'<h{level} class="{class_str}">{text}<h{level}>\n'


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
        markdown = mistune.create_markdown(renderer=TailwindRenderer())
        html = markdown(md_file.read())
        html_file.write(html) # type: ignore
                              # `mistune.html` should only return a str type, but Pylance adds an extra type for List[Dict[str, Any]]


iterate_files_in_subdir('articles')
