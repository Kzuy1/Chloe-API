from ezdxf.enums import ACI
from enum import Enum

class Entity:
    def __init__(self, dxftype, layer = None, color = None, attdef_tag = None, text_value = None, text_style = None):
        self.dxftype = dxftype
        self.layer = layer
        self.color = color
        self.attdef_tag = attdef_tag
        self.text_value = text_value
        self.text_style = text_style

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
        self.add_block(name='10315775', description='Bloco de Planicidade', entity=Entity(dxftype='TEXT', text_value='4', text_style='ROMAND'))
        self.add_block(name='10315974', description='Bloco de Planicidade', entity=Entity(dxftype='TEXT', text_value='2', text_style='ROMAND'))
        self.add_block(name='15060899', description='Bloco de Informações da Junta de Expansão', entity=Entity(dxftype='ELLIPSE', layer='CONTORNI'))  
        self.add_block(name='GASKET INSTALLATION', description='Bloco de Instalação de Junta', entity=Entity(dxftype='TEXT', layer='TESTI', text_value='KEEP IT IN POSITION WITH H.T. SILICON'))
        self.add_block(name='INDEX_STEELWORK', description='Index do Bloco de Peça', entity=Entity(dxftype='TEXT', layer='REDECAM_STEELWORK', text_value='STEELWORK ITEM'))
        self.add_block(name='MARK', description='Bloco de Indicação de Peça', entity=Entity(dxftype='WIPEOUT', color=250))
        self.add_block(name='POS', description='Bloco de Indicação', entity=Entity(dxftype='WIPEOUT', color=250))
        self.add_block(name='POS2', description='Bloco de Indicação', entity=Entity(dxftype='WIPEOUT', color=250))
        self.add_block(name='PRELIMINARY_BIG', description='Bloco de Carimbo Grande', entity=Entity(dxftype='LWPOLYLINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='PRELIMINARY_SMALL', description='Bloco de Carimbo Pequeno', entity=Entity(dxftype='LWPOLYLINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDE-A0', description='Bloco de Folha', entity=Entity(dxftype='LWPOLYLINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDE-DISTINTA-REVISIONE', description='Bloco de Revisão', entity=Entity(dxftype='LINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDECAM_A1', description='Bloco de Folha', entity=Entity(dxftype='LWPOLYLINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDECAM_A2', description='Bloco de Folha', entity=Entity(dxftype='LWPOLYLINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDECAM_A3', description='Bloco de Folha', entity=Entity(dxftype='LWPOLYLINE', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDECAM_FASTENERS', description='Bloco de Parafuso', entity=Entity(dxftype='ATTDEF', layer='REDECAM_FASTENER', color=ACI.CYAN, attdef_tag='MOU'))
        self.add_block(name='REDECAM_FITTINGS+OTHERS', description='Bloco de Acessórios', entity=Entity(dxftype='ATTDEF', layer='REDECAM_FITTING+OTHERS', color=ACI.CYAN, attdef_tag='MOU'))
        self.add_block(name='REDECAM_GASKET', description='Bloco de Junta', entity=Entity(dxftype='ATTDEF', layer='REDECAM_GASKET', color=ACI.CYAN, attdef_tag='MOU'))
        self.add_block(name='REDECAM_RAW+INSULATION', description='Bloco de Isolamento', entity=Entity(dxftype='ATTDEF', layer='REDECAM_RAW+INSULATION', color=ACI.CYAN, attdef_tag='MOU'))
        self.add_block(name='REDECAM_TITLE-BLOCK', description='Bloco de Título', entity=Entity(dxftype='INSERT', layer='REDECAM_TITLE-BLOCK'))
        self.add_block(name='REDECAM_STEELWORK', description='Bloco de Peça', entity=Entity(dxftype='ATTDEF', layer='REDECAM_STEELWORK', attdef_tag='RM'))
        self.add_block(name='REV', description='Bloco de Indicação de Revisão', entity=Entity(dxftype='WIPEOUT', color=250))
        self.add_block(name='WELDINGS_ENG-ESP', description='Bloco de Solda', entity=Entity(dxftype='TEXT', layer='0', text_value='PERFORM CONTINUOUS WELDING, UNLESS OTHERWISE INDICATED'))
        self.add_block(name='WELDINGS_ENG-FRA', description='Bloco de Solda', entity=Entity(dxftype='TEXT', layer='0', text_value='PERFORM CONTINUOUS WELDING, UNLESS OTHERWISE INDICATED'))
        self.add_block(name='WELDINGS_ENG-ITA', description='Bloco de Solda', entity=Entity(dxftype='TEXT', layer='0', text_value='PERFORM CONTINUOUS WELDING, UNLESS OTHERWISE INDICATED'))
        self.add_block(name='WELDINGS_ENG-POR', description='Bloco de Solda', entity=Entity(dxftype='TEXT', layer='0', text_value='PERFORM CONTINUOUS WELDING, UNLESS OTHERWISE INDICATED'))
        self.add_block(name='WELDINGS_ENG-RUS', description='Bloco de Solda', entity=Entity(dxftype='TEXT', layer='0', text_value='PERFORM CONTINUOUS WELDING, UNLESS OTHERWISE INDICATED'))
        self.add_block(name='WELDING_FIX-FLANGE', description='Bloco de Solda para Flange Fixa', entity=Entity(dxftype='LINE', layer='NASCOSTE'))
        self.add_block(name='WELDING_FREE-FLANGES', description='Bloco de Solda para Flange Livre', entity=Entity(dxftype='LINE', layer='NASCOSTE'))
        
        # Block in Template PRO FILE 01A, but dont have older version. Reminder to Check in new versions template.
        # 12175727
        # 17154301
        # BOM
        # CENTER-LINE
        # DIAMOND SHEET
        # ELEVATION - PLAN
        # ELEVATION - PLAN_USA
        # ELEVATION - VIEW
        # ELEVATION - VIEW_USA
        # EXPANDED MESH
        # INDEX_BOM
        # RESACRYL INSTALLATION
        # TEARDROP SHEET
        # TOP_BOM
        # TORQUE TABLE

    def add_list_blocks_check_scale(self):
        self.add_block(name='SIMBOLO-SOLDA-AO-REDOR', description='Bloco de Símbolo de Solda ao Redor', allowed_scales=[1.0], allow_mirrored=True)
        self.add_block(name='SIMBOLO-SOLDA-EM-CAMPO', description='Bloco de Símbolo de Solda em Campo', allowed_scales=[1.0], allowed_rotations=[0.0], allow_mirrored=True)
        self.add_block(name='SIMBOLO-SOLDA-EM-MEIO-V', description='Bloco de Símbolo de Solda em Meio V', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-MEIO-V-PLANA', description='Bloco de Símbolo de Solda em Meio V Plana', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V', description='Bloco de Símbolo de Solda em V', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V-CONVEXA', description='Bloco de Símbolo de Solda em V Convexa', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V-CONVEXA-DESCONTINUA', description='Bloco de Símbolo de Solda em V Convexa Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V-CONVEXA-DOS-DOIS-LADOS', description='Bloco de Símbolo de Solda em V Convexa dos Dois Lados', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V-DOS-DOIS-LADOS', description='Bloco de Símbolo de Solda em V dos Dois Lados', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-EM-V-PLANA', description='Bloco de Símbolo de Solda em V Plana', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE', description='Bloco de Símbolo de Solda de Filete', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA', description='Bloco de Símbolo de Solda de Filete com Perna', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA-DESCONTINUA', description='Bloco de Símbolo de Solda de Filete com Perna Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA-DESCONTINUA-COINCIDENTE', description='Bloco de Símbolo de Solda de Filete com Perna Descontínua Coincidente', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-COM-PERNA-DOS-DOIS-LADOS', description='Bloco de Símbolo de Solda de Filete com Perna dos Dois Lados', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-DESCONTINUA', description='Bloco de Símbolo de Solda de Filete Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-DESCONTINUA-COINCIDENTE', description='Bloco de Símbolo de Solda de Filete Descontínua Coincidente', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-DESCONTINUA-INTERCALADA', description='Bloco de Símbolo de Solda de Filete Descontínua Intercalada', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-FILETE-DOS-DOIS-LADOS', description='Bloco de Símbolo de Solda de Filete dos Dois Lados', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-CONVEXA', description='Bloco de Símbolo de Solda Reta Convexa', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-CONVEXA-DESCONTINUA', description='Bloco de Símbolo de Solda Reta Convexa Descontínua', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-CONVEXA-DOS-DOIS-LADOS', description='Bloco de Símbolo de Solda Reta Convexa dos Dois Lados', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-PLANA', description='Bloco de Símbolo de Solda Reta Plana', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='SIMBOLO-SOLDA-RETA-PLANA-DESCONTINUA', description='Bloco de Símbolo de Solda Reta Plana Descontínua', allowed_scales=[1.0], allow_mirrored=False)
    
        self.add_block(name='10315775', description='Bloco de Planicidade', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='10315974', description='Bloco de Planicidade', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='12175727', description='Bloco de Indicação de Corte', allowed_scales=[1.0], allow_mirrored=True)
        self.add_block(name='15060899', description='Bloco de Informações da Junta de Expansão', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='17154301', description='Bloco de Esquema de Carga', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='BOM', description='Bloco de Lista de Material', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='CENTER-LINE', description='Bloco de Linha de Centro', allowed_scales=[1.0], allowed_rotations=[0.0, 90.0, 270.0], allow_mirrored=True)
        self.add_block(name='DIAMOND SHEET', description='Bloco de Chapa Diamante', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='ELEVATION - PLAN', description='Bloco de Elevação', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='ELEVATION - PLAN_USA', description='Bloco de Elevação', allowed_scales=[1.0], allowed_rotations=[0.0, 180.0], allow_mirrored=True)
        self.add_block(name='ELEVATION - VIEW', description='Bloco de Elevação', allowed_scales=[1.0], allowed_rotations=[0.0, 180.0], allow_mirrored=True)
        self.add_block(name='ELEVATION - VIEW_USA', description='Bloco de Elevação', allowed_scales=[1.0], allowed_rotations=[0.0], allow_mirrored=True)
        self.add_block(name='EXPANDED MESH', description='Bloco de Chapa Expandida', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='GASKET INSTALLATION', description='Bloco de Instalação de Junta', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='INDEX_BOM', description='Index do Bloco de BOM', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='INDEX_STEELWORK', description='Index do Bloco de Peça', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='MARK', description='Bloco de Indicação de Peça', allowed_scales=[0.8, 1.0], allow_mirrored=True)
        self.add_block(name='POS', description='Bloco de Indicação de Posição', allowed_scales=[0.8, 1.0], allowed_rotations=[0.0], allow_mirrored=True)
        self.add_block(name='POS2', description='Bloco de Indicação de Posição', allowed_scales=[0.8, 1.0], allowed_rotations=[0.0], allow_mirrored=True)
        self.add_block(name='PRELIMINARY_BIG', description='Bloco de Carimbo Grande', allowed_scales=[1.0], allow_mirrored=True)
        self.add_block(name='PRELIMINARY_SMALL', description='Bloco de Carimbo Pequeno', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDE-A0', description='Bloco de Folha', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDE-DISTINTA-REVISIONE', description='Bloco de Revisão', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_A1', description='Bloco de Folha', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_A2', description='Bloco de Folha', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_A3', description='Bloco de Folha', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_FASTENERS', description='Bloco de Parafuso', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_FITTINGS+OTHERS', description='Bloco de Acessórios', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_GASKET', description='Bloco de Junta', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_RAW+INSULATION', description='Bloco de Isolamento', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_STEELWORK', description='Bloco de Peça', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REDECAM_TITLE-BLOCK', description='Bloco de Título', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='RESACRYL INSTALLATION', description='Bloco de Instalação de Resacryl', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='REV', description='Bloco de Indicação de Revisão', allowed_scales=[1.0], allowed_rotations=[0.0], allow_mirrored=True)
        self.add_block(name='TEARDROP SHEET', description='Bloco de Chapa Xadrez', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='TOP_BOM', description='Nota do Bloco de BOM', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='TORQUE TABLE', description='Tabela de Torque do Parafuso', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='WELDINGS_ENG-ESP', description='Bloco de Solda', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='WELDINGS_ENG-FRA', description='Bloco de Solda', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='WELDINGS_ENG-ITA', description='Bloco de Solda', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='WELDINGS_ENG-POR', description='Bloco de Solda', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='WELDINGS_ENG-RUS', description='Bloco de Solda', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='WELDING_FIX-FLANGE', description='Bloco de Solda para Flange Fixa', allowed_scales=[1.0], allow_mirrored=False)
        self.add_block(name='WELDING_FREE-FLANGES', description='Bloco de Solda para Flange Livre', allowed_scales=[1.0], allow_mirrored=False)

        # self.add_block(name='', description='', allowed_scales=[1.0], allow_mirrored=False)




        