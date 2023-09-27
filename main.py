import copy
import os
import shutil
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import convert_to_dng

script_directory = os.path.dirname(os.path.abspath(__file__))
extensions_to_search = [".cr3", ".cr2", ".arw", ".nef"]

dropbox_folder = "dropbox"
converted_folder = "converted"
raw_folder = "raws"

subdirectory_path = os.path.join(script_directory, dropbox_folder)


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path

        if any(file_path.endswith(ext) for ext in extensions_to_search):
            time.sleep(2)
            print(f"New file detected: {file_path}")

            photo_paths = get_from_dropbox(subdirectory_path)

            for path in photo_paths:
                time.sleep(2)
                convert_to_dng(path)

            """
            if len(photo_paths) != 0:
                print("Preparing to move dng files.")
                time.sleep(5)

                # move dngs to converted folder
                move_photos()

                # move raws to raws folder
                move_photos(dng=False)
            else:
                # move any remaingin raws to raws folder
                move_photos(dng=False)
            """


def main():
    try:
        copy.main()
    except Exception as e:
        print(e)

    time.sleep(5)
    try:
        convert_to_dng.main()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
