import os


def get_current_working_directory():
    return os.getcwd()


def change_current_working_directory(new_dir):
    return os.chdir(new_dir)
