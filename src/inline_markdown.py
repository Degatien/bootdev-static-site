import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        original_text = node.text
        extracted_images = extract_markdown_images(original_text)

        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue

        for (image_alt, image_link) in extracted_images:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(image_alt, text_type_image, image_link))
            original_text = sections[1]
        if len(original_text) > 0:
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        original_text = node.text
        extracted_links = extract_markdown_links(original_text)

        if len(extracted_links) == 0:
            new_nodes.append(node)
            continue

        for (text, url) in extracted_links:
            sections = original_text.split(f"[{text}]({url})", 1)
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(text, text_type_link, url))
            original_text = sections[1]
        if len(original_text) > 0:
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes
    
