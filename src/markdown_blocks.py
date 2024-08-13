import re
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

block_type_paragraph="paragraph"
block_type_heading="heading"
block_type_code="code"
block_type_quote="quote"
block_type_ulist="unordered_list"
block_type_olist="ordered_list"

def block_to_block_type(block: str):
    if re.match(r"^#{1,6} .*", block):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code

    lines = block.splitlines()
    list_line_starting_with_gt = list(filter(lambda x: x.startswith(">"), lines))
    list_line_unordered = list(filter(lambda x: x.startswith("* ") or x.startswith("- "), lines))
    if len(list_line_starting_with_gt) == len(lines):
        return block_type_quote
    if len(list_line_unordered) == len(lines):
        return block_type_ulist

    line_count = 0
    for line in lines:
        if line.startswith(f"{line_count + 1}."):
            line_count +=1
    if line_count == len(lines):
        return block_type_olist

    return block_type_paragraph
