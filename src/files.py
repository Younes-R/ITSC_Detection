import os


def list_files_in_directory(directory_path):
    """
    Lists all files in the given directory.
    :param directory_path: Path to the directory
    :return: List of file names
    """
    try:
        # Check if the path exists and is a directory
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory '{directory_path}' does not exist.")
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"'{directory_path}' is not a directory.")

        # List only files (exclude subdirectories)
        files = [
            f
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]
        return files

    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    file_list = list_files_in_directory(folder_path)

    if file_list:
        print("\nFiles in the folder:")
        for file_name in file_list:
            print(file_name)
    else:
        print("No files found or an error occurred.")
