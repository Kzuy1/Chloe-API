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

    # def add_list_old_blocks_check_by_name(self): 


    # def add_list_old_blocks_check_by_entity(self):