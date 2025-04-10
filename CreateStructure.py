import os

def create_structure_from_file(file_path, base_folder="generated_project"):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    path_stack = []
    base_indent = None

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line or stripped_line.startswith("```") or "──" not in line:
            continue

        indent_pos = line.find('├')
        if indent_pos == -1:
            indent_pos = line.find('└')
        if indent_pos == -1:
            indent_pos = line.find('│')
        if indent_pos == -1:
            indent_pos = 0

        if base_indent is None:
            base_indent = indent_pos

        level = (indent_pos - base_indent) // 4
        name = line.split('──')[-1].split('#')[0].strip()

        if not name:
            continue

        path_stack = path_stack[:level] + [name.rstrip('/')]
        current_path = os.path.join(base_folder, *path_stack)

        try:
            if name.endswith("/"):
                os.makedirs(current_path, exist_ok=True)
            else:
                dir_name = os.path.dirname(current_path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)
                with open(current_path, 'w', encoding='utf-8') as f:
                    f.write('')
        except Exception as e:
            print(f"❌ Error creating {current_path}: {e}")

    print(f"✅ Project structure created inside '{base_folder}'")

if __name__ == "__main__":
    create_structure_from_file("folders.txt")
