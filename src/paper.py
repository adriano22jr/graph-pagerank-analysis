class Paper():
    def __init__(self, title: str, authors: list, keywords: list, eid: str, document_type: str, publisher: str, year: int) -> None:
        self.__title = title
        self.__authors = authors
        self.__keywords = keywords
        self.__eid = eid
        self.__document_type = document_type,
        self.__publisher = publisher
        self.__year = year

    @property
    def title(self):
        return self.__title

    @property
    def authors(self):
        return self.__authors

    @property
    def keywords(self):
        return self.__keywords

    @property
    def eid(self):
        return self.__eid

    @property
    def document_type(self):
        return self.__document_type
    
    @property
    def publisher(self):
        return self.__publisher

    @property
    def year(self):
        return self.__year
    
if __name__ == "__main__":
    paper = Paper("Paper poco scientifico", ["Gianmarco Tocco", "Dario Moccia"], ["twitch", "content", "stream"], 
                  "s2023-twitch123", "Article", "Twitch.tv", 2023)
    
    print(paper.title, paper.authors, paper.keywords, paper.eid, paper.document_type, paper.publisher, paper.year)