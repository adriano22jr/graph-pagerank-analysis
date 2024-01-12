import numpy as np

class Graph():
    def __init__(self) -> None:
        self.__graph = {}
    
    def add_node(self, node):
        if node not in self.__graph:
            self.__graph[node] = set()
    
    def add_edge(self, fr, to):
        self.add_node(fr)
        self.add_node(to)
        
        self.__graph[fr].add(to)
        
    def remove_edge(self, fr, to):
        self.__graph[fr].remove(to)
        
    def remove_node(self, node):
        del self.__graph[node]
    
    def get_node_connections(self, node):
        return self.__graph[node]
    
    def get_edges(self):
        edges = []
        
        for node in self.__graph:
            for con in self.__graph[node]:
                edges.append( (node, con) )
        
        return edges
    
    def get_dict(self):
        return self.__graph
        
        
if __name__ == "__main__":
    node1 = ("Paper poco scientifico", "s2023-twitch123", "Article", 2023)
    node2 = ("Paper molto scientifico", "s2023-rep1", "Conference Paper", 2022)

    graph = Graph()
    graph.add_edge(node1, node2)
    
    print(graph.get_node_connections(node1))
    print(graph.get_node_connections(node2))
    print(graph.get_dict())