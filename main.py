import os
import shutil
import time


def get_from_dropbox():
    """
    Looks for dropbox folder inside of current directory
    Finds raw photos inside dropbox folder
    Checks if dng conversion already exists
    Returns:
        raw_photo_paths : set with paths to raw photos
    """

    # Get the current directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))

    dropbox_folder = "dropbox"
    converted_folder = "converted"

    subdirectory_path = os.path.join(script_directory, dropbox_folder)
    converted_directory_path = os.path.join(script_directory, converted_folder)

    raw_photo_paths = set()

    # Check if the subdirectory exists
    if os.path.exists(subdirectory_path) and os.path.isdir(subdirectory_path):
        extensions_to_search = [".cr3", ".cr2", ".arw", ".nef"]
        matching_files = [
            filename
            for filename in os.listdir(subdirectory_path)
            if any(filename.endswith(ext) for ext in extensions_to_search)
        ]

        if matching_files:
            print(
                f"Found {len(matching_files)} files with the specified extensions in the '{dropbox_folder}' directory:"
            )
            for matching_file in matching_files:
                raw_photo_path = os.path.join(subdirectory_path, matching_file)

                # Check if the corresponding .dng file exists in the "converted" directory
                dng_filename = os.path.splitext(matching_file)[0] + ".dng"
                dng_path = os.path.join(converted_directory_path, dng_filename)

                if not os.path.exists(dng_path):
                    print(raw_photo_path)
                    raw_photo_paths.add(raw_photo_path)
                else:
                    print(
                        f"Skipping {raw_photo_path} as it has already been converted."
                    )

        else:
            print(
                f"No files with the specified extensions found in the '{dropbox_folder}' directory."
            )

    else:
        print(
            f"The '{dropbox_folder}' directory does not exist in the script's directory."
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
    print(f"Converted {source_path}")


def move_dngs():
    """
    Finds all files with .dng extension in dropbox directory
    Moves .dng files to converted directory if it exists
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))

    source_directory_name = "dropbox"
    destination_directory_name = "converted"

    source_directory_path = os.path.join(script_directory, source_directory_name)
    destination_directory_path = os.path.join(
        script_directory, destination_directory_name
    )

    if os.path.exists(source_directory_path) and os.path.isdir(source_directory_path):
        if not os.path.exists(destination_directory_path):
            os.makedirs(destination_directory_path)

        dng_files = [
            filename
            for filename in os.listdir(source_directory_path)
            if filename.endswith(".dng")
        ]

        for dng_file in dng_files:
            source_file_path = os.path.join(source_directory_path, dng_file)
            destination_file_path = os.path.join(destination_directory_path, dng_file)
            shutil.move(source_file_path, destination_file_path)

        print(
            f"Moved {len(dng_files)} .dng files to the '{destination_directory_name}' directory."
        )
    else:
        print(
            f"The '{source_directory_name}' directory does not exist in the script's directory."
        )


def main():
    photo_paths = get_from_dropbox()

    for path in photo_paths:
        time.sleep(1)
        convert_to_dng(path)

    if len(photo_paths) != 0:
        print("Preparing to move dng files.")
        time.sleep(3)

        move_dngs()
    else:
        print("No files where moved.")


if __name__ == "__main__":
    main()
