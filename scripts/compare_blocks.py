import ezdxf
from collections import Counter


def normalize_value(value, precision=4):
    if isinstance(value, float):
        return round(value, precision)

    elif isinstance(value, (list, tuple)):
        return tuple(
            normalize_value(v, precision)
            for v in value
        )

    return value


def entity_to_key(entity, precision=4):
    attribs = entity.dxfattribs()

    IGNORED_ATTRS = {"handle", "owner"}

    normalized = {}

    for key, value in attribs.items():
        if key in IGNORED_ATTRS:
            continue

        normalized[key] = normalize_value(value, precision)

    items_sorted = tuple(sorted(normalized.items()))

    return entity.dxftype(), items_sorted


def block_signature(block):
    entities = [
        entity_to_key(entity)
        for entity in block
    ]

    return Counter(entities)


def get_block_names(doc):
    return {
        block.name
        for block in doc.blocks
        if not block.name.startswith("*")
    }


def compare_blocks(doc1, doc2):

    blocks1 = get_block_names(doc1)
    blocks2 = get_block_names(doc2)

    # =========================
    # EXISTÊNCIA DOS BLOCOS
    # =========================

    removed = blocks1 - blocks2
    added = blocks2 - blocks1

    common = blocks1 & blocks2

    # =========================
    # CONTEÚDO DOS BLOCOS
    # =========================

    modified = set()
    unchanged = set()

    for block_name in common:

        block1 = doc1.blocks.get(block_name)
        block2 = doc2.blocks.get(block_name)

        signature1 = block_signature(block1)
        signature2 = block_signature(block2)

        if signature1 == signature2:
            unchanged.add(block_name)
        else:
            modified.add(block_name)

    return removed, added, modified, unchanged


# =========================
# USO
# =========================

FILE_1 = ""
FILE_2 = ""

doc1 = ezdxf.readfile(FILE_1)
doc2 = ezdxf.readfile(FILE_2)

removed, added, modified, unchanged = compare_blocks(
    doc1,
    doc2
)


# =========================
# RESULTADO
# =========================

print("\n🔴 BLOCOS REMOVIDOS")

if removed:
    for block_name in sorted(removed):
        print(f"  - {block_name}")
else:
    print("  Nenhum")


print("\n🟢 BLOCOS ADICIONADOS")

if added:
    for block_name in sorted(added):
        print(f"  - {block_name}")
else:
    print("  Nenhum")


print("\n🟡 BLOCOS MODIFICADOS")

if modified:
    for block_name in sorted(modified):
        print(f"  - {block_name}")
else:
    print("  Nenhum")


print("\n⚪ BLOCOS SEM ALTERAÇÃO")

if unchanged:
    for block_name in sorted(unchanged):
        print(f"  - {block_name}")
else:
    print("  Nenhum")