import networkx as nx


def calculate_demand(G):
    sc = list(nx.strongly_connected_components(G))
    sc_count = [len(x) for x in sc]
    sc_sum = sum(sc_count)
    sc_ratio = [(x / sc_sum) for x in sc_count]

    result = dict()

    for i, sc_entry in enumerate(sc):
        for sc_item in sc_entry:
            result[sc_item] = sc_ratio[i]
            G.nodes[sc_item]["capacity"] = sc_ratio[i]
    return result


def print_stats(G):
    try:
        calculate_demand(G)
        print("min_cost_flow")
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.min_cost_flow.html#networkx.algorithms.flow.min_cost_flow
        # demand maybe from strongly_connected_components
        print(nx.min_cost_flow(G, capacity="inverse_weight", weight="weight"))

        print("pagerank")
        print(nx.pagerank(G))

        print("average_node_connectivity")
        print(nx.average_node_connectivity(G))

        print("dominating_set")
        print(nx.dominating_set(G))

        print("strongly_connected_components")
        print(list(nx.strongly_connected_components(G)))
    except Exception:
        pass
