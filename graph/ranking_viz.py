from colour import Color, RGB_equivalence
from networkx import DiGraph
from networkx import nx_pydot
from typing import List


def digraph_to_dot_viz(
        di_graph: DiGraph,
        start_color: str = "white",
        end_color: str = "grey",
        highlight_paths: List[tuple] = None,
        highlight_color = "red",
        output_dot_viz = None,
        max_pen_width = 12,
):
    # TODO have an option to only show the highlight path
    dg = di_graph.copy()
    max_weight = 0

    edges = dg.edges(data=True)
    for edge in edges:
        data = edge[2]
        weight = data["weight"]
        if weight > max_weight:
            max_weight = weight
        data["penwidth"] = weight
        del data["weight"]

    if max_weight > max_pen_width:
        for edge in edges:
            penwidth = edge[2]["penwidth"]
            penwidth = int((penwidth / max_weight) * max_pen_width)
            if penwidth < 1:
                penwidth = 1

            edge[2]["penwidth"] = penwidth

    nodes = dg.nodes(data=True)

    positions = set([int(x[1]["position"]) for x in nodes])
    start = Color(start_color, equality = RGB_equivalence)
    end = Color(end_color, equality = RGB_equivalence)
    color_gradient = list(start.range_to(end, max(positions) + 1))

    for node in nodes:
        data = node[1]
        data["shape"] = "rectangle"
        data["style"] = "filled"
        data["label"] = node[0].replace("_", " ").strip()
        data["fillcolor"] = color_gradient[int(data["position"])].hex_l

    print(highlight_paths)

    edges = dg.edges(data=True)
    for path in highlight_paths:
        for i in range(len(path) - 1):
            
            # get bidirectional matches
            matching_steps = [x for x in edges if x[0] == path[i] and x[1] == path[i + 1]] + \
                [x for x in edges if x[0] == path[i+1] and x[1] == path[i]]
            
            max_pen_width = 0
            for match_edge in matching_steps:
                match_edge[2]["color"] = highlight_color
                if match_edge[2]["penwidth"] > max_pen_width:
                    max_pen_width = match_edge[2]["penwidth"]

            for match_edge in matching_steps:
                match_edge[2]["penwidth"] = max_pen_width

    # seems like the graph attributes set on
    # networkx Graph don't get set on 
    # the returned pydot 
    # there is an issue on the networkX repo seems related
    # https://github.com/networkx/networkx/issues/3547
    # however concatenating removes any additional styling 
    # differences between merged paths :/
    a_graph = nx_pydot.to_pydot(dg)
    a_graph.obj_dict['attributes'] = {"concentrate": "true"}

    if output_dot_viz is not None:
        with open(output_dot_viz, "w") as f:
            f.write(str(a_graph))

    return a_graph
