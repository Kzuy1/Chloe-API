from errorDrawing import errorDrawing
from datetime import datetime
import ezdxf
import os
import re

class Drawing:
    def __init__(self, fullPath, dataIssue = None):
        self.errorDrawing = errorDrawing()
        self.fullPath = fullPath
        self.dataIssue = dataIssue
        self.fileDrawingCode = self.getDrawingCode()
        self.fileDrawingCodeSeparate = self.getDrawingCodeSeparate()
        self.docDXF = ezdxf.readfile(self.fullPath)
        self.mspDXF = self.docDXF.modelspace()
        self.subtitleBlock = self.getBlockInfo('REDECAM-TITOLO-TAVOLA')
        self.revisionBlocks = self.getBlockInfo('REDE-DISTINTA-REVISIONE')
        self.revisionBlocks = self.sortBlock(self.revisionBlocks, 'REV-N')

        #Verifica se existe dois ou mais Bloco de Título no mesmo Desenho, 
        if len(self.subtitleBlock) != 1:
            self.errorDrawing.ed09['booleanValue'] = True
            self.message = self.errorDrawing.getErrorMessages()
            return
        # Se não transforma self.subtitleBlock em um só objeto invés de lista
        self.subtitleBlock = self.subtitleBlock[0]
        
        self.checkdataIssue()
        self.checkCorrectSeparation()
        self.checksubtitleBlock()
        self.checkRevisionBlock()
        self.checkLineScaleFactor()
        self.checkLeader()
        self.checkBlockInR16()
        self.checkLayerInR16()

        self.message = self.errorDrawing.getErrorMessages()

    # Função para pegar o código do Desenho
    def getDrawingCode(self):
        drawingCode = os.path.splitext(os.path.basename(self.fullPath))[0]
        drawingCode = drawingCode.split('_', 1)
        drawingCode = drawingCode[1]
        drawingCode = drawingCode.replace('EXECUTANDO_', '')
        drawingCode = drawingCode.replace('ENTREGA_', '')
        
        return drawingCode
    
    # Função para pegar o código do Desenho separado
    def getDrawingCodeSeparate(self):
        codeSeparate = self.fileDrawingCode.split('-')  
        codeSeparate = [item.split('_') for item in codeSeparate]
        codeSeparate = sum(codeSeparate, [])

        return codeSeparate
    
    # Função para verificar a Data de Emissão
    def checkdataIssue(self):
        if self.dataIssue is None:
            self.dataIssue = datetime.now().strftime("%d/%m/%y")

    # Função para pegar as informações de Blocos
    def getBlockInfo(self, blockName):
        blocksList = []

        for insert in self.mspDXF.query(f'INSERT[name=="{blockName}"]'):
            blockInfo = {}
            
            for attrib in insert.attribs:
                tag = attrib.dxf.tag
                value = attrib.dxf.text
                height = attrib.dxf.height

                blockInfo[tag] = {'value': value, 'height': height}
            blockInfo['x_scale'] = insert.get_dxf_attrib('xscale') or 1
            blockInfo['y_scale'] = insert.get_dxf_attrib('yscale') or 1
            blockInfo['z_scale'] = insert.get_dxf_attrib('zscale') or 1

            blocksList.append(blockInfo)
        
        return blocksList
    
    # Função para ordenar em forma crescente os Blocos de acordo com atributos
    def sortBlock(self, blocksList, attribute):
        return sorted(blocksList, key=lambda x: int(x[attribute]['value']))

    # Função para verificar se está separado certo o codigo
    def checkCorrectSeparation(self):
        regexCode = r'^[A-Z0-9]+-[A-Z0-9]+_[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+_[A-Z0-9]+$'

        if not re.match(regexCode, self.fileDrawingCode):
            self.errorDrawing.ed01['booleanValue'] = True

            if len(self.fileDrawingCodeSeparate) == 6:
                self.errorDrawing.ed01['description'] += f' Correto: {self.fileDrawingCodeSeparate[0]}-{self.fileDrawingCodeSeparate[1]}_{self.fileDrawingCodeSeparate[2]}-{self.fileDrawingCodeSeparate[3]}-{self.fileDrawingCodeSeparate[4]}_{self.fileDrawingCodeSeparate[5]}\n'

    # Função para verificar as informações do Bloco de Título do Desenho
    def checksubtitleBlock(self):
        #Verifica se está na versão R18
        if 'EXCL' in self.subtitleBlock:
            self.errorDrawing.edOB['booleanValue'] = True
            self.errorDrawing.edOB['description'] += "REDECAM-TITOLO-TAVOLA - Bloco de Legenda\n"
        
        #Verifica se está na versão R16
        if 'REV-CARTIGLIO_1_0' in self.subtitleBlock:
            if (2 * self.subtitleBlock['x_scale'] - self.subtitleBlock['REV-CARTIGLIO_1_0']['height']) > 0.01:
                self.errorDrawing.edOB['booleanValue'] = True
                self.errorDrawing.edOB['description'] += "\t\tREDECAM-TITOLO-TAVOLA - Bloco de Legenda\n"

        # Verifica cada chave e seu valor correspondente somente se o Error 01 não tiver ativo
        if self.errorDrawing.ed01['booleanValue'] == False:
            # Chaves do Código do Desenho
            keyCodes = {
                'COMMESSA-N.': self.fileDrawingCodeSeparate[0] + '-' + self.fileDrawingCodeSeparate[1],
                'APP': self.fileDrawingCodeSeparate[2],
                'GRUP': self.fileDrawingCodeSeparate[3],
                'DIS': self.fileDrawingCodeSeparate[4],
                'REV': self.fileDrawingCodeSeparate[5]
            }

            for key, keyValue in keyCodes.items():
                if self.subtitleBlock[key]['value'] != keyValue:
                    
                    self.errorDrawing.ed02['booleanValue'] = True
                    break

        # Verifica se a escala condiz com o que está escrito
        scaleSubtitle = self.subtitleBlock['SCALA']['value']
        if scaleSubtitle in ('', "1:__") or abs(float(scaleSubtitle.replace("1:", "")) - self.subtitleBlock['x_scale']) > 0.0001:
            self.errorDrawing.ed03['booleanValue'] = True

        # Verifica se o desenho foi feito por EMB
        if 'SIGLA' in self.subtitleBlock and self.subtitleBlock['SIGLA']['value'] != 'EMB' :
            self.errorDrawing.ed04['booleanValue'] = True
        
        # Verifica se o desenho foi aprovado por VOL
        if 'S-CONT' in self.subtitleBlock and self.subtitleBlock['S-CONT']['value'] != 'VOL' :
            self.errorDrawing.ed04['booleanValue'] = True

        # Verifica se a aprovação está vazia, por que cliente deve aprovar
        if 'APPROVATO' in self.subtitleBlock and self.subtitleBlock['APPROVATO']['value'] != '' :
            self.errorDrawing.ed04['booleanValue'] = True

    # Função para verificar Escala dos Blocos de Revisão
    def checkRevisionBlock(self):
        for revisionBlock in self.revisionBlocks:
            # Verifica Escala do Bloco de Revisão
            if abs(self.subtitleBlock['x_scale'] - revisionBlock['x_scale']) > 0.0001 :
                self.errorDrawing.edSC['booleanValue'] = True
                self.errorDrawing.edSC['description'] += '\t\t REDE-DISTINTA-REVISIONE - Bloco de Revisão ' + revisionBlock['REV-N']['value']
            
            # Verifica Bloco de Revisão até última Revisão se está Preenchido
            if int(revisionBlock['REV-N']['value']) <= int(self.fileDrawingCodeSeparate[5]):
                for attribs in revisionBlock.values():
                    if isinstance(attribs, dict) and attribs['value'] == None:
                        self.errorDrawing.ed12['booleanValue'] = True
            
        # Verifica se a data Bloco de Revisão 0 é o mesmo no Bloco de Legenda
        if self.revisionBlocks[0]['REV-D']['value'] != self.subtitleBlock['DATA']['value']:
            self.errorDrawing.ed10['booleanValue'] = True
        
        # Verifica se a data da revisão atual do desenho condiz com o bloco de revisão
        if self.revisionBlocks[int(self.fileDrawingCodeSeparate[5])]['REV-D']['value'] != self.subtitleBlock['D-REV']['value']:
            self.errorDrawing.ed11['booleanValue'] = True
        
        # Verifica se a data da revisão atual do desenho condiz com a Date de Emissão do Usuário, Padrão: Data de Hoje
        if self.revisionBlocks[int(self.fileDrawingCodeSeparate[5])]['REV-D']['value'] != self.dataIssue:
            self.errorDrawing.ed13['booleanValue'] = True
            self.errorDrawing.ed13['description'] += self.dataIssue

    # Função para verificar o LTScale
    def checkLineScaleFactor(self):
        ltscale = self.docDXF.header['$LTSCALE']

        if abs(self.subtitleBlock['x_scale']/2 - ltscale) > 0.0001  :
            self.errorDrawing.ed06['booleanValue'] = True

    # Função para verificar as Leader
    def checkLeader(self):
        for leader in self.mspDXF.query('LEADER'):
            if leader.dxf.layer != 'QUOTE':
                self.errorDrawing.ed08['booleanValue'] = True

                return

    # Função para verificar se um bloco existe no Desenho
    def _checkBlockExists(self, blockName):
        block = self.docDXF.blocks.get(blockName)

        if block is not None:
            return True

    # Função para verificar os blocos que estão no R16
    def checkBlockInR16(self):
        blocksToCheck = [
            ('REDECAM_REVISION', 'Bloco de Revisão na R16\n'),
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

        for blockName in blocksToCheck:
            verifyBlock = self._checkBlockExists(blockName[0])

            if verifyBlock: 
                self.errorDrawing.edOB['booleanValue'] = True
                self.errorDrawing.edOB['description'] += '\t\t' + blockName[0] + " - " + blockName[1]
        
        # Verificação de Blocos de Solda
        if self._checkBlockExists('TIPICO-SALDATURA_ENG-POR') or \
            self._checkBlockExists('TIPICO-SALDATURA_ITA-ENG'): 
                self.errorDrawing.edOB['booleanValue'] = True
                self.errorDrawing.edOB['description'] += '\t\tTIPICO-SALDATURA - Bloco de Solda\n'

        # Verificação de Blocos do Formato
        if self._checkBlockExists('REDE-A0') or \
            self._checkBlockExists('REDE-A1') or \
            self._checkBlockExists('REDE-A2') or \
            self._checkBlockExists('REDE-A3'):
                self.errorDrawing.edOB['booleanValue'] = True
                self.errorDrawing.edOB['description'] += '\t\tREDE - Bloco de folha\n'
            
        # Verificação do Bloco de Junta
        if self._checkBlockExists('REDECAM-GUARNIZIONI_monolingua'):
            block = self.docDXF.blocks.get('REDECAM-GUARNIZIONI_monolingua')

            # Acessa as entidades dentro do bloco e procure um Texto escrito m (Metro)
            for entity in block:
                if entity.dxftype() == 'TEXT' and entity.dxf.text == 'm':
                    return
            
            # Caso não tenha informa que o Bloco está na Versão antiga
            self.errorDrawing.edOB['booleanValue'] = True
            self.errorDrawing.edOB['description'] += '\t\tREDECAM-GUARNIZIONI - Bloco de Junta\n'

    # Função para verificar se a Layer Existe
    def checkLayerInR16(self):
        if "CONTOUR EXI" in self.docDXF.layers:
            self.errorDrawing.ed07['booleanValue'] = True