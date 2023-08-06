import ezdxf
import openpyxl
import os
import zipfile

def lista(fullPath) :
  workbook = openpyxl.load_workbook(fullPath, data_only= True)
  fatherPath = os.path.abspath(".")

  def writeFiles(elemento):
    worksheetMaterial = workbook[elemento + ' - MATERIAL']
    MaterialList = []

    for row in range(2, worksheetMaterial.max_row + 1):
      cell_value = worksheetMaterial.cell(row=row, column=12).value
      if cell_value == None:
        break
      material = {
        'POS' : worksheetMaterial.cell(row=row, column=12).value,
        'descricao' : worksheetMaterial.cell(row=row, column=13).value,
        'unidade' : worksheetMaterial.cell(row=row, column=14).value,
        'QTDE' : f"{worksheetMaterial.cell(row=row, column=15).value:.1f}",
        'material' : worksheetMaterial.cell(row=row, column=16).value,
        'PesoTotal' : f"{worksheetMaterial.cell(row=row, column=17).value:.1f}"
      }
      MaterialList.append(material)

    worksheetPeca = workbook[elemento + ' - PEÇAS']
    PecaList = []

    for row in range(2, worksheetPeca.max_row + 1):
      cell_value = worksheetPeca.cell(row=row, column=1).value
      if cell_value == None:
        break
      peca = {
        'cod' : '...' + worksheetPeca.cell(row=row, column=2).value,
        'descricao' : worksheetPeca.cell(row=row, column=6).value or worksheetPeca.cell(row=row, column=7).value or worksheetPeca.cell(row=row, column=5).value,
        'QTDE' : worksheetPeca.cell(row=row, column=4).value,
        'material' : worksheetPeca.cell(row=row, column=8).value,
        'PesoUnit' : f"{worksheetPeca.cell(row=row, column=11).value:.1f}",
        'PesoTotal' : f"{worksheetPeca.cell(row=row, column=12).value:.1f}"
      }
      PecaList.append(peca)
    
    doc = ezdxf.readfile(fatherPath + '/BLOCO-BRANCO.dxf')
    msp = doc.modelspace()
      
    bloco_material = doc.blocks.get('EMB_LISTA_DE_MATERIAL')

    posForBlock = None
    if bloco_material :
      for indice, objeto in enumerate(MaterialList):
          pos = 196 + 7 * indice
          posForBlock = pos
          insert = msp.add_blockref(bloco_material.name, insert=(0, pos, 0))
          insert.add_attrib("POSICAO", objeto["POS"])
          insert.add_attrib("DESCRICAO", objeto["descricao"])
          insert.add_attrib("UNIDADE", objeto["unidade"])
          insert.add_attrib("QUANTIDADE", objeto["QTDE"])
          insert.add_attrib("MATERIAL", objeto["material"])
          insert.add_attrib("PESO", objeto["PesoTotal"])

    msp.add_blockref('EMB_LISTA_DE_MATERIAL_DESCRITIVO_ING', insert=(0, 182, 0))
    msp.add_blockref('EMB_LISTA_DE_MATERIAL_INFO_ING', insert=(0, posForBlock, 0))

    bloco_original = doc.blocks.get('REDECAM-DISTINTA_monolingua')

    if bloco_original :
      for indice, objeto in enumerate(PecaList):
          pos = posForBlock + 13 + 6 * indice
          insert = msp.add_blockref(bloco_original.name, insert=(0, pos, 0))
          insert.add_attrib("MARCA", objeto["cod"])
          insert.add_attrib("DESCRIZIONE-IT", objeto["descricao"])
          insert.add_attrib("DESCRIZIONE-IN-R1", objeto["descricao"])
          insert.add_attrib("QUANTITA'", objeto["QTDE"])
          insert.add_attrib("MATERIALE", objeto["material"])
          insert.add_attrib("PESO-CAD", objeto["PesoUnit"])
          insert.add_attrib("TOTALE", objeto["PesoTotal"])
          insert.add_attrib("LARGHEZZA", 0)
          insert.add_attrib("PROFONDITA'", 0)
          insert.add_attrib("ALTEZZA", 0)
          insert.add_attrib("CICLO-VERN-INT", 0)
          insert.add_attrib("CICLO-VERN-EST", 0)
          insert.add_attrib("VERNICIATURA-INT", 0)
          insert.add_attrib("VERNICIATURA-EST", 0)

    mtext = msp.add_mtext(
      text= "\A1;" + elemento,
      dxfattribs={
          "insert": (103.742, 585.407, 0),  
          "char_height": 25,  
          "width": 0,  
          "style": "Standard",
          "rotation": 0,
          "color": 4,
          "layer" : "QUOTE",
          "attachment_point": 5
      }
      )
    
    listPath = fatherPath + "/list/" + elemento + "_LISTA.dxf"
    doc.saveas(listPath)

    with zipfile.ZipFile(fatherPath + '/list/BLOCOS-BRANCOS.zip', 'a', compression=zipfile.ZIP_DEFLATED) as myzip:
      myzip.write(listPath, arcname=elemento + "_LISTA.dxf")
    
    os.remove(listPath)

  planilhas = workbook.worksheets
  nomes_planilhas = set()

  for planilha in planilhas[1:]:
      primeiro_valor = planilha.title.split('-')[0].strip()
      nomes_planilhas.add(primeiro_valor)

  nomes_planilhas = list(nomes_planilhas)
  nomes_planilhas.sort()

  zipFile = fatherPath + '/list/BLOCOS-BRANCOS.zip'
  with zipfile.ZipFile(zipFile, 'w', compression=zipfile.ZIP_DEFLATED) as myzip:
   myzip.write(fatherPath + '/BLOCO-BRANCO.dxf', arcname='BLOCO-BRANCO.dxf')

  for elemento in nomes_planilhas:
    writeFiles(elemento)
  
  return zipFile
