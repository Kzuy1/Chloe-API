from verifyDXF.ErrorDrawing import ErrorDrawing
from verifyDXF.Layer import LayerList
from datetime import datetime
import ezdxf
import os
import re

class Drawing:
    def __init__(self, full_path, data_issue = None):
        self.error_drawing = ErrorDrawing()
        self.full_path = full_path
        self.data_issue = data_issue
        self.file_drawing_code = self.get_drawing_code()
        self.file_drawing_code_separate = self.get_drawing_code_separate()
        self.layer_list = LayerList()
        self.layer_list.add_default_layer()
        self.doc_dxf = ezdxf.readfile(self.full_path)
        self.msp_dxf = self.doc_dxf.modelspace()
        self.subtitle_block = self.get_block_info('REDECAM-TITOLO-TAVOLA')
        self.revision_blocks = self.get_block_info('REDE-DISTINTA-REVISIONE')
        self.revision_blocks = self.sort_block(self.revision_blocks, 'REV-N')
        self.part_blocks = self.get_block_info('REDECAM-DISTINTA_monolingua')

        #Verifica se existe dois ou mais Bloco de Título no mesmo Desenho, 
        if len(self.subtitle_block) != 1:
            self.error_drawing.ed09['boolean_value'] = True
            self.message = self.error_drawing.get_error_messages()
            return
        # Se não transforma self.subtitleBlock em um só objeto invés de lista
        self.subtitle_block = self.subtitle_block[0]
        
        self.check_layer_properties()
        self.check_data_issue()
        self.check_correct_separation()
        self.check_subtitle_block()
        self.check_revision_block()
        self.check_part_block()
        self.check_line_scale_factor()
        self.check_leader()
        self.check_notes()
        self.check_block_in_R16()
        self.check_layer_in_R16()

        self.message = self.error_drawing.get_error_messages()

    # Função para pegar o código do Desenho
    def get_drawing_code(self):
        drawing_code = os.path.splitext(os.path.basename(self.full_path))[0]
        drawing_code = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}\.\d+_', '', drawing_code)
        drawing_code = drawing_code.replace('EXECUTANDO_', '')
        drawing_code = drawing_code.replace('ENTREGA_', '')

        return drawing_code
    
    # Função para pegar o código do Desenho separado
    def get_drawing_code_separate(self):
        code_separate = self.file_drawing_code.split('-')  
        code_separate = [item.split('_') for item in code_separate]
        code_separate = sum(code_separate, [])

        return code_separate
    
    # Função para verificar a Data de Emissão
    def check_data_issue(self):
        if self.data_issue is None:
            self.data_issue = datetime.now().strftime("%d/%m/%y")

    # Função para pegar as informações de Blocos
    def get_block_info(self, block_name):
        blocks_list = []

        for insert in self.msp_dxf.query(f'INSERT[name=="{block_name}"]'):
            block_info = {}
            
            for attrib in insert.attribs:
                print(attrib)
                tag = attrib.dxf.tag
                value = attrib.dxf.text
                height = attrib.dxf.height
                width_factor = attrib.dxf.width

                block_info[tag] = {'value': value, 'height': height, 'width_factor': width_factor}
            block_info['x_scale'] = insert.get_dxf_attrib('xscale') or 1
            block_info['y_scale'] = insert.get_dxf_attrib('yscale') or 1
            block_info['z_scale'] = insert.get_dxf_attrib('zscale') or 1

            blocks_list.append(block_info)
        
        return blocks_list
    
    # Função para ordenar em forma crescente os Blocos de acordo com atributos
    def sort_block(self, blocks_list, attribute):
        return sorted(blocks_list, key=lambda x: int(x[attribute]['value']))

    # Função para verificar as camadas
    def check_layer_properties(self):
        layers = self.doc_dxf.layers

        # Passa camada por camada no Desenho
        for layer in layers:
            name = layer.dxf.name
            visible = layer.is_on()
            frozen = layer.is_frozen()
            locked = layer.is_locked()
            color = layer.dxf.color
            line_type = layer.dxf.linetype
            line_weight = layer.dxf.lineweight

            # Procura se a camada existe
            default_layer = self.layer_list.layers.get(name)
            if default_layer is None: continue

            if (visible != default_layer.visible or 
                frozen != default_layer.frozen or 
                locked != default_layer.locked or 
                color != default_layer.color or 
                line_type != default_layer.line_type or 
                line_weight != default_layer.line_weight):
                    self.error_drawing.ed14['boolean_value'] = True
                    return

    # Função para verificar se está separado certo o codigo
    def check_correct_separation(self):
        regex_code = r'^[A-Z0-9]+-[A-Z0-9]+_[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+_[A-Z0-9]+$'

        if not re.match(regex_code, self.file_drawing_code):
            self.error_drawing.ed01['boolean_value'] = True

            if len(self.file_drawing_code_separate) == 6:
                self.error_drawing.ed01['description'] += f' Correto: {self.file_drawing_code_separate[0]}-{self.file_drawing_code_separate[1]}_{self.file_drawing_code_separate[2]}-{self.file_drawing_code_separate[3]}-{self.file_drawing_code_separate[4]}_{self.file_drawing_code_separate[5]}\n'

    # Função para verificar as informações do Bloco de Título do Desenho
    def check_subtitle_block(self):
        #Verifica se está na versão R18
        if 'EXCL' in self.subtitle_block:
            self._concat_blockname_error('REDECAM-TITOLO-TAVOLA', 'Bloco de Legenda')
        
        #Verifica se está na versão R16
        if 'REV-CARTIGLIO_1_0' in self.subtitle_block:
            if (2 * self.subtitle_block['x_scale'] - self.subtitle_block['REV-CARTIGLIO_1_0']['height']) > 0.01:
                self._concat_blockname_error('REDECAM-TITOLO-TAVOLA', 'Bloco de Legenda')

        # Verifica cada chave e seu valor correspondente somente se o Error 01 não tiver ativo
        if not self.error_drawing.ed01['boolean_value']:
            # Chaves do Código do Desenho
            key_codes = {
                'COMMESSA-N.': self.file_drawing_code_separate[0] + '-' + self.file_drawing_code_separate[1],
                'APP': self.file_drawing_code_separate[2],
                'GRUP': self.file_drawing_code_separate[3],
                'DIS': self.file_drawing_code_separate[4],
                'REV': self.file_drawing_code_separate[5]
            }

            for key, key_value in key_codes.items():
                if self.subtitle_block[key]['value'] != key_value:
                    self.error_drawing.ed02['boolean_value'] = True
                    break

        # Verifica se a escala condiz com o que está escrito
        scale_subtitle = self.subtitle_block['SCALA']['value']
        if scale_subtitle in ('', "1:__") or abs(float(scale_subtitle.replace("1:", "")) - self.subtitle_block['x_scale']) > 0.0001:
            self.error_drawing.ed03['boolean_value'] = True

        # Verifica se o desenho foi feito por EMB
        if 'SIGLA' in self.subtitle_block and self.subtitle_block['SIGLA']['value'] != 'EMB' :
            self.error_drawing.ed04['boolean_value'] = True
        
        # Verifica se o desenho foi aprovado por VOL
        if 'S-CONT' in self.subtitle_block and self.subtitle_block['S-CONT']['value'] != 'VOL' :
            self.error_drawing.ed04['boolean_value'] = True

        # Verifica se a aprovação está vazia, por que cliente deve aprovar
        if 'APPROVATO' in self.subtitle_block and self.subtitle_block['APPROVATO']['value'] != '' :
            self.error_drawing.ed04['boolean_value'] = True

    # Função para verificar Escala dos Blocos de Revisão
    def check_revision_block(self):
        # Verifica se Bloco de Revisão não está na versão antiga
        if self._checkBlockExists('REDECAM_REVISION'):
            self._concat_blockname_error('REDECAM_REVISION', 'Bloco de Revisão')
            return
        
        for revision_block in self.revision_blocks:
            # Verifica Escala do Bloco de Revisão
            if abs(self.subtitle_block['x_scale'] - revision_block['x_scale']) > 0.0001 :
                self.error_drawing.edSC['boolean_value'] = True
                self.error_drawing.edSC['description'] += '\t\t REDE-DISTINTA-REVISIONE - Bloco de Revisão ' + revision_block['REV-N']['value']

        # Verifica Bloco de Revisão atual está Preenchido
        if len(self.revision_blocks) < int(self.file_drawing_code_separate[5]) + 1:
            self.error_drawing.ed12['boolean_value'] = True
            return
        
        current_review_block = self.revision_blocks[int(self.file_drawing_code_separate[5])]
        for attribs in current_review_block.values():
            if isinstance(attribs, dict) and attribs['value'] == None:
                self.error_drawing.ed12['boolean_value'] = True
                return

        # Verifica se a data Bloco de Revisão 0 é o mesmo no Bloco de Legenda
        if self.revision_blocks[0]['REV-D']['value'] != self.subtitle_block['DATA']['value']:
            self.error_drawing.ed10['boolean_value'] = True
        
        # Verifica se a data da revisão atual do desenho condiz com o bloco de revisão
        if self.revision_blocks[int(self.file_drawing_code_separate[5])]['REV-D']['value'] != self.subtitle_block['D-REV']['value']:
            self.error_drawing.ed11['boolean_value'] = True
        
        # Verifica se a data da revisão atual do desenho condiz com a Date de Emissão do Usuário, Padrão: Data de Hoje
        if self.revision_blocks[int(self.file_drawing_code_separate[5])]['REV-D']['value'] != self.data_issue:
            self.error_drawing.ed13['boolean_value'] = True
            self.error_drawing.ed13['description'] += self.data_issue

    # Função para verficar Blocos de Peças
    def check_part_block(self):
        for part_block in self.part_blocks:
            # Verifica se o Peso está com vírgula
            if ',' in part_block["PESO-CAD"]['value'] or ',' in part_block["TOTALE"]['value']:
                self.error_drawing.ed15['boolean_value'] = True

            # Verifica se a descrição está com vírgula
            if ',' in part_block['DESCRIZIONE-IN-R1']['value']:
                self.error_drawing.ed17['boolean_value'] = True

            # Verifica se a multiplicação do peso bate
            part_qty = float(part_block["QUANTITA'"]['value'])
            part_weight = float(part_block["PESO-CAD"]['value'].replace(',', '.'))
            part_total_weight = float(part_block["TOTALE"]['value'].replace(',', '.'))
            
            if abs(part_qty * part_weight - part_total_weight) > 0.0001:
                self.error_drawing.ed16['boolean_value'] = True

            # Verifica se o Atributo MARCA do Blocos de Peças está com Fator de Largura de 0.7
            print(part_block['MARCA']['width_factor'])
            if abs(part_block['MARCA']['width_factor'] - 0.7) > 0.0001:
                self.error_drawing.ed19['boolean_value'] = True

    # Função para verificar o LTScale
    def check_line_scale_factor(self):
        ltscale = self.doc_dxf.header['$LTSCALE']

        if abs(self.subtitle_block['x_scale']/2 - ltscale) > 0.0001  :
            self.error_drawing.ed06['boolean_value'] = True

    # Função para verificar as linhas de chamadas
    def check_leader(self):
        for leader in self.msp_dxf.query('LEADER'):
            if leader.dxf.layer != 'QUOTE':
                self.error_drawing.ed08['boolean_value'] = True
                return

    # Função para verificar as Notas
    def check_notes(self):
        for entity in self.msp_dxf:
            # Verifica se a nota de marcação está correta
            if entity.dxftype() == 'TEXT' and '/...' in entity.dxf.text :
                indentify_mark = f"{self.file_drawing_code_separate[2]}-{self.file_drawing_code_separate[3]}-{self.file_drawing_code_separate[4]}/..."
                if(entity.dxf.text != indentify_mark) :
                    self.error_drawing.ed18['boolean_value'] = True
                    self.error_drawing.ed18['description'] += f' Correto: {indentify_mark}'

    # Função para verificar se um bloco existe no Desenho
    def _checkBlockExists(self, blockName):
        block = self.doc_dxf.blocks.get(blockName)

        if block is not None:
            return True
    
    # Função adicionar nome do Bloco e Descrição no Error EDOB
    def _concat_blockname_error(self, block_name, description):
        self.error_drawing.edOB['boolean_value'] = True
        self.error_drawing.edOB['description'] += f'\t\t{block_name} - {description}\n'

    # Função para verificar os blocos que estão no R16
    def check_block_in_R16(self):
        blocks_to_check = [
            ('TABELLA COPPIE SERRAGGIO - METRICO', 'Tabela de Torque do Parafuso'),
            ('PARTICOLARE-GUARNIZIONE', 'Bloco de Junta'),
            ('MARCA', 'Bloco Indicação Peça'),
            ('LIVELLO-ALZATO', 'Bloco de Nível'),
            ('LIVELLO-PIANTA', 'Bloco de Nível para Superficie'),
            ('TIPICO-SALDATURA_FLANGE-L', 'Bloco de Solda para Flange Livre'),
            ('TIPICO-SALDATURA_FLANGE-PIANE', 'Bloco de Solda com Flange Fixo'),
            ('EMB_LISTA_DE_MATERIAL', 'Bloco de Material'),
            ('EMB_LISTA_DE_MATERIAL_INFO_ING', 'Bloco de Material das Informações'),
            ('EMB_LISTA_DE_MATERIAL_DESCRITIVO_ING', 'Bloco de Material das Descrições'),
            ('EMB_LISTA_DE_MATERIAL_INFO', 'Bloco de Material das Informações'),
            ('EMB_LISTA_DE_MATERIAL_DESCRITIVO', 'Bloco de Material das Descrições')
        ]

        for block in blocks_to_check:
            if self._checkBlockExists(block[0]):
                self._concat_blockname_error(block[0], block[1])

        # Verificação de Blocos de Solda
        if self._checkBlockExists('TIPICO-SALDATURA_ENG-POR') or \
            self._checkBlockExists('TIPICO-SALDATURA_ITA-ENG'): 
                self.error_drawing.edOB['boolean_value'] = True
                self.error_drawing.edOB['description'] += '\t\tTIPICO-SALDATURA - Bloco de Solda\n'

        # Verificação de Blocos do Formato
        if self._checkBlockExists('REDE-A0') or \
            self._checkBlockExists('REDE-A1') or \
            self._checkBlockExists('REDE-A2') or \
            self._checkBlockExists('REDE-A3'):
                self.error_drawing.edOB['boolean_value'] = True
                self.error_drawing.edOB['description'] += '\t\tREDE - Bloco de folha\n'
            
        # Verificação do Bloco de Junta
        if self._checkBlockExists('REDECAM-GUARNIZIONI_monolingua'):
            block = self.doc_dxf.blocks.get('REDECAM-GUARNIZIONI_monolingua')

            # Acessa as entidades dentro do bloco e procure um Texto escrito m (Metro)
            for entity in block:
                if entity.dxftype() == 'TEXT' and entity.dxf.text == 'm':
                    return
            
            # Caso não tenha informa que o Bloco está na Versão antiga
            self.error_drawing.edOB['boolean_value'] = True
            self.error_drawing.edOB['description'] += '\t\tREDECAM-GUARNIZIONI - Bloco de Junta\n'

    # Função para verificar se a Layer Existe
    def check_layer_in_R16(self):
        if "CONTOUR EXI" in self.doc_dxf.layers:
            self.error_drawing.ed07['boolean_value'] = True