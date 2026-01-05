import os

def clear_temp(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(directory)

def save_in_temp_folder(file, base_file):
    base_dir = os.path.dirname(os.path.abspath(base_file))
    temp_dir = os.path.join(base_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    full_path = os.path.join(temp_dir, file.filename)
    file.save(full_path)

    return full_path