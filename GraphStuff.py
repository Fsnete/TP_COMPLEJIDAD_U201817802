import graphviz as gv
import networkx as nx

def nx2gv(G, weighted=False, params={'rankdir': 'LR', 'size': '6'},
          path=None, pathparams={'color': 'orangered'}, nodeinfo=False):
    if G.is_directed():
        g = gv.Digraph('G')
    else:
        g = gv.Graph('G')
    g.attr(**params)

    for u in G.nodes:
        if nodeinfo:
            g.node(str(u), **dict(G.nodes[u]))
        else:
            g.node(str(u))

    for u, v in G.edges():
        pp = pathparams if path and path[v] == u else {}

        if weighted:
            g.edge(str(u), str(v), f"{G.edges[u, v]['weight']}", **pp)
        else:
            g.edge(str(u), str(v), **pp)

    return g


