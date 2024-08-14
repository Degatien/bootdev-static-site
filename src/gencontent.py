import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown:str ):
    lines = markdown.splitlines()

    lines_filtered: list[str] = list(filter(lambda x: x.startswith("# "), lines))
    

    if len(lines_filtered) == 0:
        raise Exception("No title found")

    return lines_filtered[0].strip("#").strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.exists(from_path) == False:
        raise Exception(f"Path {from_path} does not exists")
    if os.path.exists(template_path) == False:
        raise Exception(f"Path {template_path} does not exists")

    from_path_file = open(from_path, "r")
    from_content = from_path_file.read()
    from_path_file.close()

    template_path_file = open(template_path, "r")
    template_content = template_path_file.read()
    template_path_file.close()

    html_nodes = markdown_to_html_node(from_content)

    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_nodes.to_html())
    
    
    dest_path_file = open(dest_path, "w")
    dest_path_file.write(template_content)
    dest_path_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating the page of {dir_path_content} to {dest_dir_path}")
    if os.path.exists(dir_path_content) == False:
        raise Exception(f"{dir_path_content} doesnt exists")
    if os.path.exists(dest_dir_path) == False:
        print(f"Creating {dest_dir_path} directory")
        os.mkdir(dest_dir_path)
    files = os.listdir(dir_path_content)
    print(f"Found {len(files)} files in {dir_path_content}")

    for file in files:
        src_file_path = os.path.join(dir_path_content, file)
        dest_file_path = os.path.join(dest_dir_path, file).replace(".md", ".html")
        print(f"Copying {src_file_path} to {dest_file_path}")
        if os.path.isfile(src_file_path):
            if src_file_path.endswith(".md") == False:
                continue
            generate_page(src_file_path, template_path, dest_file_path)
        elif os.path.isdir(src_file_path):
            generate_pages_recursive(src_file_path, template_path, dest_file_path)
        else:
            raise Exception(f"{src_file_path} is not file or dir")

