import sys
import ezdxf
import os
import re

constFileName = "./slashCommands/VerificadorDeDesenho/DesenhoSaves/C122021-1BF1_BF-B0-09_00.dxf"
# doc = ezdxf.readfile(sys.argv[1])
doc = ezdxf.readfile(constFileName)
msp = doc.modelspace()

#Verifica o nome do arquivo está separado corretamente
#fileName = os.path.splitext(os.path.basename(sys.argv[1]))
fileName = os.path.splitext("C122021-1BF1_BF-B0-09_00.dxf")
fileName = fileName[0]
fileName = fileName.replace('EXECUTANDO_', '')
fileName = fileName.replace('ENTREGA_', '')

pattern = r'^[A-Z0-9]+-[A-Z0-9]+_[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+_[A-Z0-9]+$'

codigo = fileName.split('-')  
codigo = [item.split('_') for item in codigo]  
codigo = sum(codigo, [])  

if re.match(pattern, fileName):
    print("O arquivo esta separado corretamente.")
else:
    print(f"O arquivo nao esta separado corretamente.\nCorreto: {codigo[0]}-{codigo[1]}_{codigo[2]}-{codigo[3]}-{codigo[4]}_{codigo[5]}" )

#//////////////////////////////////////////

for insert in msp.query('INSERT[name=="REDECAM-TITOLO-TAVOLA"]'):
    for attrib in insert.attribs:
        print('Tag: {} Value: {}'.format(attrib.dxf.tag, attrib.dxf.text))