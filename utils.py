
import os


def ensure_dir(filepath):
    """ Ensure a given directory exists by creating it if it doesn't. """

    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)


def cleanup_filename(filename):
    return filename.replace('.csv', '').replace('datasets/', '')
