import os
import subprocess
from pathlib import Path
import shutil
import uuid

def clear_temp(file_path):
    temp_dir = os.path.dirname(file_path)

    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)

def save_in_temp_folder(file, base_file):
    base_dir = os.path.dirname(os.path.abspath(base_file))
    temp_dir = os.path.join(base_dir, "temp", str(uuid.uuid4()))
    os.makedirs(temp_dir, exist_ok=True)

    if hasattr(file, "save"):
        full_path = os.path.join(temp_dir, file.filename)
        file.save(full_path)
    else:
        source = Path(file)
        full_path = os.path.join(temp_dir, source.name)
        shutil.copy2(source, full_path)

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