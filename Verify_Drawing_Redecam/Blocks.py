from ezdxf.enums import ACI
from enum import Enum

class Entity:
    def __init__(self, dxftype, layer = None, color = None, attdef_tag = None, text_value = None):
        self.dxftype = dxftype
        self.layer = layer
        self.color = color
        self.attdef_tag = attdef_tag
        self.text_value = text_value

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

    def add_list_old_blocks_check_by_name(self): 
        self.add_block('TABELLA COPPIE SERRAGGIO - METRICO', 'Tabela de Torque do Parafuso')
        self.add_block('PARTICOLARE-GUARNIZIONE', 'Bloco de Junta')
        self.add_block('MARCA', 'Bloco Indicação Peça')
        self.add_block('LIVELLO-ALZATO', 'Bloco de Nível')
        self.add_block('LIVELLO-PIANTA', 'Bloco de Nível para Superficie')
        self.add_block('TIPICO-SALDATURA_FLANGE-L', 'Bloco de Solda para Flange Livre')
        self.add_block('TIPICO-SALDATURA_FLANGE-PIANE', 'Bloco de Solda com Flange Fixo')
        self.add_block('EMB_LISTA_DE_MATERIAL', 'Bloco de Material')
        self.add_block('EMB_LISTA_DE_MATERIAL_INFO_ING', 'Bloco de Material das Informações')
        self.add_block('EMB_LISTA_DE_MATERIAL_DESCRITIVO_ING', 'Bloco de Material das Descrições')
        self.add_block('EMB_LISTA_DE_MATERIAL_INFO', 'Bloco de Material das Informações')
        self.add_block('EMB_LISTA_DE_MATERIAL_DESCRITIVO', 'Bloco de Material das Descrições')
        self.add_block('TIPICO-SALDATURA_ENG-POR', 'Bloco de Solda')
        self.add_block('TIPICO-SALDATURA_ITA-ENG', 'Bloco de Solda')
        self.add_block('REDE-A1', 'Bloco de folha')
        self.add_block('REDE-A2', 'Bloco de folha')
        self.add_block('REDE-A3', 'Bloco de folha')
        self.add_block('REDECAM_REVISION', 'Bloco de Revisão')
        self.add_block('REDECAM-BULLONERIA', 'Bloco de Parafuso')
        self.add_block('REDECAM-BULLONERIA_monolingua', 'Bloco de Parafuso')
        self.add_block('REDECAM-DISTINTA', 'Bloco de Peça')
        self.add_block('REDECAM-DISTINTA_monolingua', 'Bloco de Peça')
        self.add_block('REDECAM-GUARNIZIONI', 'Bloco de Junta')
        self.add_block('REDECAM-GUARNIZIONI_monolingua', 'Bloco de Junta')
        self.add_block('REDECAM-TITOLO-TAVOLA', 'Bloco de Título')
        self.add_block('REDECAM-TITOLO-TAVOLA_ELE+PRO', 'Bloco de Título')
        self.add_block('EMB_LISTA_DE_MATERIAL_v0.2', 'Bloco de Material')
        self.add_block('EMB_LISTA_DE_MATERIAL_INFO_ING_v0.2', 'Bloco de Material das Informações')
        self.add_block('EMB_LISTA_DE_MATERIAL_DESCRITIVO_ING_v0.2', 'Bloco de Material das Descrições')
        self.add_block('EMB_LISTA_DE_MATERIAL_INFO_v0.2', 'Bloco de Material das Informações')
        self.add_block('EMB_LISTA_DE_MATERIAL_DESCRITIVO_v0.2', 'Bloco de Material das Descrições')

    def add_list_old_blocks_check_by_entity(self):
        self.add_block(name='GASKET INSTALLATION', description='Bloco de Instalação de Junta', entity=Entity(dxftype='TEXT', layer='TESTI', text_value='KEEP IT IN POSITION WITH H.T. SILICON'))
        self.add_block(name='INDEX_STEELWORK', description='Index do Bloco de Peça', entity=Entity(dxftype='TEXT', layer='REDECAM_STEELWORK', text_value='STEELWORK ITEM'))
        self.add_block(name='MARK', description='Bloco de Indicação de Peça', entity=Entity(dxftype='WIPEOUT', color=250))
        self.add_block(name='POS', description='Bloco de Indicação de Peça', entity=Entity(dxftype='WIPEOUT', color=250))
        self.add_block(name='POS2', description='Bloco de Indicação de Peça', entity=Entity(dxftype='WIPEOUT', color=250))
        self.add_block(name='PRELIMINARY_BIG', description='Bloco de Carimbo Grande', entity=Entity(dxftype='LWPOLYLINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='PRELIMINARY_SMALL', description='Bloco de Carimbo Grande', entity=Entity(dxftype='LWPOLYLINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDECAM_TITLE-BLOCK', description='Bloco de Título', entity=Entity(dxftype='INSERT', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDECAM_STEELWORK', description='Bloco de Peça', entity=Entity(dxftype='ATTDEF', layer='REDECAM_STEELWORK', attdef_tag='RM'))
        self.add_block(name='REV', description='Bloco de Indicação de Peça', entity=Entity(dxftype='WIPEOUT', color=250))
        
    # def add_list_blocks_check_scale(self):
        # self.add_block(name='', description='', allowed_scales=[1.0], allow_mirrored=False)





        