from owlready2 import *
from enum import Enum
import json
from datetime import datetime
import hashlib
import os

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
        self.path = path

    # получение книг по теме и не раньше выбранной даты
    def getBooksByThemesAndDate(self, theme, date, typeSearch):

        if typeSearch is search.Books:
            property = "КнигаНаписанаПро"
            prop = "rating_book"
            prop1 = "date_book"
            str1 = "[Книга] "
        elif typeSearch is search.Articles:
            property = "СтатьяНаписанаПро"
            prop = "rating_article"
            prop1 = "date_article"
            str1 = "[Статья] "
        elif typeSearch is search.Sites:
            property = "СайтНаписанПро"
            prop = "rating_site"
            prop1 = "date_site"
            str1 = "[Сайт] "

        print(date)
        print("FILTER(?day > ", date, "). ")
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
            "SELECT ?title ?day " \
            "WHERE { " \
            "?title pln:" + property + " pln:" + theme + ". " \
            "?title pln:" + prop1 + " ?day. " \
            "FILTER(?day > \"" + date + "\"^^xsd:dateTime). " \
            "} " \
            
        
        #print(query)
    
        resultsList = self.graph.query(query)

        response = []

        for item in resultsList:
            title = str(item['title'].toPython())
            title = re.sub(r'.*#',"", title)
            themes, authors, url = self.getTitleThemesAndAuthors(title, typeSearch)
            
            if themes != [] or authors != []:
                response.append({'book' : str1 + title, 'themes': themes, 'authors': authors, 'url': url})
        
        return response

    # получение статей по теме и дате
    def getArticlesByThemesAndDate(self, theme, date, typeSearch):
        return self.getBooksByThemesAndDate(theme, date, typeSearch)

    # получение сайтов по теме и дате
    def getSitesByThemesAndDate(self, theme, date, typeSearch):
        return self.getBooksByThemesAndDate(theme, date, typeSearch)

    # получение книг по теме ( и если нужно, по дате)
    def getBooksByThemes(self, theme):

        if self.typeSearch is search.Books:
            property = "КнигаНаписанаПро"
            prop = "rating_book"
        elif self.typeSearch is search.Articles:
            property = "СтатьяНаписанаПро"
            prop = "rating_article"
        elif self.typeSearch is search.Sites:
            property = "СайтНаписанПро"
            prop = "rating_site"
        elif self.typeSearch is search.Authors:
            property = "ПисалПро"

        if self.typeSearch is search.Books or self.typeSearch is search.Articles or self.typeSearch is search.Sites:
            query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?title ?rating " \
                "WHERE { " \
                "?title pln:" + property + " pln:" + theme + ". " \
                "?title pln:" + prop + " ?rating" \
                "} " \
                "ORDER BY (?rating)"
        
            resultsList = self.graph.query(query)

            response = []

            for item in resultsList:
                title = str(item['title'].toPython())
                title = re.sub(r'.*#',"", title)
                themes, authors, url = self.getTitleThemesAndAuthors(title, self.typeSearch)
                
                if themes != [] or authors != []:
                    response.append({'book' : title, 'themes': themes, 'authors': authors, 'url': url})
        
        else:
            query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?author " \
                "WHERE { " \
                "?author pln:" + property + " pln:" + theme + ". " \
                "} "
            #print(query)
        
            resultsList = self.graph.query(query)

            response = []

            for item in resultsList:
                author = str(item['author'].toPython())
                author = re.sub(r'.*#',"", author)
                themes, items, url = self.getAuthorThemesAndBooks(author)
                
                #if themes != [] or items != []:
                response.append({'book' : author, 'themes': themes, 'authors': items, 'url': url})
        
        return response

    # получение статей по теме
    def getArticlesByThemes(self, theme):
        return self.getBooksByThemes(theme)

    # получение сайтов по теме
    def getSitesByThemes(self, theme):
        return self.getBooksByThemes(theme)

    # получение авторов по теме
    def getAuthorsByThemes(self, theme):
        return self.getBooksByThemes(theme)

    # получение книг по названию
    def getBooksByNames(self, title):

        if self.typeSearch is search.Books:
            property = "Книги"
            prop = "rating_book"
        elif self.typeSearch is search.Articles:
            property = "Статьи"
            prop = "rating_article"
        elif self.typeSearch is search.Sites:
            property = "Сайты"
            prop = "rating_site"

        title = title.lower()
        if title != "":
            query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                    "SELECT ?title ?rating" \
                    "WHERE { " \
                    "?title rdf:type pln:" + property + ". " \
                    "FILTER regex(lcase(STR(?title)), " + "\"" + title + "\"" + ")" \
                    "}"
        else:
            print("ОУУУУУУУУУУ")
            query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?title ?rating " \
                "WHERE { " \
                "?title rdf:type pln:" + property + "." \
                "?title pln:" + prop + " ?rating" \
                "} " \
                "ORDER BY (?rating)"
        
        resultsList = self.graph.query(query)

        response = []

        for item in resultsList:
            title = str(item['title'].toPython())
            title = re.sub(r'.*#',"", title)
            themes, authors, url = self.getTitleThemesAndAuthors(title, self.typeSearch)
            
            if themes != [] or authors != []:
                response.append({'book' : title, 'themes': themes, 'authors': authors, 'url': url})
        
        return response

    # получение статей по названию
    def getArticlesByNames(self, title):
        return self.getBooksByNames(title)

    # получение статей по названию
    def getSitesByNames(self, title):
        return self.getBooksByNames(title)

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

    # получаем темы и авторов у книги или статьи
    def getTitleThemesAndAuthors(self, title, typeSearch):
        
        if typeSearch is search.Books:
            property1 = "КнигаНаписанаПро"
            property2 = "КнигаНаписанаАвтором"
            property3 = "URL_book"
        elif typeSearch is search.Articles:
            property1 = "СтатьяНаписанаПро"
            property2 = "СтатьяНаписанаАвтором"
            property3 = "URL_article"
        elif typeSearch is search.Sites:
            property1 = "СайтНаписанПро"
            property3 = "URL_site"


        queryThemes = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
            "SELECT ?theme ?url" \
            "WHERE { " \
            "pln:" + title + " pln:" + property1 + " ?theme. " \
            "pln:" + title + " pln:" + property3 + " ?url. " \
            "}"
        
        # у сайтов нет авторов
        if typeSearch != search.Sites:
            queryAuthors = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?author " \
                "WHERE { " \
                "pln:" + title + " pln:" + property2 + " ?author." \
                "}"
        
        themes = []
        authors = []
        url_list = []

        #query is being run
        try:
            resultsThemes = self.graph.query(queryThemes)
        except Exception:
            print("тут ошибка: ", title)
        else:
            for item in resultsThemes:
                theme = str(item['theme'].toPython())
                theme = re.sub(r'.*#',"", theme)
                #print("_-_-_-_-_-_-_-_-_-__-_-__-__-_-: ", item)
                #url = str(item['url'].toPython())
                #url = re.sub(r'.*#',"", url)
                themes.append(theme)
                #url_list.append(url)
            
        
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

        return themes, authors, url_list

    # получаем книги
    def getBooksOrArticlesOrSites(self):

        if self.typeSearch is search.Books:
            vid = "Книги"
            prop = "rating_book"
        elif self.typeSearch is search.Articles:
            vid = "Статьи"
            prop = "rating_article"
        else:
            vid = "Сайты"
            prop = "rating_site"

        queryTitle = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?title ?rating " \
                "WHERE { " \
                "?title rdf:type pln:" + vid + "." \
                "?title pln:" + prop + " ?rating" \
                "} " \
                "ORDER BY (?rating)"

        #query is being run
        resultsList = self.graph.query(queryTitle)

        #creating json object
        response = []

        for item in resultsList:
            title = str(item['title'].toPython())
            title = re.sub(r'.*#',"", title)
            themes, authors = self.getTitleThemesAndAuthors(title, self.typeSearch)
            
            if themes != [] or authors != []:
                response.append({'book' : title, 'themes': themes, 'authors': authors})

        #print(response) 
        return response

    # поиск 
    def search(self):
        response = self.getBooksOrArticlesOrSites()
        return response

    # получаем темы и книги/статьи/сайты у автора
    def getAuthorThemesAndBooks(self, title):
        property1 = "ПисалПро"
        property2 = ["АвторКниги", "АвторСтатьи", "АвторВеб-Ресурса"]

        queryThemes = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
            "SELECT ?theme " \
            "WHERE { " \
            "pln:" + title + " pln:" + property1 + " ?theme." \
            "}"
        #print(queryThemes)

        queryItems = []

        for property in property2:
            queryItem = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?author " \
                "WHERE { " \
                "pln:" + title + " pln:" + property + " ?author." \
                "}"
            queryItems.append(queryItem)
        
        themes = []
        items = []
        url_list = []

        #query is being run
        try:
            resultsThemes = self.graph.query(queryThemes)
        except Exception:
            print("тут ошибка: ", title)
        else:
            for item in resultsThemes:
                theme = str(item['theme'].toPython())
                theme = re.sub(r'.*#',"", theme)
                #url = str(item['url'].toPython())
                #url = re.sub(r'.*#',"", url)
                themes.append(theme)
            
        for queryItem in queryItems:
            try:
                resultsBooks = self.graph.query(queryItem)
            except Exception:
                print("тут ошибка: ", title)
            else:
                for item in resultsBooks:
                    book = str(item['author'].toPython())
                    book = re.sub(r'.*#',"", book)
                    items.append(book)

        return themes, items, url_list

    def getAuthorsByNames(self, title):

        title = title.lower()
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?title ?rating" \
                "WHERE { " \
                "?title rdf:type pln:Авторы. " \
                "FILTER regex(lcase(STR(?title)), " + "\"" + title + "\"" + ")" \
                "}"
                
        resultsList = self.graph.query(query)

        response = []

        for item in resultsList:
            title = str(item['title'].toPython())
            title = re.sub(r'.*#',"", title)
            themes, items, url = self.getAuthorThemesAndBooks(title)
            
            #if themes != [] or items != []:
            response.append({'book' : title, 'themes': themes, 'authors': items, 'url': url})
        
        return response

    # получаем темы, существующие в онтологии
    def getThemes(self):
        
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?theme " \
                "WHERE { " \
                "?theme rdf:type pln:Темы. " \
                "}"
        
        resultsList = self.graph.query(query)

        response = []
        index = 1

        for item in resultsList:
            subj = str(item['theme'].toPython())
            subj = re.sub(r'.*#',"",subj)

            response.append({'value': "theme" + str(index), 'label': subj})
            index += 1

        return response

    # получаем данные для пользователя по его интересам
    def getDataForUser(self, user, date, typeResourse):
        
        data = []

        if user == "":
            
            interests = self.getAllThemes()
            for theme in interests:
                if typeResourse == "books":
                    data = (self.getBooksByThemesAndDate(theme, date, search.Books))
                elif typeResourse == "articles":
                    data = (self.getArticlesByThemesAndDate(theme, date, search.Articles))
                elif typeResourse == "sites":
                    data = (self.getSitesByThemesAndDate(theme, date, search.Sites))
                else:
                    data = [{'book' : "Поменяйте тип ресурса", 'themes': [], 'authors': [], 'url': []}]
            return data
        else:
            data1 = data2 = data3 = []
            interests = self.getInterestsOfUser(user)
            for theme in interests:
                data1 = (self.getBooksByThemesAndDate(theme, date, search.Books))
                data2 = (self.getArticlesByThemesAndDate(theme, date, search.Articles))
                data3 = (self.getSitesByThemesAndDate(theme, date, search.Sites))
            data = data1 + data2 + data3
            if data == []:
                interests = self.getAllThemes()
                for theme in interests:
                    data1 = (self.getBooksByThemesAndDate(theme, date, search.Books))
                    data2 = (self.getArticlesByThemesAndDate(theme, date, search.Articles))
                    data3 = (self.getSitesByThemesAndDate(theme, date, search.Sites))
                data = data1 + data2 + data3
            return data

    # получаем список всех тем
    def getAllThemes(self):
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?theme " \
                "WHERE { " \
                "?theme rdf:type pln:Темы. " \
                "}"
     
        resultsList = self.graph.query(query)

        interests = []

        for item in resultsList:
            theme = str(item['theme'].toPython())
            theme = re.sub(r'.*#',"", theme)
            
            interests.append(theme)
    
        return interests

    # проверяем наличие пользователя с таким логином и паролем
    def getUsers(self):

        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?user ?name ?surname ?placeOfWork ?login " \
                "WHERE { " \
                "?user pln:login ?login. " \
                "?user pln:names ?name. " \
                "?user pln:surname ?surname. " \
                "?user pln:placeOfWork ?placeOfWork. " \
                "}"
                
        resultsList = self.graph.query(query)

        response = []

        for item in resultsList:
            user = str(item['user'].toPython())
            user = re.sub(r'.*#',"", user)
            user_name = str(item['name'].toPython())
            user_name = re.sub(r'.*#',"", user_name)
            user_login = str(item['login'].toPython())
            user_login = re.sub(r'.*#',"", user_login)
            user_surname = str(item['surname'].toPython())
            user_surname = re.sub(r'.*#',"", user_surname)
            user_place = str(item['placeOfWork'].toPython())
            user_place = re.sub(r'.*#',"", user_place)             

            interests = self.getInterestsOfUser(user)
            roles = self.getRoleOfUser(user)
            response.append({'user': user, 'name': user_name, 'surname': user_surname, 'placeOfWork': user_place, 'interests': interests, 'roles': roles})
    
        return response

    # получаем список интересов нашего пользователя
    def getInterestsOfUser(self, user):
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
            "SELECT ?interests " \
            "WHERE { " \
            "pln:" + user + " pln:ПользовательИнтересуется ?interests. " \
            "}"

        print("User: ", user)        
        resultsList = self.graph.query(query)

        interests = []

        for item in resultsList:
            interest = str(item['interests'].toPython())
            interest = re.sub(r'.*#',"", interest)
            
            interests.append(interest)
    
        return interests

    # получаем список интересов нашего пользователя
    def getRoleOfUser(self, user):
        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
            "SELECT ?role " \
            "WHERE { " \
            "pln:" + user + " pln:role ?role. " \
            "}"
   
        resultsList = self.graph.query(query)

        roles = []

        for item in resultsList:
            role = str(item['role'].toPython())
            role = re.sub(r'.*#',"", role)
            
            roles.append(role)
    
        return roles

    # получаем пользователя по имени
    def getUserInterests(self, user):
        response = []
        interests = self.getInterestsOfUser(user)
        response.append({'interests': interests})
        return response

    # проверяем наличие пользователя с таким логином и паролем
    def checkUser(self, login, password):

        query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                "SELECT ?user ?name ?surname ?placeOfWork ?login ?hash ?role " \
                "WHERE { " \
                "?user pln:login ?login. " \
                "?user pln:hash ?hash. " \
                "?user pln:names ?name. " \
                "?user pln:surname ?surname. " \
                "?user pln:placeOfWork ?placeOfWork. " \
                "}"
                
        resultsList = self.graph.query(query)

        response = []

        for item in resultsList:
            user = str(item['user'].toPython())
            user = re.sub(r'.*#',"", user)
            user_name = str(item['name'].toPython())
            user_name = re.sub(r'.*#',"", user_name)
            user_login = str(item['login'].toPython())
            user_login = re.sub(r'.*#',"", user_login)
            user_password = str(item['hash'].toPython())
            user_password = re.sub(r'.*#',"", user_password)
            user_surname = str(item['surname'].toPython())
            user_surname = re.sub(r'.*#',"", user_surname)
            user_place = str(item['placeOfWork'].toPython())
            user_place = re.sub(r'.*#',"", user_place)             

            h = hashlib.md5(password.encode('utf-8'))

            if user_login == login and user_password == h.hexdigest():
                interests = self.getInterestsOfUser(user)
                roles = self.getRoleOfUser(user)
                response.append({'log': True, 'message': "Успешно!", 'login': login, 'user': user, 'name': user_name, 'surname': user_surname, 'placeOfWork': user_place, 'interests': interests, 'roles': roles})
                return response
    
        if response==[]:
            response.append({'log': False, 'message': "Логин или пароль неправильно набраны!"})
        return response

    # регистрируем пользователя
    def regUser(self, name, surname, placeOfWork, login, password):

        def check(login):
            query = "PREFIX pln: <http://www.semanticweb.org/nikita/ontologies/2021/0/untitled-ontology-27#>" \
                    "SELECT ?user ?name ?surname ?placeOfWork ?login ?password " \
                    "WHERE { " \
                    "?user pln:login ?login. " \
                    "}"
                    
            resultsList = self.graph.query(query)

            response = []

            for item in resultsList:
                user = str(item['user'].toPython())
                user = re.sub(r'.*#',"", user)
                user_login = str(item['login'].toPython())
                user_login = re.sub(r'.*#',"", user_login)

                if user_login == login:
                    return False
            return True

        if check(login):
            addUser = WorkWithOntology(self.path)
            #try:
            addUser.RecordingUser(name, surname, placeOfWork, login, password)
            #except Exception:
            #    print(Exception)
            #    return {'reg':False, 'message': "Неизвестная ошибка!"}
            #else:
            return {'reg': True, 'message': "Вы успешно зарегистрированы!"}
        else:
            return {'reg': False, 'message': "Пользователь с таким логином уже существует!"}


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
    
    # запись в онтологию книги или статьи
    def RecordingThemeInOntology(self, user, theme):

        def normilizeStr(str):
            str = str.strip()
            res = ""
            count_ = 0
            f = False
            for char in str:
                if char == ' ':
                    count_ += 1
                    f = False
                else:
                    f = True
                    if count_ == 1:
                        count_ = 0
                if count_ < 2:
                    res += char
                elif f:
                    res += char
                    count_ = 0
            str = res.strip()
            up = str[0].upper()
            str = up + str[1:]
            str = str.replace(' ', '__') + '__'
            '''
            while (str.find(' ') != -1):
                ind = str.find(' ')
                up = str[ind+1].upper()
                str = str[:ind] + up + str[ind+2:]
            '''
            return str
                   
        print(user)
        print(theme)
        with self.onto:
            class Темы(Thing):
                pass
            class Пользователи(Thing):
                pass
        
        theme = normilizeStr(theme)

        new_user = Пользователи(user)
        new_theme = Темы(theme)
        new_user.ПользовательИнтересуется.append(new_theme)

        self.onto.save(self.path) 
        return [{'message': "Успешно добавлено"}]

    # запись в онтологию пользователя
    def RecordingUser(self, nam, surname, placeOfWork, login, password):            

        with self.onto:    
            class Пользователи(Thing):
                pass
                
        new_user = Пользователи(login.replace(".", "_").replace("@", "_"))
        new_user.login = login
        new_user.names = nam
        new_user.surname = surname
        new_user.placeOfWork = placeOfWork
        new_user.role = "посетитель"

        h = hashlib.md5(password.encode('utf-8'))
        p = h.hexdigest()
        new_user.hash = p
        '''
        salt = os.urandom(32) # Запомните это
        print("  СОЛЬ: ", salt.decode('utf-8', 'backslashreplace'))
        
        key = hashlib.pbkdf2_hmac(
            'sha256', # Используемый алгоритм хеширования
            password.encode('utf-8'), # Конвертирование пароля в байты
            salt, # Предоставление соли
            100000, # Рекомендуется использоваться по крайней мере 100000 итераций SHA-256 
            dklen=128 # Получает ключ в 128 байтов
        )
        print("   ХЭШ: ", key.decode('utf-8', 'backslashreplace'))
        new_user.salt = salt.decode('utf-8', 'backslashreplace')
        new_user.hash = key.decode('utf-8', 'backslashreplace')
        '''

        self.onto.save(self.path) 

    # запись в онтологию пользователя
    def changeRole(self, user, role):            

        with self.onto:    
            class Пользователи(Thing):
                pass
        print("______________________________________________________________________________________________________")
        print("USER: ", user, "  ROLE: ", role)
        try:
            new_user = Пользователи(user)
            new_user.role = role
        except Exception:
            print("что то неверно")
            return [{'message': "Ошибка"}]
        else:
            print("все четко")
            self.onto.save(self.path)
            return [{'message': "Успешно"}] 
        


from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

path = r"D:\Desktop\ПМИ\3_курс\Курсовая\Готовое\psu-monitoring\api\polynology.owl"
#@auth.get_password
#def get_password(username):
 #   if username == 'kroscho':
 #       return 'kros'
 #   return None

#@auth.error_handler
#def unauthorized():
#    return jsonify({'error': 'Unauthorized access'}), 401

app = Flask(__name__)
CORS(app)

#@auth.login_required
@app.route('/pollen/api/search/books', methods=['GET'])
def getBooksByNames():
    typeSearch = search.Books
    search_string = request.args.get('search', '').replace(' ', '_')
    print(search_string)
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getBooksByNames(search_string)
    data = json.dumps(data, ensure_ascii=False)
    #print(data)
    return data

@app.route('/pollen/api/search/articles', methods=['GET'])
def getArticlesByNames():
    typeSearch = search.Articles
    search_string = request.args.get('search', '').replace(' ', '_')
    #print(search_string)
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getBooksByNames(search_string)
    data = json.dumps(data, ensure_ascii=False)
    #print(data)
    return data

@app.route('/pollen/api/search/sites', methods=['GET'])
def getSitesByNames():
    typeSearch = search.Sites
    search_string = request.args.get('search', '').replace(' ', '_')
    #print(search_string)
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getBooksByNames(search_string)
    data = json.dumps(data, ensure_ascii=False)
    #print(data)
    return data

@app.route('/pollen/api/search/authors', methods=['GET'])
def getAuthorsByNames():
    search_string = request.args.get('search', '').replace(' ', '_')
    typeSearch = search.Sites
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getAuthorsByNames(search_string)
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

@app.route('/pollen/api/search/theme/books', methods=['GET'])
def getBooksByThemes():
    typeSearch = search.Books
    search_string = request.args.get('search', '')
    print(search_string)
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getBooksByThemes(search_string)
    data = json.dumps(data, ensure_ascii=False)
    #print(data)
    return data

@app.route('/pollen/api/search/theme/articles', methods=['GET'])
def getArticlesByThemes():
    typeSearch = search.Articles
    search_string = request.args.get('search', '')
    print(search_string)
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getArticlesByThemes(search_string)
    data = json.dumps(data, ensure_ascii=False)
    #print(data)
    return data

@app.route('/pollen/api/search/theme/sites', methods=['GET'])
def getSitesByThemes():
    typeSearch = search.Sites
    search_string = request.args.get('search', '')
    print(search_string)
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getSitesByThemes(search_string)
    data = json.dumps(data, ensure_ascii=False)
    #print(data)
    return data

@app.route('/pollen/api/search/theme/authors', methods=['GET'])
def getAuthorsByThemes():
    typeSearch = search.Authors
    search_string = request.args.get('search', '')
    print(search_string)
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getAuthorsByThemes(search_string)
    data = json.dumps(data, ensure_ascii=False)
    #print(data)
    return data

@app.route('/pollen/api/login', methods=['GET'])
def getUser():
    typeSearch = search.Authors
    login = request.args.get('login', '')
    password = request.args.get('password', '')
    if (login == "" or password == ""):
        data = [{'log': False, 'message': "Введите все поля!"}]
        data = json.dumps(data, ensure_ascii=False)
        return data
    if (login.find('@') == -1):
        data = [{'log': False, 'message': "Логин должен содержать: @!"}]
        data = json.dumps(data, ensure_ascii=False)
        return data
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.checkUser(login, password)
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

@app.route('/pollen/api/reg', methods=['GET'])
def regUser():
    typeSearch = search.Authors
    name = request.args.get('name', '')
    surname = request.args.get('surname', '')
    placeOfWork = request.args.get('placeOfWork', '')
    login = request.args.get('login', '')
    password = request.args.get('password', '')
    if (name == "" or surname == "" or login == "" or password == ""):
        data = {'reg': False, 'message': "Введите все обязательные поля!"}
        data = json.dumps(data, ensure_ascii=False)
        return data
    if login.find('@') == -1:
        data = {'reg':False, 'message': "Логин должен содержать: @"}
        data = json.dumps(data, ensure_ascii=False)
        return data
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.regUser(name, surname, placeOfWork, login, password)
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

@app.route('/pollen/api/theme/add', methods=['GET'])
def addTheme():
    typeSearch = search.Authors
    theme = request.args.get('theme', '')
    user = request.args.get('user', '')
    print(user)
    print(theme)
    if theme != "":
        # запрос к онтологии
        runQuery = WorkWithOntology(path)
        data = runQuery.RecordingThemeInOntology(user, theme)
        data = json.dumps(data, ensure_ascii=False)
        print(data)
        return data
    else:
        data = [{'message': "Ошибка"}]
        data = json.dumps(data, ensure_ascii=False)
        print(data)
        return data    
    
@app.route('/pollen/api/get/themes', methods=['GET'])
def getThemes():
    typeSearch = search.Authors
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getThemes()
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

@app.route('/pollen/api/get/user_interests', methods=['GET'])
def getUserInterests():
    typeSearch = search.Authors
    user = request.args.get('user', '')
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getUserInterests(user)
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

@app.route('/pollen/api/get/users', methods=['GET'])
def getUsers():
    typeSearch = search.Authors
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getUsers()
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

@app.route('/pollen/api/change/role', methods=['GET'])
def changeRoleByUser():
    typeSearch = search.Authors
    user = request.args.get('user', '')
    role = request.args.get('role', '')
    # запрос к онтологии
    #runQuery = SparqlQueries(path, typeSearch)
    addUser = WorkWithOntology(path)
    data = addUser.changeRole(user, role)
    #data = runQuery.changeRole(user, role)
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

@app.route('/pollen/api/get/data', methods=['GET'])
def getDataForUser():
    typeSearch = search.Authors
    user = request.args.get('user', '')
    date = request.args.get('date', '')
    if date != "":
        day = date[8:10]
        year = date[11:15]
        month = date[4:7]
        if month == "Apr":
            month = "04"
    else:
        now = datetime.now()
        if now.day > 3:
            day = now.day - 3
        else:
            day = 30 - (3 - now.day)
        year = now.year
        month = now.month

    strDate = datetime(int(year), int(month), int(day), 0, 0, 0).isoformat()
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getDataForUser(user, strDate, typeSearch)
    if data == []:
        data = [{"book": "no", "themes": [], "authors": [], "url": []}]
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

@app.route('/pollen/api/get/all_data', methods=['GET'])
def getDataByDate():
    typeSearch = request.args.get('typeSearch', '')
    date = request.args.get('date', '')
    user = ""
    if date != "":
        day = date[8:10]
        year = date[11:15]
        month = date[4:7]
        if month == "Apr":
            month = "04"
    else:
        now = datetime.now()
        if now.day > 3:
            day = now.day - 3
        else:
            day = 30 - (3 - now.day)
        year = now.year
        month = now.month

    strDate = datetime(int(year), int(month), int(day), 0, 0, 0).isoformat()
    # запрос к онтологии
    runQuery = SparqlQueries(path, typeSearch)
    data = runQuery.getDataForUser(user, strDate, typeSearch)
    if data == []:
        data = [{"book": "no", "themes": [], "authors": [], "url": []}]
    data = json.dumps(data, ensure_ascii=False)
    print(data)
    return data

if __name__ == "__main__":
    app.run(debug = True)