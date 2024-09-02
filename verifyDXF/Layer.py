class LayerList:
    def __init__(self):
        self.layers = {}

    def add_layer(self, name, visible, frozen, locked, color, line_type, line_weight):
        self.layers[name] = Layer(name, visible, frozen, locked, color, line_type, line_weight)

    def add_default_layer(self):
        self.add_layer("0", True, False, False, 3, "Continuous", 50)
        self.add_layer("ALTRI IMPIANTI", True, False, False, 9, "Continuous", 9)
        self.add_layer("ASSI", True, False, False, 1, "CENTER2", 20)
        self.add_layer("CONTORNI", True, False, False, 2, "Continuous", 40)
        self.add_layer("CONTORNI 2", True, False, False, 4, "Continuous", 30)
        self.add_layer("CONTORNI 3", True, False, False, 7, "Continuous", 20)
        self.add_layer("Defpoints", True, False, False, 7, "Continuous", 20)
        self.add_layer("ESISTENTE", True, False, False, 8, "PHANTOM2", 9)
        self.add_layer("LANG-FR", False, True, False, -4, "Continuous", -3)
        self.add_layer("LANG-IN-R1", True, False, False, 3, "Continuous", -3)
        self.add_layer("LANG-IN-R2", False, True, False, -3, "Continuous", -3)
        self.add_layer("LANG-IT", False, True, False, -2, "Continuous", -3)
        self.add_layer("LANG-SP", False, True, False, -6, "Continuous", -3)
        self.add_layer("NASCOSTE", True, False, False, 6, "HIDDEN", 20)
        self.add_layer("NOTE", True, False, False, 3, "Continuous", 50)
        self.add_layer("QUOTE", True, False, False, 1, "Continuous", -3)
        self.add_layer("REDECAM_Blocco_Bulloneria", True, False, False, 5, "Continuous", -3)
        self.add_layer("REDECAM_Blocco_Distinta", True, False, False, 7, "Continuous", -3)
        self.add_layer("REDECAM_Bocco_Guarnizioni", True, False, False, 2, "Continuous", -3)
        self.add_layer("REDECAM_Squadratura_Cartiglio", True, False, False, 1, "Continuous", -3)
        self.add_layer("SOTTILI", True, False, False, 1, "Continuous", 20)
        self.add_layer("TESTI", True, False, False, 4, "Continuous", 30)
        self.add_layer("TRATTEGGI", True, False, False, 1, "Continuous", 20)

class Layer():
    def __init__(self, name, visible, frozen, locked, color, line_type, line_weight):
        self.name = name
        self.visible = visible
        self.frozen = frozen
        self.locked = locked
        self.color = color
        self.line_type = line_type
        self.line_weight = line_weight