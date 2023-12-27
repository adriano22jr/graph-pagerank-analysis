from paper import Paper

class Graph():
    def __init__(self) -> None:
        self.__graph = {}
    
    def add_node(self, node: Paper):
        if node.eid not in self.__graph:
            self.__graph[node.eid] = set()
    
    def add_edge(self, paper: Paper, cited_paper: Paper):
        self.add_node(paper)
        self.add_node(cited_paper)
        
        self.__graph[paper.eid].add(cited_paper.eid)
        
    def remove_edge(self, paper: Paper, cited_paper: Paper):
        self.__graph[paper.eid].remove(cited_paper.eid)
        
    def remove_node(self, node: Paper):
        del self.__graph[node.eid]
        for paper in self.__graph:
            self.remove_edge(paper, node)
    
    def get_connections(self, paper):
        return self.__graph[paper.eid]
    
    def get_edges(self):
        edges = []
        
        for node in self.__graph:
            for con in self.__graph[node]:
                edges.append( (node, con) )
        
        return edges
        
        
if __name__ == "__main__":
    paper1 = Paper("Paper poco scientifico", "s2023-twitch123", "Article", 2023)
    
    paper2 = Paper("Paper molto scientifico", "s2023-rep1", "Conference Paper", 2022)
    
    graph = Graph()
    graph.add_edge(paper1, paper2)
    print(graph.get_connections(paper1))
    print(graph.get_connections(paper2))
    
    
    print(graph.get_edges())