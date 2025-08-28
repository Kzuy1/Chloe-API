class LayerList:
    def __init__(self):
        self.layers = {}

    def add_layer(self, name, visible, frozen, locked, color, line_type, line_weight):
        self.layers[name] = Layer(name, visible, frozen, locked, color, line_type, line_weight)

    def add_default_layer(self):
        self.add_layer("0", True, False, False, 3, "Continuous", 50)
        self.add_layer("CONTORNO", True, False, False, 2, "Continuous", 40)
        self.add_layer("COTAS", True, False, False, 1, "Continuous", -3)
        self.add_layer("Defpoints", True, False, False, 7, "Continuous", -3)
        self.add_layer("FANTASMA", True, False, False, 8, "PHANTOM2", 9)
        self.add_layer("FINA", True, False, False, 1, "Continuous", 20)
        self.add_layer("FORMATO", True, False, False, 1, "Continuous", -3)
        self.add_layer("HACHURAS", True, False, False, 1, "Continuous", 20)
        self.add_layer("NOTAS", True, False, False, 3, "Continuous", 50)
        self.add_layer("OCULTA", True, False, False, 6, "HIDDEN", 20)
        self.add_layer("SIMETRIA", True, False, False, 1, "CENTER2", 20)
        self.add_layer("TEXTO", True, False, False, 4, "Continuous", 30)

class Layer():
    def __init__(self, name, visible, frozen, locked, color, line_type, line_weight):
        self.name = name
        self.visible = visible
        self.frozen = frozen
        self.locked = locked
        self.color = color
        self.line_type = line_type
        self.line_weight = line_weight