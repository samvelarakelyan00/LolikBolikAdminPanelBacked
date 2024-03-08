import os


def get_main_dir(current, main_dir):
    parent = ' ' * 3

    while parent[-3:] != main_dir:
        if parent == '/':
            return f"./{main_dir}/"
        parent = os.path.dirname(current)
        current = parent

    return parent
