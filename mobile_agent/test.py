'''
from owlready2 import *
from enum import Enum
import json
from datetime import datetime

# тип поиска (книги или статьи)
class search(Enum):
    Books = 1
    Articles = 2
    Sites = 3
    Authors = 4

# Запрос к онтологии
class SparqlQueries:
    def __init__(self, path, typeSearch):
        self.typeSearch = typeSearch
        my_world = World()
        #path to the owl file is given here
        my_world.get_ontology(path).load()
        #sync_reasoner(my_world)  #reasoner is started and synchronized here
        self.graph = my_world.as_rdflib_graph()

    # получение книг по теме и не раньше выбранной даты
    def getBooksByThemesAndDate(self, theme, date, typeSearch):

        if typeSearch is search.Books:
            property = "КнигаНаписанаПро"
            prop = "rating_book"
            prop1 = "date_book"
            str1 = "Книга: "
        elif typeSearch is search.Articles:
            property = "СтатьяНаписанаПро"
            prop = "rating_article"
            prop1 = "date_article"
            str1 = "Статья: "
        elif typeSearch is search.Sites:
            property = "СайтНаписанПро"
            prop = "rating_site"
            prop1 = "date_site"
            str1 = "Сайт: "

        print(date)
        print("FILTER(?day > ", date, "). ")
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
            "SELECT ?title ?day " \
            "WHERE { " \
            "?title pln:" + property + " pln:" + theme + ". " \
            "?title pln:" + prop1 + " ?day. " \
            "FILTER(?day > \"" + date + "\"^^xsd:dateTime). " \
            "} " \
            
        
        print(query)
    
        resultsList = self.graph.query(query)

        response = []

        for item in resultsList:
            title = str(item['title'].toPython())
            title = re.sub(r'.*#',"", title)
           # themes, authors, url = self.getTitleThemesAndAuthors(title, typeSearch)
            
           # if themes != [] or authors != []:
            response.append({'book' : str1 + title})
        
        return response

    # получаем данные для пользователя по его интересам
    def getDataForUser(self, user, date):
        data1 = data2 = data3 = []

        data = []

        interests = ['Палинология__', 'Типы__пыльцевых__зерен__в__зависимости__от__полярности__', 'Палинология__в__геологии__', 'Формирование__пыльцевого__зерна__', 'Форма__пыльцевого__зерна__', 'Пыльцевые__зерна__', 'Скульптура__пыльцевого__зерна__']
        for theme in interests:
            #data1 = (self.getBooksByThemesAndDate(theme, date, search.Books))
            data2 = (self.getBooksByThemesAndDate(theme, date, search.Articles))
            data3 = (self.getBooksByThemesAndDate(theme, date, search.Sites))
        return data1 + data2 + data3

def main():
    typeSearch = search.Articles
    path = r"D:\Desktop\ПМИ\3_курс\Курсовая\Готовое\psu-monitoring\api\polynology.owl"

    stringData = datetime(2021, 4, 20, 0, 0, 0).isoformat()
    #stringData = "2021-04-05T00:00:00"
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getDataForUser("nikita", stringData)
    if data == []:
        data = [{"book": "no", "themes": [], "authors": [], "url": []}]
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data
'''


from lxml.html import fromstring 
import requests 
from itertools import cycle 
import traceback 
def get_proxies():  
    url = 'https://free-proxy-list.net/'  
    response = requests.get(url)  
    parser = fromstring(response.text)  
    proxies = set()  
    for i in parser.xpath('//tbody/tr')[:10]: 
        if i.xpath('.//td[7][contains(text(),"yes")]'):  
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])  
            proxies.add(proxy) 
    print(proxies)
    return proxies #If you are copy pasting proxy ips, put in the list below
#proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080'] 
f = True

while f:
    proxies = get_proxies() 
    #proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
    proxy_pool = cycle(proxies) 
    url = 'https://httpbin.org/ip'

    for i in range(1,11): #Get a proxy from the pool  
        proxy = next(proxy_pool)  
        print("Request #%d"%i)  
        try:  
            response = requests.get(url,proxies={"http": proxy, "https": proxy})  
            print(response.json())
            f = False  
        except:  #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url   
            print("Skipping. Connnection error") 





#if __name__ == "__main__":
 #   main()