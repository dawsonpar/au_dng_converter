# copy files from one directory to another while keeping metadata

import os
import shutil
import time

script_directory = os.path.dirname(os.path.abspath(__file__))
extensions_to_search = [".cr3", ".cr2", ".arw", ".nef"]

dropbox_folder = "/Users/dawsonpar/Desktop/temp"
raw_folder = "/Users/dawsonpar/Desktop/coding/AU/dng-script/raws"


def get_from_dropbox(directory_path):
    """
    Recursively searches for raw photos inside dropbox folder and its subdirectories
    Ignores files that start with '._'
    Args:
        directory_path : String of path to dropbox folder
    Returns:
        raw_photo_paths : Set with paths to raw photos
    """

    raw_photo_paths = set()

    for root, _, files in os.walk(directory_path):
        for filename in files:
            if not filename.startswith("._") and any(
                filename.endswith(ext) for ext in extensions_to_search
            ):
                file_path = os.path.join(root, filename)

                print(file_path)
                raw_photo_paths.add(file_path)

    return raw_photo_paths


def copy_file(src, dest):
    """
    Copies file from src to dest
    Args:
        src : path to source file
        dest : path to destination file
    """
    try:
        shutil.copy2(src, dest)
        print("File copied successfully.")
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)


def main():
    print("Running copy.py")

    paths = get_from_dropbox(dropbox_folder)
    for path in paths:
        # If file doesn't exist in dest, copy it

        dest_path = os.path.join(raw_folder, path.split("/")[-1])

        if not os.path.exists(dest_path):
            print(f"Copying {path} to {raw_folder}")
            copy_file(path, raw_folder)
            time.sleep(1)
        else:
            print(
                f"Skipping {path.split('/')[-1]} as it already exists in {raw_folder.split('/')[-1]}"
            )


if __name__ == "__main__":
    main()
