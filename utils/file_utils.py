import os
import subprocess

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

def convert_file(input_path, output_extension="dxf", cad_version="ACAD2010"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

    input_path = os.path.abspath(input_path)
    input_dir = os.path.dirname(input_path)

    output_dir = os.path.join(input_dir, "out")
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "xvfb-run",
        "-a",
        "ODAFileConverter",
        input_dir,
        output_dir,
        cad_version,
        output_extension.upper(),
        "0",
        "1"
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro ao converter:\n{e.stderr}")

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    converted_file = os.path.join(output_dir, base_name + "." + output_extension.lower())

    if not os.path.exists(converted_file):
        raise RuntimeError("Arquivo convertido não foi gerado.")

    return converted_file