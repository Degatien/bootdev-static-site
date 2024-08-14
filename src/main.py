import os
import shutil
from copystatic import (
    copy_dir_content
)
from gencontent import generate_pages_recursive
    
def main():
    if os.path.exists("public"):
        print("Path public exists, deleting its content")
        shutil.rmtree("public")
    print("Creating public dir")
    os.mkdir("public")
    copy_dir_content("static", "public")
    generate_pages_recursive("content", "template.html", "public")    

main()

