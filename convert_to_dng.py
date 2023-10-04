"""
Search for all raw files in raw folder and convert to dng
If dng already exists, skip
"""

import os
import shutil
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

extensions_to_search = [".cr3", ".cr2", ".arw", ".nef"]
raws_folder_path = "/Users/dawsonpar/Desktop/coding/AU/dng-script/raws"
new_dng_event = threading.Event()


class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"New file created: {event.src_path.split('/')[-1]}")
        new_dng_event.set()


def get_raws(directory_path):
    """
    Recursively searches for raw photos inside folder and its subdirectories
    Checks if corresponding .dng file exists
    Ignores files that start with '._'
    Returns:
        raw_photo_paths : set with paths to raw photos
    """

    raw_photo_paths = set()

    for root, _, files in os.walk(directory_path):
        for filename in files:
            if not filename.startswith("._") and any(
                filename.endswith(ext) for ext in extensions_to_search
            ):
                file_path = os.path.join(root, filename)

                # Check if the corresponding .dng file exists
                dng_filename = os.path.splitext(filename)[0] + ".dng"
                dng_path = os.path.join(raws_folder_path, dng_filename)

                if not os.path.exists(dng_path):
                    print(file_path.split("/")[-1])
                    raw_photo_paths.add(file_path)
                else:
                    print(
                        f"Skipping {file_path.split('/')[-1]} as it's already been converted."
                    )

    return raw_photo_paths


def convert_to_dng(source_path):
    """
    Opens DNG Converter and converts raw to dng
    -c : Output compressed DNG files
    Args:
        source_path : String of path to photos
    """

    open_dng = "open -a /Applications/Adobe\ DNG\ Converter.app --args"
    dng_args = "-c"

    os.system(open_dng + " " + dng_args + " " + source_path)


def main():
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=raws_folder_path, recursive=False)
    observer.start()

    try:
        dng_counter = 0

        # print("Running convert_to_dng.py")
        raw_paths = get_raws(raws_folder_path)
        number_of_raws = len(raw_paths)

        for raw in raw_paths:
            convert_to_dng(raw)

            # Wait for new file to be created
            new_dng_event.wait()

            # Reset event
            new_dng_event.clear()
            dng_counter += 1

            if dng_counter == number_of_raws:
                print("Finished converting all raws")
                observer.stop()
                observer.join()

            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
