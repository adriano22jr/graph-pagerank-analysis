import bs4, requests, math

def create_url(paper_title):
    url = "https://scholar.google.com/scholar?q="
    edited_title = paper_title.replace(" ", "+")
    return url + edited_title

def get_citations(paper_title):
    response = requests.get(create_url(paper_title))

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        divs = soup.find_all("div", class_ = "gs_fl")

        for div in divs:
            elements = div.find_all("a")
            for elem in elements:
                if str(elem.contents[0]).startswith("Citato da"): 
                    citation_count = str(elem.contents[0]).split(" ")[2]
                    link = "https://scholar.google.com/scholar?start=&" + elem["href"][9:]
                    return int(citation_count), link
                
def get_referred_titles(citation_count, link):
    estimated_pages = math.ceil(citation_count / 10)
    titles_list = []
    
    for i in range(estimated_pages):
        split = link.split("start=")
        current_page = split[0] + f"start={i * 10}" + split[1]
        
        response = requests.get(current_page)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        
        h3s = soup.find_all("h3", class_ = "gs_rt")
        for h3 in h3s:
            if h3.find("a"):
                element = h3.find("a").contents[0]
                titles_list.append(element)
            elif h3.find("span", id = ""):
                element = h3.find("span").contents[0]
                titles_list.append(element)
            print(len(titles_list))
    return titles_list