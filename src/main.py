import os
import shutil

def copy_dir_content(src_dir:str, dest_dir: str):
    print(f"Starting the copy of {src_dir} to {dest_dir}")
    if os.path.exists(src_dir) == False:
        raise Exception(f"{src_dir} doesnt exists")
    if os.path.exists(dest_dir) == False:
        print(f"Creating {dest_dir} directory")
        os.mkdir(dest_dir)
    files = os.listdir(src_dir)
    print(f"Found {len(files)} files in {src_dir}")

    for file in files:
        src_file_path = os.path.join(src_dir, file)
        dest_file_path = os.path.join(dest_dir, file)
        print(f"Copying {src_file_path} to {dest_file_path}")
        if os.path.isfile(src_file_path):
            shutil.copy(src_file_path, dest_file_path)
        elif os.path.isdir(src_file_path):
            copy_dir_content(src_file_path, dest_file_path)
        else:
            raise Exception(f"{src_file_path} is not file or dir")

def main():
    if os.path.exists("./public"):
        print("Path public exists, deleting its content")
        shutil.rmtree("./public")
    print("Creating public dir")
    os.mkdir("./public")
    copy_dir_content("./static", "./public")

main()

