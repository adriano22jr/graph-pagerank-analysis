import networkx as nx

def create_citation_graph(dataframe):
    graph = nx.DiGraph()  
    nodes_list = set()
    edges_list = set()
    
    for paper_id in set(dataframe["id"]):
        nodes_list.add(str(paper_id))
    
    current = 1    
    for paper_id in set(dataframe["id"]):
        percentage = (current / len(dataframe.axes[0]) * 100)
        print(f"Current percentage: {percentage: .2f}%", end = "\r")
        
        current_paper = tuple(dataframe.loc[dataframe["id"] == paper_id].iloc[0])
        references = current_paper[7]
        for reference_id in references:
            if reference_id in nodes_list:
                edges_list.add( (str(paper_id), reference_id) )

        current += 1
    
    graph.add_nodes_from(nodes_list)
    graph.add_edges_from(edges_list)
    
    return graph

def create_subgraph(graph, start_node):
    sub = nx.DiGraph()
    nodes_list = set()
    edges_list = []
    
    ancestors = nx.ancestors(graph, start_node)
    for item in ancestors: nodes_list.add(item)
    
    edges_list += graph.in_edges(start_node)
    
    for node in nodes_list:
        edges_list += graph.in_edges(node)
        
    sub.add_nodes_from(nodes_list)
    sub.add_edges_from(edges_list)
        
    return sub

def get_authors_name(dataframe, input_list):
    authors = []
    
    for item in input_list:
        row = tuple(dataframe.loc[:, int(item)])
        if row[0] is None: authors.append(row[1])
        elif row[1] is None: authors.append(row[0])
        else: authors.append(row[0] + " " + row[1])
        
    return authors

def normalization(x, new_min, new_max, old_min, old_max):
    new_x = ( (x - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
    return new_x

def normalize_pagerank(graph, sorted_scores):
    pagerank_subgraph_scores = []
    normalized_scores = []
    
    for node in graph.nodes:
        for couple in sorted_scores:
            if couple[0] == node: pagerank_subgraph_scores.append(couple)
            
    pagerank_subgraph_scores.sort(key = lambda x : x[1], reverse = True)
    normalized_scores = [(x[0], 25 - normalization(x[1], 0, 1, min(pagerank_subgraph_scores)[1], max(pagerank_subgraph_scores)[1])) for x in pagerank_subgraph_scores]
    
    return normalized_scores

def get_node_colors(graph, sorted_scores):
    pagerank_subgraph_scores = []
    color_gradients = []
    
    for node in graph.nodes:
        for couple in sorted_scores:
            if couple[0] == node: pagerank_subgraph_scores.append(couple)
            
    pagerank_subgraph_scores.sort(key = lambda x : x[1], reverse = True)
    
    scores_set = set([x[1] for x in pagerank_subgraph_scores])    
    steps = len(scores_set) - 1
    count = 1
    r_step, g_step, b_step = (124 - 69) / steps, (223 - 145) / steps, (218 - 80) / steps 
    
    for item in pagerank_subgraph_scores:
        if item[1] == max(scores_set): color_gradients.append( (item[0], item[1], (124, 223, 80)) )
        elif item[1] == min(scores_set): color_gradients.append( (item[0], item[1], (69, 145, 218)) )
        else:
            color_gradients.append( (item[0], item[1], (round(124 - r_step*count, 0), round(223 - g_step*count, 0), round(80 + b_step*count, 0))) )
            count += 1
    
    return color_gradients