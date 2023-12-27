class Paper():
    def __init__(self, title: str, eid: str, document_type: str, year: int) -> None:
        self.__title = title
        self.__eid = eid
        self.__document_type = document_type,
        self.__year = year

    @property
    def title(self):
        return self.__title
    
    @property
    def eid(self):
        return self.__eid

    @property
    def document_type(self):
        return self.__document_type

    @property
    def year(self):
        return self.__year
    
if __name__ == "__main__":
    paper = Paper("Paper poco scientifico", "s2023-twitch123", "Article", 2023)
    
    print(paper.title, paper.eid, paper.document_type, paper.year)