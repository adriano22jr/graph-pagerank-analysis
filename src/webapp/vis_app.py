from flask_visjs import VisJS4, Network
from flask import Flask, render_template_string, redirect, render_template, request, url_for
from functions import *
import pandas as pd

app = Flask(__name__, template_folder = "templateFiles", static_folder = "staticFiles")
VisJS4().init_app(app)

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html")
    
@app.route("/regular", methods = ["GET", "POST"])
def regular():
    if request.method == "POST":
        paper_id = request.form["paper_id"]
        return redirect(url_for("subgraph", type = "regular", paper = paper_id)) 
    else:
        paper_dataframe = pd.read_json("src/data/nlp_papers.json")
        citation_graph = create_citation_graph(paper_dataframe)
        
        scores = nx.pagerank(citation_graph)
        sorted_scores = sorted(scores.items(), key = lambda x : x[1], reverse = True)
        
        triples = []
        for item in sorted_scores:
            input_links = citation_graph.in_edges(item[0])
            triples.append( (item[0], item[1], len(input_links)) )
        return render_template("pagerank.html", triples = triples)
    
@app.route("/weighted", methods = ["GET", "POST"])
def weighted():
    if request.method == "POST":
        paper_id = request.form["paper_id"]
        return redirect(url_for("subgraph", type = "weighted", paper = paper_id)) 
    else:
        paper_dataframe = pd.read_json("src/data/nlp_papers.json")
        similarity_dataframe = pd.read_json("src/data/similarities.json", dtype={'id': str})
        weighted_citation_graph = create_weighted_citation_graph(paper_dataframe, similarity_dataframe)
        
        scores = nx.pagerank(weighted_citation_graph)
        sorted_scores = sorted(scores.items(), key = lambda x : x[1], reverse = True)
        
        triples = []
        for item in sorted_scores:
            input_links = weighted_citation_graph.in_edges(item[0])
            triples.append( (item[0], item[1], len(input_links)) )
        return render_template("pagerank.html", triples = triples)
    
@app.route("/complete-graph", methods = ["GET", "POST"])
def complete_graph():
    paper_dataframe = pd.read_json("src/data/nlp_papers.json")
    authors_dataframe = pd.read_json("src/data/nlp_authors.json")
    citation_graph = create_citation_graph(paper_dataframe)
    
    scores = nx.pagerank(citation_graph)
    sorted_scores = sorted(scores.items(), key = lambda x : x[1], reverse = True)
    colors = get_node_colors(citation_graph, sorted_scores)

    network = Network("650px", "1000px", directed = True)
    for node in citation_graph.nodes:
        current_paper_informations = tuple(paper_dataframe.loc[paper_dataframe["id"] == int(node)].iloc[0])
        authors_list = get_authors_name(authors_dataframe, current_paper_informations[3])
        
        pagerank = 0;
        for couple in sorted_scores:
            if couple[0] == node:
                pagerank = couple[1]
                
        color = ""
        for triple in colors:
            if triple[0] == node:
                color = "rgba" + str(triple[2])
        
        network.add_node(node, color = color, titolo = current_paper_informations[1], abstract = current_paper_informations[2], authors = authors_list, year = str(current_paper_informations[4]), publisher = current_paper_informations[5], keywords = current_paper_informations[6], pagerank = pagerank)
        
    network.add_edges(citation_graph.edges)
    return render_template("complete-graph.html", network = network, graph = citation_graph)
    

@app.route("/subgraph/<type>/<paper>", methods = ['GET', 'POST'])
def subgraph(type, paper):
    paper_dataframe = pd.read_json("src/data/nlp_papers.json")
    similarity_dataframe = pd.read_json("src/data/similarities.json", dtype={'id': str})
    authors_dataframe = pd.read_json("src/data/nlp_authors.json")
    
    if type == "regular":
        citation_graph = create_citation_graph(paper_dataframe)
    else:
        citation_graph = create_weighted_citation_graph(paper_dataframe, similarity_dataframe)
    
    scores = nx.pagerank(citation_graph)
    sorted_scores = sorted(scores.items(), key = lambda x : x[1], reverse = True)
    
    subgraph = create_subgraph(citation_graph, paper)
    colors = get_node_colors(subgraph, sorted_scores)
    
    network = Network("650px", "1000px", directed = True)
    for node in subgraph.nodes:
        current_paper_informations = tuple(paper_dataframe.loc[paper_dataframe["id"] == int(node)].iloc[0])
        authors_list = get_authors_name(authors_dataframe, current_paper_informations[3])
        
        pagerank = 0;
        for couple in sorted_scores:
            if couple[0] == node:
                pagerank = couple[1]
                
        color = ""
        for triple in colors:
            if triple[0] == node:
                color = "rgba" + str(triple[2])
        
        if type == "regular":
            if node == paper: network.add_node(node, color = {"background": color, "border": "red"}, titolo = current_paper_informations[1], abstract = current_paper_informations[2], authors = authors_list, year = str(current_paper_informations[4]), publisher = current_paper_informations[5], keywords = current_paper_informations[6], pagerank = pagerank)
            else: network.add_node(node, color = color, titolo = current_paper_informations[1], abstract = current_paper_informations[2], authors = authors_list, year = str(current_paper_informations[4]), publisher = current_paper_informations[5], keywords = current_paper_informations[6], pagerank = pagerank)
        else: 
            if node == paper: network.add_node(node, color = {"background": color, "border": "red"}, titolo = current_paper_informations[1], abstract = current_paper_informations[2], authors = authors_list, year = str(current_paper_informations[4]), publisher = current_paper_informations[5], keywords = current_paper_informations[6], pagerank = pagerank)
            else: network.add_node(node, color = color, titolo = current_paper_informations[1], abstract = current_paper_informations[2], authors = authors_list, year = str(current_paper_informations[4]), publisher = current_paper_informations[5], keywords = current_paper_informations[6], pagerank = pagerank)
            
    if type == "regular":
        network.add_edges(subgraph.edges)
    else:
        for edge in subgraph.edges(data = True):
            weight = edge[2]["weight"]
            network.add_edge(edge[0], edge[1], value = weight)
    return render_template("subgraph.html", network = network, paper_id = paper, subgraph = subgraph)


if __name__ == "__main__":
    app.run(port = 8080, debug=True)