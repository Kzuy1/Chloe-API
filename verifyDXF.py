import ezdxf
import os
import re

class veriftDrawingDXF:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.message = ''
        self.fileDrawingCode = self.getDrawingCode()
        self.docDXF = ezdxf.readfile(self.fullPath)
        self.mspDXF = self.docDXF.modelspace()
        self.checkCorrectSeparation()
        self.subtitleBlock = self.getSubtitleBlock()
        self.checkBlockInR16()
        self.checkLayerInR16()
        

    # Função para pegar o código do Desenho
    def getDrawingCode(self):
        drawingCode = os.path.splitext(os.path.basename(self.fullPath))[0]
        drawingCode = drawingCode.replace('EXECUTANDO_', '')
        drawingCode = drawingCode.replace('ENTREGA_', '')

        return(drawingCode)

    # Função para verificar se está separado certo o codigo
    def checkCorrectSeparation(self):
        regexCode = r'^[A-Z0-9]+-[A-Z0-9]+_[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+_[A-Z0-9]+$'

        codeSeparate = self.fileDrawingCode.split('-')  
        codeSeparate = [item.split('_') for item in codeSeparate]  
        codeSeparate = sum(codeSeparate, [])  

        if not re.match(regexCode, self.fileDrawingCode):
            self.message += 'O arquivo não está separado corretamente. '

            if len(codeSeparate) == 6:
                self.message += f'Correto: {codeSeparate[0]}-{codeSeparate[1]}_{codeSeparate[2]}-{codeSeparate[3]}-{codeSeparate[4]}_{codeSeparate[5]}\n'
            else:
                self.message += '\n'
    
    # Função para pegar as informações do Bloco de Título do Desenho
    def getSubtitleBlock(self):
        dataSubtitle = {}
        for insert in self.mspDXF.query('INSERT[name=="REDECAM-TITOLO-TAVOLA"]'):
            for attrib in insert.attribs:
                tag = attrib.dxf.tag
                value = attrib.dxf.text
                height = attrib.dxf.height

                dataSubtitle[tag] = {'value': value, 'height': height}
            dataSubtitle['x_scale'] = insert.get_dxf_attrib('xscale')
            dataSubtitle['y_scale'] = insert.get_dxf_attrib('yscale')
            dataSubtitle['z_scale'] = insert.get_dxf_attrib('zscale')

        if 'EXCL' in dataSubtitle:
            self.message += 'Titulo, Bloco R18\n'
        
        if 'REV-CARTIGLIO_1_0' in dataSubtitle and dataSubtitle['REV-CARTIGLIO_1_0']['height'] != 2:
            self.message += 'Titulo, Bloco R16\n'

    # Função para verificar se um bloco existe no Desenho
    def checkBlockExists(self, blockName):
        block = self.docDXF.blocks.get(blockName)

        if block is not None:
            return True

    # Função para verificar os blocos que estão no R16
    def checkBlockInR16(self):
        blocksToCheck = [
            ('REDE-DISTINTA-REVISIONE', 'Bloco de Revisão na R16\n'),
            ('TABELLA COPPIE SERRAGGIO - METRICO', 'Tabela de Torque na R16\n'),
            ('PARTICOLARE-GUARNIZIONE', 'Bloco Gasket na R16\n'),
            ('MARCA', 'Bloco Marca na R16\n'),
            ('LIVELLO-ALZATO', 'Bloco de Nível na R16\n'),
            ('LIVELLO-PIANTA', 'Bloco de Nível para Superficie na R16\n'),
            ('TIPICO-SALDATURA_FLANGE-L', 'Bloco de Solda no Flange R16\n'),
            ('TIPICO-SALDATURA_FLANGE-PIANE', 'Bloco de Solda com Chapa no Flange R16\n'),
            ('EMB_LISTA_DE_MATERIAL', 'Bloco de Material R16\n'),
            ('EMB_LISTA_DE_MATERIAL_INFO_ING', 'Bloco de Material das Informações na R16\n'),
            ('EMB_LISTA_DE_MATERIAL_DESCRITIVO_ING', 'Bloco de Material das Descrições na R16\n'),
            ('EMB_LISTA_DE_MATERIAL_INFO', 'Bloco de Material das Informações na R16\n'),
            ('EMB_LISTA_DE_MATERIAL_DESCRITIVO', 'Bloco de Material das Descrições na R16\n')
        ]

        for block in blocksToCheck:
            verifyBlock = self.checkBlockExists(block[0])

            if verifyBlock: self.message += block[1]
        
        # Verificação de blocos de Solda
        if self.checkBlockExists('TIPICO-SALDATURA_ENG-POR') or \
            self.checkBlockExists('TIPICO-SALDATURA_ITA-ENG'): 
                self.message += 'Bloco de Solda na R16\n'

        # Verificação de blocos de formato
        if self.checkBlockExists('REDE-A0') or \
            self.checkBlockExists('REDE-A1') or \
            self.checkBlockExists('REDE-A2') or \
            self.checkBlockExists('REDE-A3'): 
                self.message += ('Bloco de folha na R16\n')

    # Função para verificar se a Layer Existe
    def checkLayerInR16(self):
        if "CONTOUR EXI" in self.docDXF.layers:
            self.message += f'A Layer CONTOUR EXI existe no arquivo\n'