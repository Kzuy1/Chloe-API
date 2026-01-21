from Verify_Drawing.ErrorDrawing import ErrorDrawing
from Verify_Drawing.Layer import LayerList
from Verify_Drawing.OldBlocks import BlockList, Entity
from Verify_Drawing.OldLayers import old_layers
from utils.file_utils import save_in_temp_folder
from datetime import datetime
from json import load
import ezdxf
import os
import re

class Drawing:
    def __init__(self, file, data_issue = None):
        self.error_drawing = ErrorDrawing()
        self.data_issue = data_issue
        self.full_path = save_in_temp_folder(file, __file__)
        self.file_drawing_code = self.get_drawing_code()
        self.file_drawing_code_separate = self.get_drawing_code_separate()
        self.layer_list = LayerList()
        self.layer_list.add_default_layer()
        self.doc_dxf = ezdxf.readfile(self.full_path)
        self.msp_dxf = self.doc_dxf.modelspace()
        self.subtitle_block = self.get_block_info('SATUS_LEGENDA')
        self.revision_blocks = self.get_block_info('SATUS_REVISAO')
        self.revision_blocks = self.sort_block(self.revision_blocks, 'REV-N')
        self.part_blocks = self.get_block_info('SATUS_LISTA-PECAS')
        self.format_block = self.get_block_info('SATUS_A1', 'SATUS_A3')
        
        if self.has_multiple_blocks():
            self.message = self.error_drawing.get_error_messages()
            return

        self.check_layer_properties()
        self.check_data_issue()
        self.check_correct_separation()
        self.check_subtitle_block()
        self.check_revision_block()
        self.check_part_block()
        self.check_line_scale_factor()
        self.check_leader()
        self.check_dimensions_indicate()
        self.check_format_block_at_origin()
        self.check_dimension_step()
        # # self.check_version_blocks()
        self.check_older_layers()

        self.message = self.error_drawing.get_error_messages()
    
    def has_multiple_blocks(self) -> bool:
        if len(self.subtitle_block) != 1:
            self.error_drawing.ed09['boolean_value'] = True
            self.error_drawing.ed09['description'] += '\nBloco de Legenda'
        
        if len(self.format_block) != 1:
            self.error_drawing.ed09['boolean_value'] = True
            self.error_drawing.ed09['description'] += '\nBloco de Formato'
        
        if self.error_drawing.ed09['boolean_value'] == False:
            self.subtitle_block = self.subtitle_block[0]
            self.format_block = self.format_block[0]
        
        return self.error_drawing.ed09['boolean_value']

    # Função para pegar o código do Desenho
    def get_drawing_code(self):
        drawing_code = os.path.splitext(os.path.basename(self.full_path))[0]
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
    def get_block_info(self, *block_names):
        blocks_list = []

        for block_name in block_names:
            for insert in self.msp_dxf.query(f'INSERT[name=="{block_name}"]'):
                block_info = {}
                
                for attrib in insert.attribs:
                    tag = attrib.dxf.tag
                    value = attrib.dxf.text
                    height = attrib.dxf.height
                    width_factor = attrib.dxf.width

                    block_info[tag] = {'value': value, 'height': height, 'width_factor': width_factor}
                
                block_info['x_scale'] = insert.get_dxf_attrib('xscale') or 1
                block_info['y_scale'] = insert.get_dxf_attrib('yscale') or 1
                block_info['z_scale'] = insert.get_dxf_attrib('zscale') or 1
                
                block_info['x_position'] = insert.dxf.insert[0]
                block_info['y_position'] = insert.dxf.insert[1]
                block_info['z_position'] = insert.dxf.insert[2]

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
            true_color = layer.dxf.true_color
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
                line_weight != default_layer.line_weight or
                true_color is not None):
                    self.error_drawing.ed14['boolean_value'] = True
                    return

    # Função para verificar se está separado certo o codigo
    def check_correct_separation(self):
        regex_code = None

        # REMOVER FLAG EM 28/03/26
        if self.file_drawing_code.startswith("EM"):
            regex_code = r'^[A-Z0-9]{4}-[A-Z0-9]{7}-[0-9]{3}_[0-9]{2}$'
        elif self.file_drawing_code.startswith("STS"):
            regex_code = r'^STS-[A-Z0-9]{7}-[A-Z0-9]{3}-[0-9]{5}_[0-9]{2}$'

        if regex_code is None:
            self.error_drawing.ed01['boolean_value'] = True
            return

        if not re.match(regex_code, self.file_drawing_code):
            self.error_drawing.ed01['boolean_value'] = True

    # Função para verificar as informações do Bloco de Título do Desenho
    def check_subtitle_block(self):
        if not self.error_drawing.ed01['boolean_value']:
            code_value = "-".join(self.file_drawing_code_separate[:-1])
            revision_value = self.file_drawing_code_separate[-1] 

            key_codes = {
                'CODIGO-1': code_value,
                'REVISAO': revision_value
            }

            for key, key_value in key_codes.items():
                if self.subtitle_block[key]['value'] != key_value:
                    self.error_drawing.ed02['boolean_value'] = True
                    break

        # Verifica se a escala condiz com o que está escrito
        scale_subtitle = self.subtitle_block['ESCALA']['value']
        if scale_subtitle in ('', "1:XX") or abs(float(scale_subtitle.replace("1:", "")) - self.subtitle_block['x_scale']) > 0.0001:
            self.error_drawing.ed03['boolean_value'] = True

    # Função para verificar Escala dos Blocos de Revisão
    def check_revision_block(self):
        for revision_block in self.revision_blocks:
            # Verifica Escala do Bloco de Revisão
            if abs(self.subtitle_block['x_scale'] - revision_block['x_scale']) > 0.0001 :
                self.error_drawing.edSC['boolean_value'] = True
                self.error_drawing.edSC['description'] += f'\t\t\tSATUS_REVISAO - Bloco de Revisão {revision_block["REV-N"]["value"]}\n'

        # Verifica se existe bloco de revisão correspondente a quantidade de revisões
        if len(self.revision_blocks) < int(self.file_drawing_code_separate[-1]) + 1:
            self.error_drawing.ed12['boolean_value'] = True
            return

        # Verifica Bloco de Revisão até última Revisão se está Preenchido
        current_review_block = self.revision_blocks[int(self.file_drawing_code_separate[-1])]
        for attribs in current_review_block.values():
            if isinstance(attribs, dict) and attribs['value'] == '':
                self.error_drawing.ed12['boolean_value'] = True
                return

        # Verifica se a data Bloco de Revisão 0 é o mesmo no Bloco de Legenda
        if self.revision_blocks[0]['REV-D']['value'] != self.subtitle_block['DATA']['value']:
            self.error_drawing.ed10['boolean_value'] = True
        
        # Verifica se a data da revisão atual do desenho condiz com a Date de Emissão do Usuário, Padrão: Data de Hoje
        if self.revision_blocks[int(self.file_drawing_code_separate[-1])]['REV-D']['value'] != self.data_issue:
            self.error_drawing.ed13['boolean_value'] = True
            self.error_drawing.ed13['description'] += self.data_issue

        # Verificar a revisão de pares a mesma pessoa está atribuída a mais de um papel na Revisão de Pares
        revision_responsibles = []
        revision_responsibles.append(self.revision_blocks[int(self.file_drawing_code_separate[-1])]['DES.']['value'].strip().upper())
        revision_responsibles.append(self.revision_blocks[int(self.file_drawing_code_separate[-1])]['VERIF.']['value'].strip().upper())
        revision_responsibles.append(self.revision_blocks[int(self.file_drawing_code_separate[-1])]['APROV.']['value'].strip().upper())
        
        if len(revision_responsibles) != len(set(revision_responsibles)):
            self.error_drawing.ed04['boolean_value'] = True

        # Verificar se revisão de pares do Bloco 0 está igual ao Bloco de Título
        if any([
            self.revision_blocks[0]['DES.']['value'] != self.subtitle_block['DES.']['value'],
            self.revision_blocks[0]['VERIF.']['value'] != self.subtitle_block['VERIF.']['value'],
            self.revision_blocks[0]['APROV.']['value'] != self.subtitle_block['APROV.']['value']
        ]):
            self.error_drawing.ed05['boolean_value'] = True

    # Função para verficar Blocos de Peças
    def check_part_block(self):
        sum_weight = 0
        sum_weight_withou_rock = 0

        for part_block in self.part_blocks:
            # Verifica se o Peso está com Ponto
            if '.' in part_block["PESO_UNIT."]['value'] or '.' in part_block["PESO_TOTAL"]['value']:
                self.error_drawing.ed15['boolean_value'] = True

            # Verifica se a multiplicação do peso bate
            part_qty = float(part_block["QTDE."]['value'])
            part_weight = float(part_block["PESO_UNIT."]['value'].replace(',', '.'))
            part_total_weight = float(part_block["PESO_TOTAL"]['value'].replace(',', '.'))
            
            if abs(part_qty * part_weight - part_total_weight) > 0.0001:
                self.error_drawing.ed16['boolean_value'] = True

            # Realiza soma do peso total e soma do peso somente das peças de aço.
            sum_weight += part_total_weight
            if not any(keyword in part_block['DESCRICAO']['value'] for keyword in ['ROCHA', 'ROCK']):
                sum_weight_withou_rock += part_total_weight

        # Verifica se a nota de Peso Total Aprox. está próxima da soma dos pesos dos blocos brancos
        for entity in self.msp_dxf:
            if entity.dxftype() == 'TEXT' and entity.dxf.layer == 'TEXTO' and 'kg' in entity.dxf.text and entity.dxf.color == 2:
                compare_weight = sum_weight

                if any(keyword in entity.dxf.text for keyword in ['STEELWORK', 'AÇO']):
                    compare_weight = sum_weight_withou_rock

                total_weight_approx = re.sub(r'\D', '', entity.dxf.text)

                if abs(round(compare_weight) - float(total_weight_approx)) > 0.1:
                    self.error_drawing.ed20['boolean_value'] = True
                    self.error_drawing.ed20['description'] += f"{round(compare_weight)} kg"
                    break

    # Função para verificar o LTScale
    def check_line_scale_factor(self):
        ltscale = self.doc_dxf.header['$LTSCALE']

        if abs(self.subtitle_block['x_scale']/2 - ltscale) > 0.0001  :
            self.error_drawing.ed06['boolean_value'] = True

    # Função para verificar as linhas de chamadas
    def check_leader(self):
        for leader in self.msp_dxf.query('LEADER'):
            if leader.dxf.layer != 'COTAS':
                self.error_drawing.ed08['boolean_value'] = True
                return
    
    # Função para verificar as especificações da Cotas
    def check_dimensions_indicate(self):
        dim_styles = self.doc_dxf.dimstyles

        for dim_style in dim_styles:
            dim_name = dim_style.dxf.name
            if dim_name == 'Standard':
                continue
            
            # Verifica se o Estilo de Cota está no PorCamada
            if dim_style.dxf.dimclrd != 256 or dim_style.dxf.dimclre != 256:
                self.error_drawing.ed21['boolean_value'] = True
                self.error_drawing.ed21['description'] += f'\t\t\t{dim_name}\n'

            # Verifica se a Escala da Cota está no padrão do formato
            if  abs(self.subtitle_block['x_scale'] - dim_style.dxf.dimscale) > 0.0001:
                self.error_drawing.ed22['boolean_value'] = True
                self.error_drawing.ed22['description'] += f'\t\t\t{dim_name}\n'

            # Verifica o fator de Escada da Cota está correto
            scale_factor = round(dim_style.dxf.dimlfac * self.subtitle_block['x_scale'], 1)
            scale_factor = re.sub(r'\b(\d+)\.0\b', r'\1', str(scale_factor))
            if scale_factor not in dim_style.dxf.name:
                self.error_drawing.ed23['boolean_value'] = True
                self.error_drawing.ed23['description'] += f'\t\t\t{dim_name}\n'

    def check_format_block_at_origin(self):
        if (
            self.format_block['x_position'],
            self.format_block['y_position'],
            self.format_block['z_position'],
        ) != (0, 0, 0): 
            self.error_drawing.ed24['boolean_value'] = True

    def check_dimension_step(self):
        pattern = re.compile(
            r'\<\>\(\s*([\d.,]+)\s*x\s*([\d.,]+)\s*\)',
            re.IGNORECASE
        )

        for dim in self.msp_dxf.query("DIMENSION"):
            dim_text = dim.dxf.text

            if not dim_text:
                continue

            match = pattern.search(dim_text)
            if not match:
                continue

            qty = float(match.group(1).replace(',', '.'))
            step = float(match.group(2).replace(',', '.'))

            result = qty * step
            measured = dim.dxf.actual_measurement

            if abs(result - measured) > 1:
                self.error_drawing.ed25['boolean_value'] = True
                return
                
    # Função para verificar se um bloco existe no Desenho
    # def _checkBlockExists(self, blockName):
    #     block = self.doc_dxf.blocks.get(blockName)

    #     if block is not None:
    #         return True
    
    # # Função adicionar nome do Bloco e Descrição no Error EDOB
    # def _concat_blockname_error(self, block_name, description):
    #     self.error_drawing.edOB['boolean_value'] = True
    #     self.error_drawing.edOB['description'] += f'\t\t\t{block_name} - {description}\n'

    # def inspect_block(self, block_name: str, expected: Entity) -> bool:
    #     block = self.doc_dxf.blocks.get(block_name)
    #     if block is None:
    #         return False

    #     for entity in block:
    #         if entity.dxftype() == expected.dxftype:
    #             if expected.layer is not None and entity.dxf.layer != expected.layer:
    #                 continue
    #             if expected.color is not None and entity.dxf.color != expected.color:
    #                 continue
    #             return True

    #     return False
        
    # Função para verificar as versões dos blocos
    # def check_version_blocks(self):

    #     blocks_to_check_by_entity = BlockList()
    #     blocks_to_check_by_entity.add_list_old_blocks_check_by_entity()

    #     # for block in blocks_to_check:
    #     #     if self._checkBlockExists(block[0]):
    #     #         self._concat_blockname_error(block[0], block[1])

    #     for block in blocks_to_check_by_entity.blocks:
    #         if not self.inspect_block(block.name, block.entity):
    #             print(block.name)
    #             self._concat_blockname_error(block.name, block.description)


    # Função para verificar Layer antigas
    def check_older_layers(self):
        for layer in self.doc_dxf.layers:
            layer_name = layer.dxf.name
            if layer_name in old_layers:
                self.error_drawing.ed07['boolean_value'] = True
                self.error_drawing.ed07['description'] += f'\t\t\t{layer_name}\n'