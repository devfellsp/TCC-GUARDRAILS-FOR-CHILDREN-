"""Restaura somente o índice preservado desta versão isolada, sem inferência."""
import numpy as np
import guardkids as g


def restore():
    pointer = g.read_json(g.BASE / "indice_preservado/current.json")
    folder = g.BASE / "indice_preservado" / pointer["id"]
    meta = g.read_json(folder / "chunks.json")
    if g.digest(meta) != pointer["id"]:
        raise ValueError("Identidade do índice preservado divergente")
    with np.load(folder / "index.npz", allow_pickle=False) as data:
        vectors = data["vectors"]
    g.validate_index(meta, vectors, g.config())
    return g.publish_index(meta, vectors)


if __name__ == "__main__":
    print(restore())
