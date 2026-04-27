import ezdxf
import hashlib

def normalize_value(value, precision=4):
    if isinstance(value, float):
        return round(value, precision)
    elif isinstance(value, (list, tuple)):
        return tuple(normalize_value(v, precision) for v in value)
    return value


def entity_to_string(e, precision=4):
    attribs = e.dxfattribs()
    normalized = {}

    IGNORED_ATTRS = {"handle", "owner"}

    for k, v in attribs.items():
        if k in IGNORED_ATTRS:
            continue
        normalized[k] = normalize_value(v, precision)

    items_sorted = sorted(normalized.items())
    return f"{e.dxftype()}|{items_sorted}"


def block_signature(block):
    entity_strings = [entity_to_string(e) for e in block]
    entity_strings.sort()
    full_string = "\n".join(entity_strings)
    return hashlib.md5(full_string.encode()).hexdigest()


# =========================
# USO
# =========================

BLOCK_NAME = ""

doc1 = ezdxf.readfile("")
doc2 = ezdxf.readfile("")

block1 = doc1.blocks.get(BLOCK_NAME)
block2 = doc2.blocks.get(BLOCK_NAME)

if block1 is None:
    print(f"Bloco '{BLOCK_NAME}' não existe no arquivo 1")
elif block2 is None:
    print(f"Bloco '{BLOCK_NAME}' não existe no arquivo 2")
else:
    sig1 = block_signature(block1)
    sig2 = block_signature(block2)

    if sig1 == sig2:
        print(f"Bloco '{BLOCK_NAME}' é idêntico")
    else:
        print(f"Bloco '{BLOCK_NAME}' foi MODIFICADOXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")