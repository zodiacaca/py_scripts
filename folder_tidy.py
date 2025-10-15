
import os
import shutil

names = []

def tidy_folder(folder_paths):
    for folder_path in folder_paths:
        for root, folders, files in os.walk(folder_path):
            # print(f"path: {root}, folders: {len(folders)}, count: {len(files)}")
            if len(folders) == 0 and len(files) == 1 and len(root.split("\\")) == 6:

            """
                old_file = os.path.join(root, files[0])
                shutil.move(old_file, folder_path)
            """

            """
                if files[0] in names:
                    new_name = root.split("\\")[-1] + "." + files[0].split(".")[-1]
                    old_file = os.path.join(root, files[0])
                    new_file = os.path.join(root, new_name)
                    os.rename(old_file, new_file)
                    print(old_file)
                    print(new_file)
                else:
                    names.append(files[0])
            """

            """
            if len(folders) == 0 and len(files) == 0:
                print(root)
                # os.rmdir(root)
            """

if __name__ == "__main__":
    folder_paths = set([
        r"D:\NAS-01-D\Media",
        r"E:\NAS-01-E",
        r"F:\NAS-01-F",
        r"U:\NAS-01-U\[porn]",
        r"U:\NAS-01-U\GirlsSection",
        r"U:\NAS-01-U\impulse"
    ])

    tidy_folder(folder_paths)
