import ezdxf
from collections import Counter

def normalize_value(value, precision=4):
    if isinstance(value, float):
        return round(value, precision)
    elif isinstance(value, (list, tuple)):
        return tuple(normalize_value(v, precision) for v in value)
    return value

def entity_to_key(e, precision=4):

    attribs = e.dxfattribs()

    IGNORED_ATTRS = {"handle", "owner"}

    normalized = {}
    for k, v in attribs.items():
        if k in IGNORED_ATTRS:
            continue
        normalized[k] = normalize_value(v, precision)

    items_sorted = tuple(sorted(normalized.items()))

    return (e.dxftype(), items_sorted)

def get_block_entities(block):
    return [entity_to_key(e) for e in block]

def diff_blocks(block1, block2):
    ents1 = Counter(get_block_entities(block1))
    ents2 = Counter(get_block_entities(block2))

    removed = ents1 - ents2
    added = ents2 - ents1

    return removed, added


# =========================
# USO
# =========================

BLOCK_NAME = ""

doc1 = ezdxf.readfile("")
doc2 = ezdxf.readfile("")

block1 = doc1.blocks.get(BLOCK_NAME)
block2 = doc2.blocks.get(BLOCK_NAME)

if not block1 or not block2:
    print("Bloco não existe em um dos arquivos")
else:
    removed, added = diff_blocks(block1, block2)

    print(f"\n🔴 REMOVIDOS ({sum(removed.values())}):")
    for ent, count in removed.items():
        print(f"{count}x {ent}")

    print(f"\n🟢 ADICIONADOS ({sum(added.values())}):")
    for ent, count in added.items():
        print(f"{count}x {ent}")