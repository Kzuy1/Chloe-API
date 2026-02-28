from ezdxf.enums import ACI
from enum import Enum

class Entity:
    def __init__(self, dxftype, layer = None, color = None):
        self.dxftype = dxftype
        self.layer = layer
        self.color = color

class Block():
    def __init__(self, name: str, description: str, entity: Entity = None, allowed_scales: list[float] = None, allowed_rotations: list[float] = None, allow_mirrored: bool = True):
        self.name = name
        self.description = description
        self.entity = entity
        self.allowed_scales = allowed_scales or []
        self.allowed_rotations = allowed_rotations or []
        self.allow_mirrored = allow_mirrored

class BlockScaleError(Enum):
    MIRRORED = "mirrored"
    SCALED = "scaled"
    ROTATED = "rotated"

class BlockList:
    def __init__(self):
        self.blocks = []

    def add_block(self, name: str, description: str, entity: Entity = None, allowed_scales: list[float] = None, allowed_rotations: list[float] = None, allow_mirrored: bool = True):
        self.blocks.append(Block(name, description, entity, allowed_scales, allowed_rotations, allow_mirrored))

    # def add_list_old_blocks_check_by_name(self): 


    # def add_list_old_blocks_check_by_entity(self):

    def add_list_blocks_check_scale(self):
        self.add_block(name='SIMBOLO-SOLDA-AO-REDOR', description='Bloco de Símbolo de Solda ao Redor', allowed_scales=[1.0], allow_mirrored=True)
        self.add_block(name='SIMBOLO-SOLDA-EM-CAMPO', description='Bloco de Símbolo de Solda em Campo', allowed_scales=[1.0], allowed_rotations=[0.0], allow_mirrored=True)
        self.add_block(name='SIMBOLO-SOLDA-FILETE', description='Bloco de Símbolo de Solda de Filete', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-DOS-DOIS-LADOS', description='Bloco de Símbolo de Solda de Filete dos Dois Lados', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-DESCONTINUA', description='Bloco de Símbolo de Solda de Filete Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA-DESCONTINUA-COINCIDENTE', description='Bloco de Símbolo de Solda de Filete com Perna Descontínua Coincidente', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-CONVEXA', description='Bloco de Símbolo de Solda Reta Convexa', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-CONVEXA-DESCONTINUA', description='Bloco de Símbolo de Solda Reta Convexa Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-PLANA', description='Bloco de Símbolo de Solda Reta Plana', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-PLANA-DESCONTINUA', description='Bloco de Símbolo de Solda Reta Plana Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V', description='Bloco de Símbolo de Solda em V', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V-CONVEXA', description='Bloco de Símbolo de Solda em V Convexa', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V-CONVEXA-DESCONTINUA', description='Bloco de Símbolo de Solda em V Convexa Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V-PLANA', description='Bloco de Símbolo de Solda em V Plana', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-MEIO-V', description='Bloco de Símbolo de Solda em Meio V', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-MEIO-V-PLANA', description='Bloco de Símbolo de Solda em Meio V Plana', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA', description='Bloco de Símbolo de Solda de Filete com Perna', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA-DESCONTINUA', description='Bloco de Símbolo de Solda de Filete com Perna Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA-DESCONTINUA-COINCIDENTE', description='Bloco de Símbolo de Solda de Filete com Perna Descontínua Coincidente', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA-DOS-DOIS-LADOS', description='Bloco de Símbolo de Solda de Filete com Perna dos Dois Lados', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-DESCONTINUA-INTERCALADA', description='Bloco de Símbolo de Solda de Filete Descontínua Intercalada', allowed_scales=[1.0], allow_mirrored=False)

        self.add_block(name='SATUS_A1', description='Bloco de Formato A1', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_A2', description='Bloco de Formato A2', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_A3', description='Bloco de Formato A3', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LEGENDA', description='Bloco de Legenda', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_REVISAO-LEGENDA', description='Bloco de Legenda de Revisão', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_REVISAO', description='Bloco de Revisão', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-MATERIAL-DESCRITIVO', description='Bloco de Lista de Material Descritivo', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-MATERIAL', description='Bloco de Lista de Material', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-MATERIAL-NOTA', description='Bloco de Lista de Material Nota', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-PECAS-DESCRITIVO', description='Bloco de Lista de Peças Descritivo', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-PECAS', description='Bloco de Lista de Peças', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-PECAS-NOTA', description='Bloco de Lista de Peças Nota', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-FIXADORES-DESCRITIVO', description='Bloco de Lista de Fixadores Descritivo', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-FIXADORES', description='Bloco de Lista de Fixadores', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-FIXADORES-NOTA', description='Bloco de Lista de Fixadores Nota', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-COMPONENTES-DESCRITIVO', description='Bloco de Lista de Componentes Descritivo', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-COMPONENTES', description='Bloco de Lista de Componentes', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LISTA-COMPONENTES-NOTA', description='Bloco de Lista de Componentes Nota', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_CARIMBO', description='Bloco de Carimbo', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_BLOCO-SOLDAS', description='Bloco de Soldas', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SATUS_LINHA-DE-DIVISAO', description='Bloco de Linha de Divisão', allowed_scales=[1.0], allow_mirrored=False)

        self.add_block(name='SATUS_INDICACAO-REVISAO', description='Bloco de Indicação de Revisão', allowed_scales=[1.0], allowed_rotations=[0.0], allow_mirrored=True)
        self.add_block(name='SATUS_INDICACAO-POS', description='Bloco de Indicação de Posição', allowed_scales=[1.0], allowed_rotations=[0.0], allow_mirrored=True)
        self.add_block(name='SATUS_INDICACAO-NIVEL', description='Bloco de Indicação de Nível', allowed_scales=[1.0], allow_mirrored=True)
        self.add_block(name='SATUS_INDICACAO-TAG', description='Bloco de Indicação de Tag', allowed_scales=[1.0], allow_mirrored=True)
        self.add_block(name='SATUS_CORTE', description='Bloco de Indicação de Corte', allowed_scales=[1.0], allow_mirrored=True)
        self.add_block(name='SATUS_VISTO', description='Bloco de Indicação de Visto', allowed_scales=[1.0], allow_mirrored=True)




        
        # self.add_block(name='', description='', allowed_scales=[1.0], allow_mirrored=False)





        