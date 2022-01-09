import requests
from bs4 import BeautifulSoup
from owlready2 import *
from enum import Enum
import Levenshtein
import json

countNewItem = 0
# тип поиска (книги или статьи)
class search(Enum):
    Books = 1
    Articles = 2
    Sites = 3

# Результаты поиска гугл 
class SearchResult:
    def __init__(self, query):
        self.query = query.replace(' ', '+')

    # очищаем строку от ненужных символов
    def clean_str(self, str):
        #chars = [u'\xa0', '"', '...', '|', '…', ',', '\'', '(', ')']
        chars = ['\\','`', '"','*','{','}', '|', '…', ',', '[',']','(',')','>','#','+','-','.','!','$','\'', '—']
        for ch in chars:
            if ch in str:
                str = str.replace(ch, " ")
        str = str.replace(u'\xa0', u'').replace(' ', '_')
        return str

    # поиск авторов для книг
    def get_authors(self, url, results, i):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        for aut in soup.find_all("span", class_="addmd"):
            return aut.text
        for aut in soup.find_all("div", attrs = {"class":"bookinfo_sectionwrap"}):
            return aut.contents[0].text
        return ""

    # поиск книг
    def get_books(self, url, results, i, page_):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        # тут заголовки            
        for entry in soup.find_all("h3"):
            #title = entry.text.replace(u'\xa0', u'').replace('"', '').replace('...', '').replace('…', '').replace('|', '').replace('\'', '').replace(',', '').replace('\'', '').replace('(', '_').replace(')', '_').replace(' ', '_')
            title = self.clean_str(entry.text)
            results.append({'title': title})
        k = 1
        # тут URL + авторы
        for entry in soup.find_all("div", attrs={"class": "kCrYT"}):
            # там выводятся по 2 ссылки, поэтому выбираем только одну из двух
            if k % 2 != 0:
                results[i]['url'] = entry.a['href']
                results[i]['author'] = self.get_authors(entry.a['href'], results, i)
                results[i]['type'] = "КНИГА"
                results[i]['rating'] = page_ / 10 + 1
                i += 1
            k += 1   

    # поиск статей  
    def get_articles(self, url, results, page_):
        content = requests.get(url).text
        page = BeautifulSoup(content, 'lxml')            
        
        for entry in page.find_all("div", attrs={"class": "gs_ri"}):
            count_quote = 0
            entry1 = entry.find("h3", attrs={"class": "gs_rt"})
            book_text = entry1.find(class_ = "gs_ct1")
            if book_text and book_text.text == "[КНИГА]":
                type = "КНИГА"
            else: 
                type = "СТАТЬЯ"
            title = entry1.a.text
            #title = title.replace(u'\xa0', u'').replace('"', '').replace('...', '').replace('…', '').replace('|', '').replace('\'', '').replace(',', '').replace('(', '_').replace(')', '_').replace(' ', '_')
            title = self.clean_str(title)
            url = entry1.a['href']
            author = entry.find(class_="gs_a").text
            quote = entry.find(class_ = "gs_fl")
            for q in quote.find_all("a"):
                if (q.text.find("Цитируется")!=-1):
                    count_quote = int(q.text[q.text.find(":")+2:len(q.text)])
            results.append({"title": title, "url": url, "type": type, "author": author, "count_quote": count_quote, "rating": page_ / 10 + 1})
        #print(results)

    # поиск сайтов (гугл)
    def get_sites_google(self, url, results, page_):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')            
        k = 1 
        for entry in soup.find_all("div", attrs={"class": "kCrYT"}):
            #if k%2 != 0:
            if entry.a:
                if entry.a.text != "Картинки":
                    if entry.a.text.find('Результаты поиска по') == -1:                        
                        # если это не статья и не книга, то добавляем
                        if entry.a.text.find('[PDF]') == -1 and entry.a.text.find('books.google') == -1:
                            url = entry.a['href'].replace('/url?q=', '')
                            url = url[0:url.find('&sa=')].strip()
                            if entry.h3:
                                #title = entry.h3.text.replace(u'\xa0', u'').replace('"', '').replace('...', '').replace('…', '').replace('|', '').replace('\'', '').replace(',', '').replace('(', '_').replace(')', '_').replace(' ', '_')
                                title = self.clean_str(entry.h3.text)
                            else:
                                title = self.clean_str(entry.a.text)
                                #title = entry.a.text.replace(u'\xa0', u'').replace('"', '').replace('...', '').replace('…', '').replace('|', '').replace('\'', '').replace(',', '').replace('(', '_').replace(')', '_').replace(' ', '_')
                            results.append({"title": title, "url": url, "type": "САЙТ", "author": [], "rating": page_ / 10 + 1})                            
                else:
                    k -= 1
            else:
                k -= 1
            k += 1       

    # деление авторов по отдельности (статьи)
    def splitArticleAuthors(self, searchArticleResult):
        for i in searchArticleResult:
            result = []
            author = ""
            for char in i['author']:
                if char == ',':
                    result.append(author.replace(u'\xa0', u'').strip())
                    author = ""
                elif char == '-':
                    result.append(author.replace(u'\xa0', u'').strip())
                    i['author'] = result
                    break
                else:
                    author += char
    
    # деление авторов по отдельности (книги)
    def splitBooksResult(self, searchBookResult):
        for i in searchBookResult:
            result = []
            author = i['author'] 
            index = author.find(":")
            if index != -1:
                author = author[index+1:len(author)].strip()
            else:
                author = author.strip()
            index = author.find("(")
            if index != -1:
                #i['author'] = author[0:index].strip()
                result.append(author[0:index].strip())
            elif author == "":
                #i['author'] = "Не_найден"
                result.append("Не найден")
            else:    
                #i['author'] = author.strip()
                result.append(author.strip())
            i['author'] = result

    # поиск результатов
    def search(self, max_page, typeSearch):
        page_ = 0
        i = 0
        results = []
        self.typeSearch = typeSearch

        while page_ < max_page * 10:            
            if self.typeSearch is search.Books:
                url = 'https://www.google.com/search?q=' + self.query + '&tbm=bks&sxsrf=ALeKk001DXhruKQYY1Rr2PCCAv-m_VLOfg:1613307363334&ei=4x0pYPXnE-HHrgTU26XAAw&start=' + str(page_) + '&sa=N&ved=0ahUKEwi15beitunuAhXho4sKHdRtCTg4ChDy0wMIdw&biw=896&bih=754&dpr=1.25'
                self.get_books(url, results, i, page_)
            elif self.typeSearch is search.Articles:
                url = 'https://scholar.google.com/scholar?start=' + str(page_) + '&q=' + self.query + '&hl=ru&as_sdt=1,5&as_vis=1'
                self.get_articles(url, results, page_)     
            elif self.typeSearch is search.Sites:
                url = 'https://www.google.com/search?q=' + self.query + '&rlz=1C1PNBB_ruRU900RU900&sxsrf=ALeKk03WBG-UBqflFo50CcZjNZ2Uy8rEdA:1613941804874&ei=LMwyYKnvNLSMwPAP27iFqA0&start=' + str(page_) + '&sa=N&ved=2ahUKEwiptd7f8fvuAhU0BhAIHVtcAdU4FBDy0wN6BAgEEDo&biw=896&bih=754'  
                self.get_sites_google(url, results, page_)
            i = len(results)   
            page_ += 10
 
        #print(results)

        if self.typeSearch is search.Books:
            self.splitBooksResult(results)
        elif self.typeSearch is search.Articles:
            self.splitArticleAuthors(results)

        return results

# Запрос к онтологии
class SparqlQueries:
    def __init__(self, path, typeSearch):
        self.typeSearch = typeSearch
        my_world = World()
        #path to the owl file is given here
        my_world.get_ontology(path).load()
        #sync_reasoner(my_world)  #reasoner is started and synchronized here
        self.graph = my_world.as_rdflib_graph()

    # получение книг по названию
    def getBooksOfNames(self, title):
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?title " \
                "WHERE { " \
                "?title rdf:type pln:Книги. " \
                "FILTER regex(STR(?title), " + "\"" + title + "\"" + ")" \
                "}"
        
        resultsList = self.graph.query(query)

        titles = []

        for item in resultsList:
            title = str(item['title'].toPython())
            title = re.sub(r'.*#',"", title)
            
            titles.append(title)
        
        print(titles)
        return titles

    # получение классов для подклассов
    def getSubClasses(self):
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?subject ?object " \
                "WHERE { " \
                "?subject rdfs:subClassOf ?object" \
                "}"
        
        resultsList = self.graph.query(query)

        response = {}

        for item in resultsList:
            subj = str(item['subject'].toPython())
            subj = re.sub(r'.*#',"",subj)
            obj = str(item['object'].toPython())
            obj = re.sub(r'.*#',"",obj)
            #response.append({subj: obj})
            response[subj] = obj
        
        #print(response)
        return response


    # получаем книги
    def getBooksOrArticlesOrSites(self):

        # получаем темы и авторов у книги или статьи
        def getTitleThemesAndAuthors(title):
            
            if self.typeSearch is search.Books:
                property1 = "КнигаНаписанаПро"
                property2 = "КнигаНаписанаАвтором"
            elif self.typeSearch is search.Articles:
                property1 = "СтатьяНаписанаПро"
                property2 = "СтатьяНаписанаАвтором"
            elif self.typeSearch is search.Sites:
                property1 = "СайтНаписанПро"


            queryThemes = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?theme " \
                "WHERE { " \
                "pln:" + title + " pln:" + property1 + " ?theme." \
                "}"
            
            # у сайтов нет авторов
            if self.typeSearch != search.Sites:
                queryAuthors = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                    "SELECT ?author " \
                    "WHERE { " \
                    "pln:" + title + " pln:" + property2 + " ?author." \
                    "}"
            
            themes = []
            authors = []

            #query is being run
            try:
                resultsThemes = self.graph.query(queryThemes)
            except Exception:
                print("тут ошибка: ", title)
            else:
                for item in resultsThemes:
                    theme = str(item['theme'].toPython())
                    theme = re.sub(r'.*#',"", theme)
                    themes.append(theme)
            
            if self.typeSearch != search.Sites:
                try:
                    resultsAuthors = self.graph.query(queryAuthors)
                except Exception:
                    print("тут ошибка: ", title)
                else:
                    for item in resultsAuthors:
                        author = str(item['author'].toPython())
                        author = re.sub(r'.*#',"", author)
                        authors.append(author)

            return themes, authors


        if self.typeSearch is search.Books:
            vid = "Книги"
        elif self.typeSearch is search.Articles:
            vid = "Статьи"
        else:
            vid = "Сайты"

        queryTitle = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?title " \
                "WHERE { " \
                "?title rdf:type pln:" + vid + "." \
                "}"

        #query is being run
        resultsList = self.graph.query(queryTitle)

        #creating json object
        response = []

        for item in resultsList:
            title = str(item['title'].toPython())
            title = re.sub(r'.*#',"", title)
            themes, authors = getTitleThemesAndAuthors(title)
            
            if themes != [] or authors != []:
                response.append({'book' : title, 'themes': themes, 'authors': authors})

        print(response) #just to show the output
        return response

    # поиск 
    def search(self):
        
        response = self.getBooksOrArticlesOrSites()

        return response

    # получение класса у объекта
    def getClassOfObj(self, item):
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?class " \
                "WHERE { " \
                "pln:" + item + " rdfs:subClassOf ?class" \
                "}"
        
        resultsList = self.graph.query(query)

        for item in resultsList:
            c = str(item['class'].toPython())
            c = re.sub(r'.*#',"",c)
        
        return c

# добавление результатов в онтологию
class WorkWithOntology:
    def __init__(self, path):
        onto_path.append(path)
        self.onto = get_ontology(path)
        self.onto.load()
        self.onto.save(path)
        self.path = path
    
    # получаем поисковую строку из того что ввели
    def getQuery(self, query, typeSearch):
        runQuery = SparqlQueries(self.path, typeSearch)
        resList = runQuery.getSubClasses()
        del runQuery
        levs = [(key, Levenshtein.ratio(query, key)) for key in resList.keys()]
        key, score = max(levs, key=lambda lev: lev[1])
        return key

    # получаем темы для статьи или книги(про что написано)
    def getAllThemes(self, query, typeSearch):
        runQuery = SparqlQueries(self.path, typeSearch)
        resultThemes = []
        resList = runQuery.getSubClasses()
        del runQuery
        checkList = ['СкульптураЗерна', 'ФормаЗерна', 'СоставЗерна', 'ТипыЗеренВЗависимостиОтПолярности', 'ФормированиеЗерна', 'ПыльцевыеЗерна']
        resultThemes.append(query)
        while True:
            levs = [(key, Levenshtein.ratio(query, key)) for key in resList.keys()]
            key, score = max(levs, key=lambda lev: lev[1])
            query = resList.get(key)
            resultThemes.append(query)
            if query in checkList:
                break 
        return resultThemes

    # делим список на части
    def SplitList(self, item):
        authors = item.get('author')
        title = item.get('title')
        url = item.get('url')
        type = item.get('type')
        rating = item.get('rating')
        return title, authors, url, type, rating

    # запись в онтологию книги или статьи
    def RecordingBookOrArticle(self, title, authors, url, type, rating):          
        with self.onto:
            class Авторы(Thing):
                pass
            class Статьи(Thing):
                pass
            class Книги(Thing):
                pass
            class Сайты(Thing):
                pass
        
        if type == "СТАТЬЯ":                
            for author in authors:  
                new_aut = Авторы(author.replace(' ', '_'))  
                new_title = Статьи(title.replace(' ', '_'))
                new_aut.АвторСтатьи.append(new_title)
                new_title.СтатьяНаписанаАвтором.append(new_aut)
                new_title.URL_article = url
                new_title.rating_article.append(rating)
                              
        elif type == "КНИГА": 
            for author in authors:
                new_aut = Авторы(author.replace(' ', '_'))  
                new_title = Книги(title.replace(' ', '_'))
                new_aut.АвторКниги.append(new_title)
                new_title.КнигаНаписанаАвтором.append(new_aut)
                new_title.URL_book = url
                new_title.rating_book.append(rating)
        
        elif type == "САЙТ":
            new_site = Сайты(title.replace(' ', '_'))
            new_site.URL_site = url
            new_site.rating_site.append(rating)

        self.onto.save(self.path) 

    # запись в онтологию книг или статей с их тематиками
    def RecordingResultsWithThemes(self, resultsList, resultThemes):            

        # проверка на существование этой книги или статьи в онтологии
        def CheckExist(item):
            existList = self.onto.search(iri = "*" + item)
            if existList == []:
                return False
            return True 

        with self.onto:    
            class Авторы(Thing):
                pass
            class Статьи(Thing):
                pass
            class Книги(Thing):
                pass
            class Сайты(Thing):
                pass
        
        #checkList = ['Борозды', 'Лептомы', 'Поры', 'Руги', 'Щели', 'Бороздно-оровые', 'Бороздно-поровые', 'Порово-оровые', '',]
        for item in resultsList:
            title, authors, url, type, rating = self.SplitList(item)
            
            if CheckExist(title.replace(' ', '_')) == False:
                self.RecordingBookOrArticle(title, authors, url, type, rating)
                global countNewItem
                countNewItem += 1
            for theme in resultThemes:             
                typeClass = theme
                class_var =  self.onto[typeClass]
                                
                if type == "КНИГА":
                    for author in authors:
                        new_aut = Авторы(author.replace(' ', '_'))
                        new_title = Книги(title.replace(' ', '_'))
                        new_aut.ПисалПро.append(class_var)
                        new_title.КнигаНаписанаПро.append(class_var)
                        new_title.rating_book.append(rating)
                elif type == "СТАТЬЯ": 
                    count_quote = item.get('count_quote')
                    for author in authors:
                        new_aut = Авторы(author.replace(' ', '_')) 
                        new_title = Статьи(title.replace(' ', '_'))
                        new_aut.ПисалПро.append(class_var)
                        new_title.СтатьяНаписанаПро.append(class_var)
                        new_title.Count_quotes.append(count_quote)
                        new_title.rating_article.append(rating)
                elif type == "САЙТ":
                    new_site = Сайты(title.replace(' ', '_'))
                    new_site.СайтНаписанПро.append(class_var)
                    new_site.rating_site.append(rating)

                self.onto.save(self.path) 


from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'kroscho':
        return 'kros'
    return None

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

app = Flask(__name__)
CORS(app)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
#@auth.login_required
def main():

    # деление строки по словам
    def splitQuery(query):
        result = ""
        for char in query:
            if char == char.upper():
                result += " " + char.lower()
            else:
                result += char
        return result

    #query = "палинология пыльцевое зерно"
    path = r"D:\Desktop\ПМИ\3_курс\Курсовая\Бот\polynology.owl"
    max_page = 3
    typeSearch = search.Articles

        
    # запрос к онтологии
    #runQuery = SparqlQueries(path, typeSearch)
    #data = runQuery.search()
    #print(data)
    #return json.dumps(data, ensure_ascii=False)

    
    # работа с онтологией
    addRes = WorkWithOntology(path)
    query = addRes.getQuery("вегетативные клетки зерна", typeSearch)
    #print(query)
    themesList = addRes.getAllThemes(query, typeSearch)
    #print(themesList)
    query += " пыльцевое зерно"
    query = "палинология пыльцевое зерно"
    query = splitQuery(query)
    #print(query)
    
    # поиск с гугла
    searchRes = SearchResult(query)
    searchResList = searchRes.search(max_page, typeSearch)
    print(searchResList)
    del searchRes

    addRes.RecordingResultsWithThemes(searchResList, themesList)
    print(countNewItem)
    del addRes
    

    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.search()
    data = json.dumps(data, ensure_ascii=False)
    #data = runQuery.getBooksOfNames("Пал")
    print(data)
    return data
    

if __name__ == "__main__":
    #main()
    app.run(debug = True)