import networkx as nx
import matplotlib.pyplot as plt
operators = set('.*|')
brackets = set('()')


class Node:
    def __init__(self):
        self.left, self.right, self.root, self.value = None, None, None, None

    def new_left(self):
        self.left = Node()
        self.left.root = self
        return self.left

    def new_right(self):
        self.right = Node()
        self.right.root = self
        return self.right

    def new_right_root(self):
        self.root = Node()
        self.root.left = self
        return self.root

    def __repr__(self):
        return self.value


def get_filled_concat_symbols_regexp(regexp):
    T = set(filter(lambda item: not item in operators | brackets, regexp))
    filed_regexp = str()

    for i, item in enumerate(regexp):
        filed_regexp += item
        if i + 1 < len(regexp) and regexp[i] in T | set('*)') and regexp[i + 1] in T | set('('):
            filed_regexp += '.'

    return filed_regexp


def build_tree(regexp):
    root = Node()
    current = root.new_left()

    T = set(filter(lambda item: not item in operators | brackets, regexp))
    filled_regexp = get_filled_concat_symbols_regexp(regexp)

    for token in filled_regexp:

        if token == '(':
            current = current.new_left()
            continue

        if token == ')':
            current = current.root or current.new_right_root()
            continue

        if token in T:
            current.value = token
            current = current.root or current.new_right_root()
            continue

        if token in set('.|'):
            if current.value:
                current = current.new_right_root()
            current.value = token
            current = current.new_right()

            continue

        if token == '*':
            if current.value:
                current = current.new_right_root()
            current.value = token
    return current


def nullable(node):
    if node is None:
        return True

    if node.value == '|':
        return nullable(node.left) or nullable(node.right)

    if node.value == '.':
        return nullable(node.left) and nullable(node.right)

    if node.value == '*':
        return True

    return False


i = 1


def fill_tree_pos(root):
    global i

    if root is None:
        return

    fill_tree_pos(root.left)
    fill_tree_pos(root.right)

    root.firstpos = set()
    root.lastpos = set()

    if root.value in operators:

        if root.value == '|':
            root.firstpos |= root.left.firstpos | root.right.firstpos
            root.lastpos |= root.left.lastpos | root.right.lastpos

        if root.value == '.':
            if nullable(root.left):
                root.firstpos |= root.left.firstpos | root.right.firstpos
            else:
                root.firstpos |= root.left.firstpos

            if nullable(root.right):
                root.lastpos |= root.left.lastpos | root.right.lastpos
            else:
                root.lastpos |= root.right.lastpos

        if root.value == '*':
            root.firstpos |= root.left.firstpos
            root.lastpos |= root.left.lastpos
    else:
        root.firstpos.add(i)
        root.lastpos.add(i)

        i += 1


def fill_followpos(root, followpos):
    if root is None:
        return

    fill_followpos(root.left, followpos)
    fill_followpos(root.right, followpos)
    if root.value == '.':
        for i in root.left.lastpos:
            followpos[i - 1] |= root.right.firstpos

    if root.value == '*':
        for i in root.left.lastpos:
            followpos[i - 1] |= root.left.firstpos



def build_dka(q0, regexp, followpos):
    positions = list(filter(lambda item: not item in operators | brackets, regexp))

    F = list()
    Q = set()

    unhandled = set()

    unhandled.add(tuple(q0))

    while unhandled:
        current = unhandled.pop()
        if not current in Q:
            for i in current:
                next_state = followpos[i - 1]
                F.append((current, positions[i - 1], tuple(next_state)))

                unhandled.add(tuple(next_state))
        Q.add(current)

    return Q, F


if __name__ == '__main__':
    #regexp = '(a|b)*abb'
    regexp = '1*0'
    regexp += '#'

    root = build_tree(regexp)
    fill_tree_pos(root)
    followpos = [set() for i in range(len(list(filter(lambda item: not item in operators | brackets, regexp))))]
    fill_followpos(root, followpos)

    Q, F = build_dka(root.firstpos, regexp, followpos)
    G = nx.DiGraph()
    step = []
    variables = {}
    final = ''
    for i in range(len(F)):
        for j in range(len(F[i][0])):
            for k in range(len(F[i][2])):
                G.add_edges_from([(F[i][0][j], F[i][2][k])], weight=ord(F[i][1]))
                if F[i][1] != '#':
                    print("{0} -> {1} по символу {2}".format(str(F[i][0][j]),str(F[i][2][k]),F[i][1]))
    pos = nx.spring_layout(G)
    edge_labels = dict([((u, v,), chr(d['weight']))
                        for u, v, d in G.edges(data=True)])
    nx.draw(G, pos, node_color = '#CCDAE5',node_size=400, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
