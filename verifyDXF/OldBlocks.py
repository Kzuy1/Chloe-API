from ezdxf.enums import ACI

class Entity:
    def __init__(self, dxftype, layer = None, color = None):
        self.dxftype = dxftype
        self.layer = layer
        self.color = color

class Block():
    def __init__(self, name, description, entity: Entity = None):
        self.name = name
        self.description = description
        self.entity = entity

class BlockList:
    def __init__(self):
        self.blocks = []

    def add_block(self, name, description, entity: Entity = None):
        self.blocks.append(Block(name, description, entity))

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
        self.add_block('REDE-A0', 'Bloco de folha')
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
        self.add_block('SIMBOLO-SOLDA-FILETE-COM-PERNA-DE-3mm', 'Simbolo Solda Filete com Perna de 3mm')
        self.add_block('SIMBOLO-SOLDA-FILETE-COM-PERNA-DE-3mm-DOS-DOIS-LADOS', 'Simbolo Solda Filete com perna de 3mm dos dois lados')
        self.add_block('SIMBOLO-SOLDA-FILETE-COM-PERNA-DE-3mm-50(200)', 'Simbolo Solda Filete com Perna de 3mm 50(200)')
        self.add_block('SIMBOLO-SOLDA-FILETE-COM-ALT.-E-COMP.-DE-3mm', 'Simbolo solda Filete com ALT. e COMP. de 3mm')
        self.add_block('SIMBOLO-SOLDA-FILETE-COM-ALT.-E-COMP.-DE-3mm-50(200)', 'Simbolo solda Filete com ALT. e COMP. de 3mm 50(200)')
        self.add_block('SIMBOLO-SOLDA-FILETE-COM-ALT.-E-COMP.-DE-3mm-50(200)-DOS-DOIS-LADOS', 'Simbolo solda Filete com ALT. e COMP. de 3mm 50(200) dos dois lados')

    def add_list_old_blocks_check_by_entity(self):
        self.add_block('SIMBOLO-SOLDA-FILETE', 'Simbolo de Solda Filete', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-FILETE-DOS-DOIS-LADOS', 'Simbolo Solda Filete dos dois lados', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-FILETE-50(200)', 'Simbolo Solda Filete 50(200)', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-FILETE-50(200)-DOS-DOIS-LADOS', 'Simbolo Solda Filete 50(200) dos dois lados', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-RETA-CONVEXA', 'Simbolo Solda Reta Convexa', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-RETA-CONVEXA-50(200)', 'Simbolo Solda Reta Convexa 50(200)', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-RETA-PLANA', 'Simbolo Solda Reta Plana', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-RETA-PLANA-50(200)', 'Simbolo Solda Reta Plana 50(200)', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-EM-V', 'Simbolo Solda em V', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-EM-V-CONVEXA', 'Simbolo Solda em V Convexa', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-EM-V-CONVEXA-50(200)', 'Simbolo Solda em V Convexa 50(200)', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-EM-V-PLANA', 'Simbolo Solda em V Plana', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-EM-MEIO-V', 'Simbolo Solda em Meio V', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-EM-MEIO-V-PLANA', 'Simbolo Solda em Meio V Plana', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
        self.add_block('SIMBOLO-SOLDA-INTERCALADA-50(150)', 'Simbolo Solda Intercalada 50(150)', Entity(dxftype = 'LINE', color = ACI.MAGENTA))
