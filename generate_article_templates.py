import os

import mistune


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
        html = mistune.html(md_file.read())
        html_file.write(html) # type: ignore
                              # `mistune.html` should only return a str type, but Pylance adds an extra type for List[Dict[str, Any]]


iterate_files_in_subdir('articles')
