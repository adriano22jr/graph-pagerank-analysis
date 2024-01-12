from flask_visjs import VisJS4, Network
from flask import Flask, render_template_string, redirect, render_template, request, url_for
import networkx as nx
import pandas as pd

app = Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")
VisJS4().init_app(app)

@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        paper_id = request.form["paper_id"]
        return redirect(url_for("subgraph", paper = paper_id)) 
    else:
        paper_dataframe = pd.read_json("src/data/nlp_papers.json")
        citation_graph = create_citation_graph(paper_dataframe)
        
        scores = nx.pagerank(citation_graph)
        sorted_scores = sorted(scores.items(), key = lambda x : x[1], reverse = True)
        
        triples = []
        for item in sorted_scores:
            input_links = citation_graph.in_edges(item[0])
            triples.append( (item[0], item[1], len(input_links)) )
        return render_template("index.html", triples = triples)

@app.route("/subgraph/<paper>", methods=['GET', 'POST'])
def subgraph(paper):
    paper_dataframe = pd.read_json("src/data/nlp_papers.json")
    citation_graph = create_citation_graph(paper_dataframe)
    subgraph = create_subgraph(citation_graph, paper)
    
    network = Network("500px", "1000px", directed = True)
    for node in subgraph.nodes:
        network.add_node(node)
    network.add_edges(subgraph.edges)
    
    return render_template("subgraph.html", network = network, paper_id = paper, subgraph = subgraph)
    
    
    
    
    
    
    
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


if __name__ == "__main__":
    app.run(port = 8080, debug=True)