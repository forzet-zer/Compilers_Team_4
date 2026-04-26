from nltk.tree import Tree

class Arbol:
    def __init__(self, etiqueta_raiz, hijos=None):
        self.label = etiqueta_raiz
        self.children = hijos

    def etiqueta(self):
        return self.label

    def hijos(self):
        return self.children

    def print(self, f):
        tree = _toNLTK_Tree(self)
        tree.pretty_print(stream=f,unicodelines=False)


def _toNLTK_Tree(arbol):
    if isinstance(arbol, (str, int, float, bool)):
        return str(arbol)
    if not hasattr(arbol, 'hijos') or arbol.hijos() is None:
        return Tree(arbol.etiqueta(), [])
    else:
        hijos_procesados = []
        for child in arbol.hijos():
            if isinstance(child, list):
                hijos_procesados.extend(_toNLTK_Tree(c) for c in child)
            else:
                hijos_procesados.append(_toNLTK_Tree(child))
        return Tree(arbol.etiqueta(), hijos_procesados)