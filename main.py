import os
import time

# open -a /Applications/Adobe\ DNG\ Converter.app --args -c /path/to/photo
# open -a /Applications/Adobe\ DNG\ Converter.app --args -c /Users/dawsonpar/Desktop/coding/AU/20230126_0162_dp.cr3


def get_from_dropbox():
    """
    Looks for dropbox folder inside of current directory
    Finds raw photos inside dropbox folder
    Returns:
        raw_photo_paths : set with paths to raw photos
    """

    # Get the current directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))

    dropbox_folder = "dropbox"

    subdirectory_path = os.path.join(script_directory, dropbox_folder)

    raw_photo_paths = set()

    # Check if the subdirectory exists
    if os.path.exists(subdirectory_path) and os.path.isdir(subdirectory_path):
        # List all files with the ".cr3" extension in the "dropbox" directory
        cr3_files = [
            filename
            for filename in os.listdir(subdirectory_path)
            if filename.endswith(".cr3")
        ]

        if cr3_files:
            print(
                f"Found {len(cr3_files)} '.cr3' files in the '{dropbox_folder}' directory:"
            )
            for cr3_file in cr3_files:
                # print(os.path.join(subdirectory_path, cr3_file))
                raw_photo_paths.add(os.path.join(subdirectory_path, cr3_file))
        else:
            print(f"No '.cr3' files found in the '{dropbox_folder}' directory.")
    else:
        print(
            f"The '{dropbox_folder}' directory does not exist in the script's directory."
        )

    print(raw_photo_paths)
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
    print("Converted photo")


def main():
    # path_to_photos = "/Users/dawsonpar/Desktop/coding/AU/20230126_0167_dp.cr3"
    # convert_to_dng(path_to_photos)
    photo_paths = get_from_dropbox()

    for path in photo_paths:
        convert_to_dng(path)
        print("Converted" + path)
        time.sleep(1)


if __name__ == "__main__":
    main()
