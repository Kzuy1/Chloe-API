from Verify_Drawing_Redecam.ErrorDrawing import ErrorDrawing
from Verify_Drawing_Redecam.Layer import LayerList
from Verify_Drawing_Redecam.Blocks import BlockList, Entity, BlockScaleError
from Verify_Drawing_Redecam.OldLayers import old_layers
from utils.file_utils import save_in_temp_folder, convert_file
from ezdxf.entities.dimstyleoverride import DimStyleOverride
from datetime import datetime
import ezdxf
import os
import re
import math

class Drawing:
    def __init__(self, file, data_issue = None):
        self.error_drawing = ErrorDrawing()
        self.data_issue = data_issue
        self.full_path = save_in_temp_folder(file, __file__)
        self.convert_to_dxt()
        self.file_drawing_code = self.get_drawing_code()
        self.file_drawing_code_separate = self.get_drawing_code_separate()
        self.layer_list = LayerList()
        self.layer_list.add_default_layer()
        self.doc_dxf = ezdxf.readfile(self.full_path)
        self.msp_dxf = self.doc_dxf.modelspace()
        self.subtitle_block = self.get_block_info('REDECAM_TITLE-BLOCK')
        self.revision_blocks = self.get_block_info('REDE-DISTINTA-REVISIONE')
        self.revision_blocks = self.sort_block(self.revision_blocks, 'REV-N')
        # self.part_blocks = self.get_block_info('SATUS_LISTA-PECAS')
        self.format_block = self.get_block_info('REDE-A0', 'REDECAM_A1','REDECAM_A3')
        
        if self.has_multiple_blocks():
            self.message = self.error_drawing.get_error_messages()
            return

        self.check_layer_properties()
        self.check_data_issue()
        self.check_correct_separation()
        self.check_subtitle_block()
        self.check_revision_block()
        # self.check_part_block()
        self.check_line_scale_factor()
        self.check_leader()
        # self.check_dimensions_indicate()
        self.check_format_block_at_origin()
        self.check_dimension_step()
        # # # self.check_version_blocks()
        self.check_older_layers()
        # self.check_blocks_scale()

        self.message = self.error_drawing.get_error_messages()
    
    def has_multiple_blocks(self) -> bool:
        if len(self.subtitle_block) != 1:
            self.error_drawing.er09['boolean_value'] = True
            self.error_drawing.er09['description'] += '\nBloco de Legenda'
        
        if len(self.format_block) != 1:
            self.error_drawing.er09['boolean_value'] = True
            self.error_drawing.er09['description'] += '\nBloco de Formato'
        
        if self.error_drawing.er09['boolean_value'] == False:
            self.subtitle_block = self.subtitle_block[0]
            self.format_block = self.format_block[0]
        
        return self.error_drawing.er09['boolean_value']
    
    # Função para converter o arquivo
    def convert_to_dxt(self):
        ext = os.path.splitext(self.full_path)[1].lower()

        if ext == ".dwg":
            self.full_path = convert_file(
                self.full_path,
                output_extension="dxf",
                cad_version="ACAD2010"
            )

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
                    self.error_drawing.er14['boolean_value'] = True
                    return

    # Função para verificar se está separado certo o codigo
    def check_correct_separation(self):
        regex_code = r'^[A-Z0-9]{7}(\.[0-9]+)?(-[A-Z0-9-]+)?_[A-Z]{3}-[0-9]{3}_[0-9]{2}$'

        if not re.match(regex_code, self.file_drawing_code):
            self.error_drawing.er01['boolean_value'] = True

    # Função para verificar as informações do Bloco de Título do Desenho
    def check_subtitle_block(self):
        if not self.error_drawing.er01['boolean_value']:
            if self.subtitle_block['FROM-DWG']['value'] + '_' + self.subtitle_block['REV']['value'] != self.file_drawing_code:
                self.error_drawing.er02['boolean_value'] = True
            
            if self.subtitle_block['COMBOFIELD1']['value'] + '_' + self.subtitle_block['DOC']['value'] + '-' + self.subtitle_block['NUM']['value'] != self.subtitle_block['FROM-DWG']['value']:
                self.error_drawing.er02['boolean_value'] = True

            join_combofield = self.subtitle_block['PRN']['value'] + self.subtitle_block['LIN']['value']
            if self.subtitle_block['ITESIN']['value']:
                join_combofield += '-' + self.subtitle_block['ITESIN']['value']
            if join_combofield != self.subtitle_block['COMBOFIELD1']['value']:
                self.error_drawing.er02['boolean_value'] = True

            join_itemsin = self.subtitle_block['ITE']['value']
            if self.subtitle_block['SIN']['value']:
                join_itemsin += '-' + self.subtitle_block['SIN']['value']
            if join_itemsin != self.subtitle_block['ITESIN']['value']:
                self.error_drawing.er02['boolean_value'] = True

        # Verifica se a escala condiz com o que está escrito
        scale_subtitle = self.subtitle_block['SCA']['value']
        if scale_subtitle in ('', "1:XX") or abs(float(scale_subtitle.replace("1:", "")) - self.subtitle_block['x_scale']) > 0.0001:
            self.error_drawing.er03['boolean_value'] = True

    # Função para verificar Escala dos Blocos de Revisão
    def check_revision_block(self):
        # Verifica se existe bloco de revisão correspondente a quantidade de revisões
        if len(self.revision_blocks) < int(self.file_drawing_code_separate[-1]) + 1:
            self.error_drawing.er12['boolean_value'] = True
            return

        # Verifica Bloco de Revisão até última Revisão se está Preenchido
        current_review_block = self.revision_blocks[int(self.file_drawing_code_separate[-1])]
        for attribs in current_review_block.values():
            if isinstance(attribs, dict) and attribs['value'] == '':
                self.error_drawing.er12['boolean_value'] = True
                return

        # Verifica se a data Bloco de Revisão 0 é o mesmo no Bloco de Legenda da Data de Emissão
        if self.revision_blocks[0]['REV-D']['value'] != self.subtitle_block['DAT']['value']:
            self.error_drawing.er10['boolean_value'] = True

        # Verifica se a data Bloco de Revisão N é o mesmo no Bloco de Legenda da Data de Revisão
        if self.revision_blocks[int(self.file_drawing_code_separate[-1])]['REV-D']['value'] != self.subtitle_block['D-REV']['value']:
            self.error_drawing.er11['boolean_value'] = True
        
        # Verifica se a data da revisão atual do desenho condiz com a Date de Emissão do Usuário, Padrão: Data de Hoje
        if self.revision_blocks[int(self.file_drawing_code_separate[-1])]['REV-D']['value'] != self.data_issue:
            self.error_drawing.er13['boolean_value'] = True
            self.error_drawing.er13['description'] += self.data_issue

        # Verificar a revisão de pares está atribuída em 'EMB' e 'VOL'
        if self.revision_blocks[int(self.file_drawing_code_separate[-1])]['MOD']['value'].strip().upper() != 'EMB' or \
           self.revision_blocks[int(self.file_drawing_code_separate[-1])]['APP']['value'].strip().upper() != 'VOL':
            self.error_drawing.er04['boolean_value'] = True

        # Verificar se revisão de pares do Bloco 0 está igual ao Bloco de Título
        if any([
            self.revision_blocks[0]['MOD']['value'] != self.subtitle_block['DRA']['value'],
            self.revision_blocks[0]['APP']['value'] != self.subtitle_block['CON']['value'],
        ]):
            self.error_drawing.er05['boolean_value'] = True
        
        # Verifica se o Aprovado do Bloco de Legenda está em branco
        if self.subtitle_block['APP']['value'] != '':
            self.error_drawing.er17['boolean_value'] = True

    # Função para verficar Blocos de Peças
    def check_part_block(self):
        sum_weight = 0
        sum_weight_withou_rock = 0

        for part_block in self.part_blocks:
            # Verifica se o Peso está com Ponto
            if '.' in part_block["PESO_UNIT."]['value'] or '.' in part_block["PESO_TOTAL"]['value']:
                self.error_drawing.er15['boolean_value'] = True

            # Verifica se a multiplicação do peso bate
            part_qty = float(part_block["QTDE."]['value'])
            part_weight = float(part_block["PESO_UNIT."]['value'].replace(',', '.'))
            part_total_weight = float(part_block["PESO_TOTAL"]['value'].replace(',', '.'))
            
            if abs(part_qty * part_weight - part_total_weight) > 0.0001:
                self.error_drawing.er16['boolean_value'] = True

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
                    self.error_drawing.er20['boolean_value'] = True
                    self.error_drawing.er20['description'] += f"{round(compare_weight)} kg"
                    break

    # Função para verificar o LTScale
    def check_line_scale_factor(self):
        ltscale = self.doc_dxf.header['$LTSCALE']

        if abs(self.subtitle_block['x_scale']/2 - ltscale) > 0.0001  :
            self.error_drawing.er06['boolean_value'] = True

    # Função para verificar as linhas de chamadas
    def check_leader(self):
        for leader in self.msp_dxf.query('LEADER'):
            if leader.dxf.layer != 'QUOTE':
                self.error_drawing.er08['boolean_value'] = True
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
                self.error_drawing.er21['boolean_value'] = True
                self.error_drawing.er21['description'] += f'\t\t\t{dim_name}\n'

            # Verifica se a Escala da Cota está no padrão do formato
            if  abs(self.subtitle_block['x_scale'] - dim_style.dxf.dimscale) > 0.0001:
                self.error_drawing.er22['boolean_value'] = True
                self.error_drawing.er22['description'] += f'\t\t\t{dim_name}\n'

            # Verifica o fator de Escada da Cota está correto
            scale_factor = round(dim_style.dxf.dimlfac * self.subtitle_block['x_scale'], 1)
            scale_factor = re.sub(r'\b(\d+)\.0\b', r'\1', str(scale_factor))
            if scale_factor not in dim_style.dxf.name:
                self.error_drawing.er23['boolean_value'] = True
                self.error_drawing.er23['description'] += f'\t\t\t{dim_name}\n'

    def check_format_block_at_origin(self):
        if (
            self.format_block['x_position'],
            self.format_block['y_position'],
            self.format_block['z_position'],
        ) != (0, 0, 0): 
            self.error_drawing.er24['boolean_value'] = True

    def _get_dimension_suffix(self, dim):
        if dim.dxf.text:
            return dim.dxf.text
        
        override = DimStyleOverride(dim)
        dimpost = override.get('dimpost')
        if dimpost:
            return dimpost

    def check_dimension_step(self):
        pattern = re.compile(
            r'\(\s*([\d.,]+)\s*[xX]\s*([\d.,]+)\s*\)',
            re.IGNORECASE
        )

        for dim in self.msp_dxf.query("DIMENSION"):
            dim_text = self._get_dimension_suffix(dim)
        
            if not dim_text:
                continue
            match = pattern.search(dim_text)

            if not match:
                continue

            qty = float(match.group(1).replace(',', '.'))
            step = float(match.group(2).replace(',', '.'))

            result = qty * step
            measured = dim.dxf.actual_measurement
            tolerance = 1.15

            if abs(result - measured) > tolerance:
                self.error_drawing.er25['boolean_value'] = True
                return
    
    # Função para verificar escala dos blocos
    def validate_block_insert(self, insert, block):
        x_scale = insert.dxf.xscale
        y_scale = insert.dxf.yscale
        z_scale = insert.dxf.zscale
        rotation = insert.dxf.rotation % 360

        allowed_rotation_for_mirrored = 0.0
        tolerance = 0.001
        if not block.allow_mirrored and (x_scale < 0 or y_scale < 0 or not math.isclose(rotation, allowed_rotation_for_mirrored, abs_tol=tolerance)):
            return BlockScaleError.MIRRORED
        
        if not any(math.isclose(z_scale, s * self.subtitle_block['z_scale'], abs_tol=tolerance) for s in block.allowed_scales):
            return BlockScaleError.SCALED

        if block.allowed_rotations and not any(math.isclose(rotation, r, abs_tol=tolerance) for r in block.allowed_rotations):
            return BlockScaleError.ROTATED
        
    # Função para procurar blocos
    def check_blocks_scale(self):
        blocks_to_check = BlockList()
        blocks_checked = set()
        blocks_to_check.add_list_blocks_check_scale()
        blocks_index = {block.name: block for block in blocks_to_check.blocks}

        for insert in self.msp_dxf.query("INSERT"):
            block_name = insert.dxf.name
            block = blocks_index.get(block_name)

            if not block or block_name in blocks_checked:
                continue
            
            error = self.validate_block_insert(insert, block)

            if error is None:
                continue

            print(error)

            blocks_checked.add(block_name)

            if error == BlockScaleError.MIRRORED:
                self._concat_block_error(self.error_drawing.er26, block.name, block.description, "Bloco espelhado")

            if error == BlockScaleError.SCALED:
                self._concat_block_error(self.error_drawing.er26, block.name, block.description, "Escala incorreta")

            if error == BlockScaleError.ROTATED:
                self._concat_block_error(self.error_drawing.er26, block.name, block.description, "Rotação incorreta")

    # Função para verificar se um bloco existe no Desenho
    # def _checkBlockExists(self, blockName):
    #     block = self.doc_dxf.blocks.get(blockName)

    # Função adicionar nome do Bloco e Descrição no Error
    def _concat_block_error(self, error: dict, block_name: str, block_description: str, error_description: str):
        error['boolean_value'] = True
        error['description'] += f'\t\t\t{block_name} - {block_description} - {error_description}\n'
    #     if block is not None:
    #         return True
    

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
                self.error_drawing.er07['boolean_value'] = True
                self.error_drawing.er07['description'] += f'\t\t\t{layer_name}\n'