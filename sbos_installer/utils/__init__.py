def modify_file_entry(file_path, search_string, replace_string):
    with open(file_path, 'r') as file:
        content = file.read()

    modified_content = content.replace(search_string, replace_string)

    with open(file_path, 'w') as file:
        file.write(modified_content)