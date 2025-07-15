import os
import zipfile
import shutil
import ezdxf
from openpyxl import load_workbook
from ezdxf.enums import TextEntityAlignment
from datetime import datetime

def importAttributesFromXlsx(xlsxPath, zipPath):
    # criando pastas temporárias pra trabalhar em paralelo
    timestamp = datetime.now().isoformat().replace(":", "-")
    temp_dir = f"temp_dxf_{timestamp}"
    edited_dir = os.path.join(temp_dir, "edited")
    os.makedirs(edited_dir, exist_ok=True)

    # extraindo arquivos do .zip
    with zipfile.ZipFile(zipPath, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    wb = load_workbook(xlsxPath)
    ws = wb.active
    header = [cell.value for cell in ws[1]]
    idx_nome = header.index("PartName")
    idx_esp = header.index("Thickness")
    idx_mat = header.index("Material")
    idx_qtd = header.index("Quantity")

    for row in ws.iter_rows(min_row=2, values_only=True):
        nome_peca = str(row[idx_nome])
        espessura = row[idx_esp]
        material = row[idx_mat]
        quantidade = row[idx_qtd]

        nome_arquivo = f'{nome_peca}.dxf'
        caminho_entrada = os.path.join(temp_dir, nome_arquivo)
        caminho_saida = os.path.join(edited_dir, nome_arquivo)

        if not os.path.exists(caminho_entrada):
            print(f'[Aviso] Arquivo não encontrado: {nome_arquivo}')
            continue

        try:
            doc = ezdxf.readfile(caminho_entrada)
            msp = doc.modelspace()

            if "Administração" not in doc.layers:
                doc.layers.new(name='Administração', dxfattribs={'color': 1})

            textos = [
                f'Part Name {nome_peca}',
                f'Thickness {espessura}',
                f'Material {material}',
                f'Quantity {quantidade}',
            ]

            y_offset = -15
            for texto in textos:
                msp.add_text(
                    texto,
                    dxfattribs={
                        'layer': 'Administração',
                        'height': 10,
                        'style': 'Arial'
                    }
                ).set_placement((0, y_offset), align=TextEntityAlignment.LEFT)
                y_offset -= 12

            doc.saveas(caminho_saida)
        except Exception as e:
            print(f'[Erro] {nome_arquivo}: {e}')

    output_folder = os.path.join(os.path.dirname(__file__), "editedDxfFiles")
    os.makedirs(output_folder, exist_ok=True)

    outputPath = os.path.join(output_folder, f"resultado_{timestamp}.zip")

    base_path = os.path.splitext(outputPath)[0]
    zip_final_path = shutil.make_archive(base_path, 'zip', edited_dir)

    shutil.rmtree(temp_dir)

    return zip_final_path
