from asyncio.windows_events import NULL
from re import I
from itsdangerous import json
from owlready2 import *
from enum import Enum
from datetime import datetime
import copy

path_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(path_dir)
print(path_dir)

from testing.sparqlQueries.config import config
import testing.sparqlQueries.queries as queries
from testing.sparqlQueries.utils import checkAnswer, checkCorrectAnswer, getTermFromText, getTokensFromTexts, getTypeTaskValue
from testing.sparqlQueries.autoGeneration import AutoGeneration, typeTemplate

# тип ответа на вопрос
class typeTask(Enum):
    Text = "1"
    Single = "2"
    Multiple = "3"
    TrueFalse = "4"

class TestingService:
    def __init__(self) -> None:
        onto_path.append(config['path'])
        self.path = config['path']
        self.onto = get_ontology(self.path)
        self.onto.load()
        
        my_world = World()
        my_world.get_ontology(self.path).load()
        self.graph = my_world.as_rdflib_graph()
            
    def createTest(self, test, module):

        with self.onto:
            class Тест(Thing):
                pass
            class Модуль(Thing):
                pass
            class Группа_заданий(Thing):
                pass
            class Задание(Thing):
                pass 
            class Вопрос(Задание):
                pass
            class Единственный(Вопрос):
                pass
            class Множественный(Вопрос):
                pass
            class Текстовый(Вопрос):
                pass
            class Логический(Вопрос):
                pass
            class Ответ(Задание):
                pass
            class Термин(Thing):
                pass

        newTest = Тест()
        newGroupOfTasks = Группа_заданий()
        module = Модуль(module["moduleObj"])

        newTest.testName = test['testName']
        listTasks = test['tasks']
        term = {}

        for task in listTasks:
            newTask = Задание()
            newQuestion = Вопрос()
            tTask = task['type']
            if tTask == typeTask.Text.value:
                newQuestion = Текстовый()
                newQuestion.textQuestion = task['question']
                #term = self.getTermByTask(task)
            else:
                if tTask == typeTask.Single.value:
                    newQuestion = Единственный()
                elif tTask == typeTask.Multiple.value:
                    newQuestion = Множественный()
                else:
                    newQuestion = Логический()

                newQuestion.textQuestion = task['question']
                #term = self.getTermByTask(task)
                if "answers" in task:
                    listAnswers = task['answers']
                    for answ in listAnswers:
                        newAnswer = Ответ()
                        newAnswer.textAnswer = answ['answer']
                        if "correct" in answ and answ['correct']:
                            newQuestion.has_correct_answer.append(newAnswer)
                            newAnswer.is_correct_answer_of.append(newQuestion)
                        else:
                            newQuestion.has_wrong_answer.append(newAnswer)
                            newAnswer.is_wrong_answer_of.append(newQuestion)
                        newTask.task_has_answer.append(newAnswer)
            newTask.task_has_question = newQuestion
            newTask.is_task_of.append(newGroupOfTasks)
            term = task["term"]
            termObj = Термин(term)
            newTask.hasTerm = termObj
        
        newTest.has_group_of_task.append(newGroupOfTasks)
        newGroupOfTasks.is_group_of_task.append(newTest)
        module.has_test.append(newTest)
        newTest.is_test_of.append(module)

        self.onto.save(self.path) 

    def createLecture(self, nameLecture, moduleObj, selectedTerms):

        with self.onto:
            class Модуль(Thing):
                pass
            class Лекция(Thing):
                pass
            class Термин(Thing):
                pass

        newLecture = Лекция()
        module = Модуль(moduleObj)

        newLecture.lectureName = nameLecture
        newLecture.is_lecture_of.append(module)
        module.has_lecture.append(newLecture)

        for termObj in selectedTerms:
            term = Термин(termObj)
            newLecture.has_term.append(term)
            term.is_term_of.append(newLecture)

        self.onto.save(self.path) 

    def createCourse(self, courseObj):
        with self.onto:
            class Курс(Thing):
                pass

        newCourse = Курс()
        
        newCourse.nameCourse = courseObj['title']
        newCourse.descriptionCourse = courseObj['description']
        newCourse.infoCourse = courseObj['info']
        
        self.onto.save(self.path) 

    def createModule(self, module, courseObj):
        with self.onto:
            class Курс(Thing):
                pass
            class Модуль(Thing):
                pass
            class Область(Thing):
                pass

        course = Курс(courseObj)
        subArea = Область(module["subjectArea"])
        newModule = Модуль()

        newModule.nameModule = module['nameModule']
        newModule.has_subject_area = subArea
        course.has_module.append(newModule)
        newModule.is_module_of.append(course)
        
        self.onto.save(self.path) 

    def checkNameTest(self, testName):        
        query = queries.getTestsNames()
        resultsTests = self.graph.query(query)
        for itemTest in resultsTests:
            nameTest = str(itemTest['nameTest'].toPython())
            nameTest = re.sub(r'.*#',"", nameTest)
            if nameTest == testName:
                return True
        return False

    def checkNameCourse(self, courseName):        
        query = queries.getCoursesNames()
        resultsCourses = self.graph.query(query)
        for itemTest in resultsCourses:
            nameCourse = str(itemTest['courseName'].toPython())
            nameCourse = re.sub(r'.*#',"", nameCourse)
            if nameCourse == courseName:
                return True
        return False

    def updateTest(self, updateTest):
        with self.onto:
            class Тест(Thing):
                pass
            class Группа_заданий(Thing):
                pass
            class Задание(Thing):
                pass
            class Вопрос(Задание):
                pass
            class Единственный(Вопрос):
                pass
            class Множественный(Вопрос):
                pass
            class Текстовый(Вопрос):
                pass
            class Логический(Вопрос):
                pass
            class Ответ(Задание):
                pass
            class Термин(Thing):
                pass
        
        term = {}
        query = queries.getTestsNames()
        resultsTests = self.graph.query(query)
        for itemTest in resultsTests:
            nameTest = str(itemTest['nameTest'].toPython())
            nameTest = re.sub(r'.*#',"", nameTest)
            testObj = str(itemTest['testObj'].toPython())
            testObj = re.sub(r'.*#',"", testObj)
            if nameTest != updateTest['prevNameTest']:
                continue
            groupTask = str(itemTest['groupTasks'].toPython())
            groupTask = re.sub(r'.*#',"", groupTask)
            groupTaskObj = Группа_заданий(groupTask)
            print("GROUP TASK: ", groupTaskObj)
            if updateTest['prevNameTest'] != updateTest['testName']:
                curTest = Тест(testObj)
                curTest.testName = updateTest['testName']

            self.deleteTasks(groupTask)
            
            for task in updateTest['tasks']:
                newTask = Задание()
                newQuestion = Вопрос()
                tTask = task['type']
                if tTask == typeTask.Text.value:
                    newQuestion = Текстовый()
                    newQuestion.textQuestion = task['question']
                    #term = self.getTermByTask(task)
                else:
                    if tTask == typeTask.Single.value:
                        newQuestion = Единственный()
                    elif tTask == typeTask.Multiple.value:
                        newQuestion = Множественный()
                    else:
                        newQuestion = Логический()

                    newQuestion.textQuestion = task['question']
                    #term = self.getTermByTask(task)
                    if "answers" in task:
                        listAnswers = task['answers']
                        for answ in listAnswers:
                            newAnswer = Ответ()
                            newAnswer.textAnswer = answ['answer']
                            if "correct" in answ and answ['correct']:
                                newQuestion.has_correct_answer.append(newAnswer)
                                newAnswer.is_correct_answer_of.append(newQuestion)
                            else:
                                newQuestion.has_wrong_answer.append(newAnswer)
                                newAnswer.is_wrong_answer_of.append(newQuestion)
                            newTask.task_has_answer.append(newAnswer)
                newTask.task_has_question = newQuestion
                newTask.is_task_of.append(groupTaskObj)
                
                term = task["term"]
                if term:
                    termObj = Термин(term)
                    newTask.hasTerm = termObj

        print("Тест изменен!")
        self.onto.save(self.path)

    def deleteTest(self, deleteTest):
        with self.onto:
            class Тест(Thing):
                pass

            class Группа_заданий(Thing):
                pass
        
        query = queries.getTestsNames()
        resultsTests = self.graph.query(query)
        for itemTest in resultsTests:
            testItem = {}
            nameTest = str(itemTest['nameTest'].toPython())
            nameTest = re.sub(r'.*#',"", nameTest)
            testObj = str(itemTest['testObj'].toPython())
            testObj = re.sub(r'.*#',"", testObj)
            if nameTest != deleteTest['testName']:
                continue
            groupTask = str(itemTest['groupTasks'].toPython())
            groupTask = re.sub(r'.*#',"", groupTask)
            groupTaskObj = Группа_заданий(groupTask)
            print("GROUP TASK: ", groupTaskObj)
            testItem["testName"] = nameTest
            
            self.deleteTasks(groupTask)
            destroy_entity(Группа_заданий(groupTaskObj))
            destroy_entity(Тест(testObj))
        print("Тест удален!")
        self.onto.save(self.path)

    def deleteCourse(self, courseObj):
        with self.onto:
            class Курс(Thing):
                pass
        
        course = Курс(courseObj)
        listStudents = self.getStudentsOfCourse(courseObj)
        listModules = self.getModulesOfCourse(courseObj)
        
        for module in listModules:
            moduleObj = module["moduleObj"]
            listTests = self.getTestsOfModule(moduleObj)
            for test in listTests:
                self.deleteTest(test)
            self.deleteModule(moduleObj, courseObj)
        for student in listStudents:
            self.unsubscribeCourse(student["uid"], courseObj)
        destroy_entity(course)

        self.onto.save(self.path)

    def deleteModule(self, moduleObj, courseObj):
        with self.onto:
            class Курс(Thing):
                pass
            class Модуль(Thing):
                pass
        
        module = Модуль(moduleObj)
        course = Курс(courseObj)

        course.has_module.remove(module)
        module.is_module_of.remove(course)
        destroy_entity(module)

        print("Модуль удален!")
        self.onto.save(self.path)

    def deleteTasks(self, groupTask):
        with self.onto:
            class Задание(Thing):
                pass

            class Вопрос(Задание):
                pass

            class Ответ(Задание):
                pass

        query = queries.getTasksQuestions(groupTask)
        resultsTasks = self.graph.query(query)
        for itemTask in resultsTasks:
            taskObj = str(itemTask['task'].toPython())
            taskObj = re.sub(r'.*#',"", taskObj)
            questionObj = str(itemTask['quest'].toPython())
            questionObj = re.sub(r'.*#',"", questionObj)
            print("TASK QUEST: ", taskObj, questionObj)
            query = queries.getAnswersByTask(taskObj, groupTask)
            resultAnswers = self.graph.query(query)
            for itemAnsw in resultAnswers:
                answer = str(itemAnsw['answObj'].toPython())
                answer = re.sub(r'.*#',"", answer)
                if answer != None:
                    #destroy_entity(self.onto.search(is_a = self.onto[answer])[0])
                    destroy_entity(Ответ(answer))
            #destroy_entity(Вопрос(questionObj))
            destroy_entity(Задание(taskObj))
            destroy_entity(self.onto.search(is_a = self.onto[questionObj])[0])
            #destroy_entity(self.onto.search(is_a = self.onto[taskObj])[0])

    def getTests(self):
        query = queries.getTestsNames()
        resultsTests = self.graph.query(query)
        listTests = []
        for itemTest in resultsTests:
            testItem = {}
            nameTest = str(itemTest['nameTest'].toPython())
            nameTest = re.sub(r'.*#',"", nameTest)
            groupTask = str(itemTest['groupTasks'].toPython())
            groupTask = re.sub(r'.*#',"", groupTask)
            testItem["testName"] = nameTest
            query = queries.getTasksQuestions(groupTask)
            resultsTasks = self.graph.query(query)
            listTasks = []
            for itemTask in resultsTasks:
                task = {}
                taskObj = str(itemTask['task'].toPython())
                taskObj = re.sub(r'.*#',"", taskObj)
                questionText = str(itemTask['questText'].toPython())
                questionText = re.sub(r'.*#',"", questionText)
                typeQuestion = str(itemTask['taskType'].toPython())
                typeQuestion = re.sub(r'.*#',"", typeQuestion)

                task = {"question": questionText, "type": getTypeTaskValue(typeQuestion)}

                query = queries.getAnswersByTask(taskObj, groupTask)
                resultAnswers = self.graph.query(query)
                listAnswers = []
                for itemAnsw in resultAnswers:
                    answerObj = str(itemAnsw['answObj'].toPython())
                    answerObj = re.sub(r'.*#',"", answerObj)
                    answerText = str(itemAnsw['answText'].toPython())
                    answerText = re.sub(r'.*#',"", answerText)
                    listAnswers.append({"answer": answerText})
                task["answers"] = listAnswers
                listTasks.append(task)
            testItem["tasks"] = listTasks
            listTests.append(testItem)
        return listTests

    def getTest(self, testName):
        tests = self.getTests()
        for test in tests:
            if test['testName'] == testName:
                return test
        return {}

    def getTestsWithAnswers(self):
        query = queries.getTestsNames()
        resultsTests = self.graph.query(query)
        listTests = []
        for itemTest in resultsTests:
            testItem = {}
            nameTest = str(itemTest['nameTest'].toPython())
            nameTest = re.sub(r'.*#',"", nameTest)
            groupTask = str(itemTest['groupTasks'].toPython())
            groupTask = re.sub(r'.*#',"", groupTask)
            testObj = str(itemTest['testObj'].toPython())
            testObj = re.sub(r'.*#',"", testObj)
            testItem["testName"] = nameTest
            testItem["testObj"] = testObj
            query = queries.getTasksQuestions(groupTask)
            resultsTasks = self.graph.query(query)
            listTasks = []
            for itemTask in resultsTasks:
                task = {}
                taskObj = str(itemTask['task'].toPython())
                taskObj = re.sub(r'.*#',"", taskObj)
                term = str(itemTask['term'].toPython())
                term = re.sub(r'.*#',"", term)
                questionText = str(itemTask['questText'].toPython())
                questionText = re.sub(r'.*#',"", questionText)
                typeQuestion = str(itemTask['taskType'].toPython())
                typeQuestion = re.sub(r'.*#',"", typeQuestion)

                task = {"taskObj": taskObj, "question": questionText, "term": term, "type": getTypeTaskValue(typeQuestion)}

                query = queries.getAnswersByTask(taskObj, groupTask)
                resultAnswers = self.graph.query(query)
                query = queries.getCorrectAnswersByTask(taskObj, groupTask)
                resultCorrectAnswers = self.graph.query(query)
                listAnswers = []
                listCorrects = []
                for correctAnsw in resultCorrectAnswers:
                    correct = str(correctAnsw['answObj'].toPython())
                    correct = re.sub(r'.*#',"", correct)
                    listCorrects.append(correct)
                for itemAnsw in resultAnswers:
                    answerObj = str(itemAnsw['answObj'].toPython())
                    answerObj = re.sub(r'.*#',"", answerObj)
                    answerText = str(itemAnsw['answText'].toPython())
                    answerText = re.sub(r'.*#',"", answerText)
                    listAnswers.append({"answerObj": answerObj, "answer": answerText, "correct": checkCorrectAnswer(answerObj, listCorrects)})
                task["answers"] = listAnswers
                listTasks.append(task)
            testItem["tasks"] = listTasks
            listTests.append(testItem)
        print(listTests)
        return listTests

    def getTestWithAnswers(self, testName):
        tests = self.getTestsWithAnswers()
        for test in tests:
            if test['testName'] == testName:
                return test
        return {}

     # получение даты прохождения теста в виде объекта
    def getNowDate(self):
        now = datetime.now()
        strDate = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second).isoformat()
        objDate = datetime.strptime(strDate,"%Y-%m-%dT%H:%M:%S")
        return objDate

    def getTermsScoresByLastAttempts(self, userObj, uid):
        with self.onto:
            class Термин(Thing):
                pass
            class Пользователь(Thing):
                pass
            class Задание(Thing):
                pass 

        user = Пользователь(userObj)
        query = queries.getLastAttemptsForAverageScoreByUser(userObj)
        resultAttempts = self.graph.query(query)
        attempts = {}
        termsScores = {}
        listLastAttempts = []
        for itemAttempt in resultAttempts:
            testObj = str(itemAttempt['test'].toPython())
            testObj = re.sub(r'.*#',"", testObj)
            testName = str(itemAttempt['testName'].toPython())
            testName = re.sub(r'.*#',"", testName)
            attemptObj = str(itemAttempt['attempt'].toPython())
            attemptObj = re.sub(r'.*#',"", attemptObj)
            if testObj in attempts:
                continue
            else:
                attempts[testObj] = {"testObj": testObj, "testName": testName, "attemptObj": attemptObj}       
                listAllAttempts = self.getAttempts(uid, testName)
                for attempt in listAllAttempts:
                    if attempt["testName"] == testName and attempt["attemptObj"] == attemptObj:
                        listLastAttempts.append(attempt)
                    else:
                        continue
        #print(listLastAttempts)
        for attempt in listLastAttempts:
            tasks = attempt["tasks"]
            for i in range(len(tasks)):
                taskObj = tasks[i]["taskObj"]
                task = Задание(taskObj)
                query = queries.getTermByTask(taskObj)
                resultTerm = self.graph.query(query)
                termObj = ""
                for itemTerm in resultTerm:
                    termObj = str(itemTerm['term'].toPython())
                    termObj = re.sub(r'.*#',"", termObj)
                    if termObj != "":
                        if termObj not in termsScores:
                            termsScores[termObj] = {"sum": 1, "sumScore": 0}
                        else:
                            termsScores[termObj]["sum"] += 1
                for answer in tasks[i]["answers"]:
                    if termObj != "":
                        termsScores[termObj]["sumScore"] += float(answer["score"])
                        break
        print("TermsSCORES: ", termsScores)
        for termObj, term in termsScores.items():
            termItem = Термин(termObj)
            if term["sum"] != 0:
                if term["sumScore"] / term["sum"] > 0.6:
                    user.knownTerm.append(termItem)
                else:
                    user.unknownTerm.append(termItem)
        return termsScores


    def createNewAttempt(self, test, userObj, userAnswers):
        with self.onto:
            class Тест(Thing):
                pass
            class ОтветыСтудента(Thing):
                pass
            class Задание(Thing):
                pass 
            class Пользователь(Thing):
                pass
            class Попытка_прохождения_теста(Thing):
                pass
            class Элемент_теста(Thing):
                pass
            class Термин(Thing):
                pass

        trueAnswers = test['tasks']

        testObj = test["testObj"]
        tasks = test["tasks"]
    
        user = Пользователь(userObj)
        test = Тест(testObj)
        newAttempt = Попытка_прохождения_теста()
        
        user.has_attempt_to_pass_test.append(newAttempt)
        newAttempt.is_attempt_to_pass_test_of.append(user)
        newAttempt.relates_to_test.append(test)
        sum = 0
        termsScores = {}
        for i in range(len(tasks)):
            term = ""
            newTestElement = Элемент_теста()
            newAttempt.has_test_element.append(newTestElement)
            newTestElement.is_test_element_of.append(newAttempt)
            taskObj = tasks[i]["taskObj"]
            task = Задание(taskObj)
            query = queries.getTermByTask(taskObj)
            resultTerm = self.graph.query(query)
            for itemTerm in resultTerm:
                termObj = str(itemTerm['term'].toPython())
                termObj = re.sub(r'.*#',"", termObj)
                if termObj != "":
                    if termObj not in termsScores:
                        termsScores[termObj] = {"sum": 0, "sumScore": 0}
                    else:
                        termsScores[termObj]["sum"] += 1
            newTestElement.has_task.append(task)
            if userAnswers[i]["type"] != typeTask.Text.value:
                result = checkAnswer(trueAnswers[i], userAnswers[i])
                if termObj != "":
                    termsScores[termObj]["sumScore"] += result["sum"]
                sum += result["sum"]
                for j in range(len(result["answerObj"])):
                    #answ = Ответ(result["answerObj"][j])
                    query = queries.getTextAnswerByAnswer(result["answerObj"][j])
                    resultTextAnswer = self.graph.query(query)
                    textAnswer = ""
                    for textAnsw in resultTextAnswer:   
                        textAnswer = str(textAnsw['textAnswer'].toPython())
                        textAnswer = re.sub(r'.*#',"", textAnswer)
                    newAnsw = ОтветыСтудента()
                    answ_correct = result["correct"][j]
                    newAnsw.score = 1 if answ_correct else 0
                    newAnsw.rightAnswer = answ_correct
                    newAnsw.textAnswer = textAnswer
                    newTestElement.has_answer.append(newAnsw)
            else:
                newAnsw = ОтветыСтудента()
                newAnsw.score = 0
                newAnsw.rightAnswer = False
                newAnsw.textAnswer = userAnswers[i]["answer"]
                newTestElement.has_answer.append(newAnsw)
        
        for termObj, term in termsScores.items():
            print("TermObj: ", termObj)
            termItem = Термин(termObj)
            if term["sum"] != 0:
                if term["sumScore"] / term["sum"] > 0.6:
                    user.knownTerm.append(termItem)
                else:
                    user.unknownTerm.append(termItem)
        
        succesfullAttempt = False
        if sum / len(tasks) > 0.3:
            succesfullAttempt = True
        newAttempt.maxScore = len(tasks)
        newAttempt.sumScore = sum
        newAttempt.succesfullAttempt = succesfullAttempt
        newAttempt.checked = False
        newAttempt.dateAndTime = self.getNowDate()
        newAttempt.percentCompleteOfTest = sum / len(tasks)

        self.onto.save(self.path)
        return sum
    
    def getResultAttempt(self, answers, user):
        nameTest = answers['testName']
        test = self.getTestWithAnswers(nameTest)
        userObj = user["userObj"]
        userAnswers = answers['answers']
        sum = self.createNewAttempt(test, userObj, userAnswers)
        result = {"trueCount": sum, "countTasks": len(test['tasks'])}

        return result

    def createUser(self, user):
        with self.onto:
            class Пользователь(Thing):
                pass

        newUser = Пользователь()
        print("User: ", user)
        newUser.firstName = user['firstName']
        newUser.lastName = user['lastName']
        newUser.email = user['email']
        newUser.uid = user['uid']
        newUser.role = 'student'

        self.onto.save(self.path)

    def createSubjectArea(self, nameSubjArea):
        with self.onto:
            class Предметная_область(Thing):
                pass
            class Область(Предметная_область):
                pass

        newSubhArea = Область(nameSubjArea)
    
        self.onto.save(self.path)

    def getUser(self, user_uid):
        query = queries.getUsers()
        resultUsers = self.graph.query(query)
        userItem = {}
        for itemUser in resultUsers:
            uid = str(itemUser['uid'].toPython())
            uid = re.sub(r'.*#',"", uid)
            if uid != user_uid:
                continue
            userObj = str(itemUser['userObj'].toPython())
            userObj = re.sub(r'.*#',"", userObj)
            firstName = str(itemUser['firstName'].toPython())
            firstName = re.sub(r'.*#',"", firstName)
            lastName = str(itemUser['lastName'].toPython())
            lastName = re.sub(r'.*#',"", lastName)
            role = str(itemUser['role'].toPython())
            role = re.sub(r'.*#',"", role)
            email = str(itemUser['email'].toPython())
            email = re.sub(r'.*#',"", email)
            userItem = {"userObj": userObj, "firstName": firstName, "lastName": lastName, "email": email, "role": role, "uid": uid, "fullName": firstName + " " + lastName}
        
        return userItem

    def getUsers(self):
        query = queries.getUsers()
        resultUsers = self.graph.query(query)
        listUsers = []
        for itemUser in resultUsers:
            uid = str(itemUser['uid'].toPython())
            uid = re.sub(r'.*#',"", uid)
            userObj = str(itemUser['userObj'].toPython())
            userObj = re.sub(r'.*#',"", userObj)
            firstName = str(itemUser['firstName'].toPython())
            firstName = re.sub(r'.*#',"", firstName)
            lastName = str(itemUser['lastName'].toPython())
            lastName = re.sub(r'.*#',"", lastName)
            role = str(itemUser['role'].toPython())
            role = re.sub(r'.*#',"", role)
            email = str(itemUser['email'].toPython())
            email = re.sub(r'.*#',"", email)
            userItem = {"userObj": userObj, "firstName": firstName, "lastName": lastName, "email": email, "role": role, "uid": uid, "fullName": firstName + " " + lastName}
            listUsers.append(userItem)        
        
        return listUsers
    
    def getUsersWhoPassedTheTest(self, testName):
        print("testName: ", testName)
        users = self.getUsers()
        
        listUsers = []
        for user in users:
            listAttempts = self.getAttempts(user["uid"], testName)
            if listAttempts:
                user["attempts"] = listAttempts
                listUsers.append(user)

        print(listUsers)
        return listUsers


    def getAttempts(self, user_uid, nameTest):
        print("UID NAMETEST: ", user_uid, nameTest)
        user = self.getUser(user_uid)
        test = self.getTestWithAnswers(nameTest)
        userObj = user["userObj"]
        testObj = test["testObj"]
        tasks = test["tasks"]
        query = queries.getAttempts(userObj, testObj)
        resultAttempts = self.graph.query(query)
        listAttempts = []
        for itemAttempt in resultAttempts:
            testCopy = copy.deepcopy(test)
            tasksCopy = testCopy["tasks"]
            attemptObj = str(itemAttempt['attemptObj'].toPython())
            attemptObj = re.sub(r'.*#',"", attemptObj)
            percentComplete = str(itemAttempt['percentComplete'].toPython())
            percentComplete = re.sub(r'.*#',"", percentComplete)
            succesfull = str(itemAttempt['succesfull'].toPython())
            succesfull = re.sub(r'.*#',"", succesfull)
            checked = str(itemAttempt['checked'].toPython())
            checked = re.sub(r'.*#',"", checked)
            testCopy["percentComplete"] = percentComplete
            testCopy["succesfull"] = succesfull
            testCopy["checked"] = checked
            testCopy["attemptObj"] = attemptObj
            query = queries.getTestElements(attemptObj)
            resultTestElements = self.graph.query(query)
            i = 0
            for itemTestElement in resultTestElements:
                answersCopy = tasksCopy[i]["answers"]
                taskType = tasksCopy[i]["type"]
                testElementObj = str(itemTestElement['testElem'].toPython())
                testElementObj = re.sub(r'.*#',"", testElementObj)
                query = queries.getAnswersAndCorrectByTestElem(testElementObj)
                resultAnswersByTestElem = self.graph.query(query)
                for itemAnswByTestElem in resultAnswersByTestElem:
                    answObj = str(itemAnswByTestElem['answerObj'].toPython())
                    answObj = re.sub(r'.*#',"", answObj)
                    answText = str(itemAnswByTestElem['textAnswer'].toPython())
                    answText = re.sub(r'.*#',"", answText)
                    correctAnsw = str(itemAnswByTestElem['correct'].toPython())
                    correctAnsw = re.sub(r'.*#',"", correctAnsw)
                    answScore = str(itemAnswByTestElem['score'].toPython())
                    answScore = re.sub(r'.*#',"", answScore)
                    correctAnsw = True if correctAnsw == "True" else False
                    if taskType == "1":
                        answersCopy = [{"answerObj": answObj, "answer": answText, "correct": False, "correctByUser": correctAnsw, "score": answScore}]
                        #print("ASNWERSCOPY: ", answersCopy)
                    for j in range(len(answersCopy)):
                        if answersCopy[j]['answer'] == answText:
                            answersCopy[j]["correctByUser"] = correctAnsw
                        if "correctByUser" not in answersCopy[j]:
                            answersCopy[j]["correctByUser"] = None
                        answersCopy[j]["score"] = answScore
                    testCopy["tasks"][i]["answers"] = answersCopy
                i += 1
            listAttempts.append(testCopy)
        return listAttempts

    def getUserCourses(self, user_uid):
        user = self.getUser(user_uid)
        userObj = user["userObj"]
        query = queries.getUserCourses(userObj)
        resultCourses = self.graph.query(query)
        listCourses = []
        for itemCourse in resultCourses:
            courseObj = str(itemCourse['courseObj'].toPython())
            courseObj = re.sub(r'.*#',"", courseObj)
            courseName = str(itemCourse['courseName'].toPython())
            courseName = re.sub(r'.*#',"", courseName)
            courseDescription = str(itemCourse['courseDescription'].toPython())
            courseDescription = re.sub(r'.*#',"", courseDescription)
            courseInfo = str(itemCourse['courseInfo'].toPython())
            courseInfo = re.sub(r'.*#',"", courseInfo)
            item = {"courseObj": courseObj, "courseName": courseName, "courseDescription": courseDescription, "courseInfo": courseInfo}
            listCourses.append(item)
        
        print(listCourses)
        return listCourses

    def getAllCourses(self):
        query = queries.getCoursesNames()
        resultCourses = self.graph.query(query)
        listCourses = []
        for itemCourse in resultCourses:
            courseObj = str(itemCourse['courseObj'].toPython())
            courseObj = re.sub(r'.*#',"", courseObj)
            courseName = str(itemCourse['courseName'].toPython())
            courseName = re.sub(r'.*#',"", courseName)
            courseDescription = str(itemCourse['courseDescription'].toPython())
            courseDescription = re.sub(r'.*#',"", courseDescription)
            courseInfo = str(itemCourse['courseInfo'].toPython())
            courseInfo = re.sub(r'.*#',"", courseInfo)
            item = {"courseObj": courseObj, "courseName": courseName, "courseDescription": courseDescription, "courseInfo": courseInfo}
            listCourses.append(item)
        
        print(listCourses)
        return listCourses

    def subscribeCourse(self, _uid, _courseObj):
        with self.onto:
            class Пользователь(Thing):
                pass
            class Курс(Thing):
                pass
        user = self.getUser(_uid)
        userObj = user["userObj"]

        userItem = Пользователь(userObj)
        courseItem = Курс(_courseObj)

        userItem.enrolled_course.append(courseItem)
        self.onto.save(self.path)

    def unsubscribeCourse(self, _uid, _courseObj):
        with self.onto:
            class Пользователь(Thing):
                pass
            class Курс(Thing):
                pass
        user = self.getUser(_uid)
        userObj = user["userObj"]

        userItem = Пользователь(userObj)
        courseItem = Курс(_courseObj)

        userItem.enrolled_course.remove(courseItem)
        self.onto.save(self.path)    

    def getNameDescrInfoCourse(self, courseObj):
        query = queries.getNameDescrInfoCourse(courseObj)
        resultCourses = self.graph.query(query)
        courseItem = {}
        for itemCourse in resultCourses:
            courseName = str(itemCourse['courseName'].toPython())
            courseName = re.sub(r'.*#',"", courseName)
            courseDescription = str(itemCourse['courseDescription'].toPython())
            courseDescription = re.sub(r'.*#',"", courseDescription)
            courseInfo = str(itemCourse['courseInfo'].toPython())
            courseInfo = re.sub(r'.*#',"", courseInfo)
            courseItem = {"courseObj": courseObj, "courseName": courseName, "courseDescription": courseDescription, "courseInfo": courseInfo}
        return courseItem

    def getStudentsOfCourse(self, courseObj):
        query = queries.getStudentsCourse(courseObj)
        resultUsers = self.graph.query(query)
        listUsers = []
        for itemUser in resultUsers:
            uid = str(itemUser['uid'].toPython())
            uid = re.sub(r'.*#',"", uid)
            user = self.getUser(uid)
            listUsers.append(user)
            
        return listUsers

    def getTestsOfModule(self, moduleObj):
        query = queries.getTestsOfModule(moduleObj)
        resultTests = self.graph.query(query)
        listTests = []
        for itemTest in resultTests:
            testObj = str(itemTest['testObj'].toPython())
            testObj = re.sub(r'.*#',"", testObj)
            testName = str(itemTest['testName'].toPython())
            testName = re.sub(r'.*#',"", testName)
            groupTasks = str(itemTest['groupTasks'].toPython())
            groupTasks = re.sub(r'.*#',"", groupTasks)
            item = {"testObj": testObj, "testName": testName, "groupTasks": groupTasks}
            listTests.append(item)
        
        print("Tests: ", listTests)
        return listTests

    def getLecturesOfModule(self, moduleObj):
        query = queries.getLecturesOfModule(moduleObj)
        resultLectures = self.graph.query(query)
        listLectures = []
        for itemLecture in resultLectures:
            lectureObj = str(itemLecture['lectureObj'].toPython())
            lectureObj = re.sub(r'.*#',"", lectureObj)
            lectureName = str(itemLecture['lectureName'].toPython())
            lectureName = re.sub(r'.*#',"", lectureName)
            item = {"lectureObj": lectureObj, "lectureName": lectureName}
            listLectures.append(item)
        
        print("Lectures: ", listLectures)
        return listLectures

    def getModulesOfCourse(self, courseObj):
        query = queries.getModulesOfCourse(courseObj)
        resultModules = self.graph.query(query)
        listModules = []
        for itemModule in resultModules:
            moduleObj = str(itemModule['moduleObj'].toPython())
            moduleObj = re.sub(r'.*#',"", moduleObj)
            nameModule = str(itemModule['nameModule'].toPython())
            nameModule = re.sub(r'.*#',"", nameModule)
            subArea = str(itemModule['subArea'].toPython())
            subArea = re.sub(r'.*#',"", subArea)
            listTests = self.getTestsOfModule(moduleObj)
            listLectures = self.getLecturesOfModule(moduleObj)
            item = {"moduleObj": moduleObj, "nameModule": nameModule, "subjectArea": subArea, "tests": listTests, "lectures": listLectures}
            listModules.append(item)
        
        print(listModules)
        return listModules

    def getCourseInfo(self, courseObj):
        courseItem = self.getNameDescrInfoCourse(courseObj)
        listStudents = self.getStudentsOfCourse(courseObj)
        listModules = self.getModulesOfCourse(courseObj)

        courseItem["students"] = listStudents
        courseItem["modules"] = listModules

        print("COURSE ITEM: ", courseItem)
        return courseItem

    def editProfile(self, userItem):
        with self.onto:
            class Пользователь(Thing):
                pass
        
        userPrev = self.getUser(userItem["uid"])
        userObj = userPrev["userObj"]
        user = Пользователь(userObj)

        user.firstName = userItem["firstName"]
        user.lastName = userItem["lastName"]
        
        print("Профиль изменен!")
        self.onto.save(self.path)

    def editRole(self, userItem):
        with self.onto:
            class Пользователь(Thing):
                pass
        
        user = self.getUser(userItem["uid"])
        userObj = user["userObj"]
        user = Пользователь(userObj)

        user.role = userItem["role"]
        
        print("Роль изменена!")
        self.onto.save(self.path)

    def editModule(self, moduleItem):
        with self.onto:
            class Модуль(Thing):
                pass
            class Область(Thing):
                pass
        
        moduleObj = moduleItem["moduleObj"]
        moduleName = moduleItem["nameModule"]
        subjArea = moduleItem["subjectArea"]

        subjectArea = Область(subjArea)
        module = Модуль(moduleObj)

        module.has_subject_area = subjectArea
        module.nameModule = moduleName
        
        print("Профиль изменен!")
        self.onto.save(self.path)

    def editAttempt(self, attemptItem):
        with self.onto:
            class Попытка_прохождения_теста(Thing):
                pass
            class ОтветыСтудента(Thing):
                pass
            class Пользователь(Thing):
                pass
            class Термин(Thing):
                pass
        
        attemptObj = attemptItem["attemptObj"]
        userObj = attemptItem["userObj"]
        user = Пользователь(userObj)
        attempt = Попытка_прохождения_теста(attemptObj)

        attempt.checked = True
        
        termsScores = {}
        for taskItem in attemptItem["tasks"]:
            taskObj = taskItem["taskObj"]
            query = queries.getTermByTask(taskObj)
            resultTerm = self.graph.query(query)
            termObj = ""
            for itemTerm in resultTerm:
                termObj = str(itemTerm['term'].toPython())
                termObj = re.sub(r'.*#',"", termObj)
                if termObj != "":
                    if termObj not in termsScores:
                        termsScores[termObj] = {"sum": 1, "sumScore": 0}
                    else:
                        termsScores[termObj]["sum"] += 1
            if taskItem["type"] == typeTask.Text.value:
                for answer in taskItem["answers"]:
                    answerObj = ОтветыСтудента(answer["answerObj"])
                    prevAnswerScore = answerObj.score
                    print("prevAnswerScore: ", prevAnswerScore)
                    answerObj.score = answer["score"]
                    if prevAnswerScore != answer["score"]:
                        attempt.sumScore -= float(prevAnswerScore)
                        attempt.sumScore += float(answer["score"])
                        attempt.percentCompleteOfTest = attempt.sumScore / attempt.maxScore
                    if termObj != "":
                        termsScores[termObj]["sumScore"] += float(answer["score"])
            elif taskItem["type"] != typeTask.Multiple.value:
                for answer in taskItem["answers"]:
                    if answer["correctByUser"] == True:
                        if termObj != "":
                            termsScores[termObj]["sumScore"] += float(answer["score"])
                        break
            elif taskItem["type"] == typeTask.Multiple.value:
                sum = 0
                maxSum = 0
                for answer in taskItem["answers"]:
                    if answer["correctByUser"] == True:
                        maxSum += 1
                        sum += 1
                    elif answer["correctByUser"] == False:
                        maxSum += 1
                if termObj != "" and maxSum != 0:
                    termsScores[termObj]["sumScore"] += (sum / maxSum)

        print("TERMSCORES: ", termsScores)
        for termObj, term in termsScores.items():
            print("TermObj: ", termObj)
            termItem = Термин(termObj)
            if term["sum"] != 0:
                if term["sumScore"] / term["sum"] > 0.6:
                    try:
                        user.unknownTerm.remove(termItem)
                    except Exception:
                        print('Нельзя удалить несуществующее')
                    user.knownTerm.append(termItem)
                else:
                    try:
                        user.knownTerm.remove(termItem)
                    except Exception:
                        print('Нельзя удалить несуществующее')
                    user.unknownTerm.append(termItem)
        
        print("Попытка изменена!")
        self.onto.save(self.path)

    def getTermsOfField(self, fieldObj):
        query = queries.getTermsOfField(fieldObj)
        resultTerms = self.graph.query(query)
        listTerms = []
        for itemTerm in resultTerms:
            term = str(itemTerm['term'].toPython())
            term = re.sub(r'.*#',"", term)
            prevTerm = str(itemTerm['prevTerm'].toPython())
            prevTerm = re.sub(r'.*#',"", prevTerm)
            moveToPrev = str(itemTerm['moveToPrev'].toPython())
            moveToPrev = re.sub(r'.*#',"", moveToPrev)
            item = {"term": term, "prevTerm": prevTerm, "moveToPrev": moveToPrev}
            listTerms.append(item)
        
        #print(listTerms)
        return listTerms

    def getTermsNormilizeOfField(self, fieldObj):
        query = queries.getTermsOfField(fieldObj)
        resultTerms = self.graph.query(query)
        listTerms = []
        listTermsNormalize = []
        for itemTerm in resultTerms:
            term = str(itemTerm['term'].toPython())
            term = re.sub(r'.*#',"", term)
            termNormalize = str(itemTerm['termNormalize'].toPython())
            termNormalize = re.sub(r'.*#',"", termNormalize)
            #item = {"term": term, "termNormalize": termNormalize}
            listTerms.append(term)
            listTermsNormalize.append(termNormalize)
        
        #print(listTerms)
        return listTerms, listTermsNormalize

    def getTermByTask(self, task):
        tokens = getTokensFromTexts([task["question"]])
        terms = self.getTermsOfField("палинология")
        print(tokens)
        term = getTermFromText(tokens[0], terms)
        print(term)
        return term

    def getKnownTermsByUser(self, userObj, termsScores):
        query = queries.getKnownTermsByUser(userObj)
        resultTerms = self.graph.query(query)
        listTerms = []
        sumCorr = {}
        sumCou = {}
        sumCorrect = 0
        sumCount = 0
        for itemTerm in resultTerms:
            termObj = str(itemTerm['term'].toPython())
            termObj = re.sub(r'.*#',"", termObj)
            subjectArea = str(itemTerm['subjectArea'].toPython())
            subjectArea = re.sub(r'.*#',"", subjectArea)
            term = termObj.replace("_", " ")
            termStr = term[0].upper() + term[1:]
            if termObj in termsScores:
                item = {"termObj": termObj, "term": termStr, "sumCount": termsScores[termObj]["sum"], "sumCorrect": termsScores[termObj]["sumScore"], "subjectArea": subjectArea}
                listTerms.append(item)
                if subjectArea not in sumCorr:
                    sumCorr[subjectArea] = {"sumCorrect": termsScores[termObj]["sumScore"], "sumCount": termsScores[termObj]["sum"]}
                else:
                    sumCorr[subjectArea]["sumCorrect"] += termsScores[termObj]["sumScore"]
                    sumCorr[subjectArea]["sumCount"] += termsScores[termObj]["sum"]
                sumCorrect += termsScores[termObj]["sumScore"]
                sumCount += termsScores[termObj]["sum"]
        
        return listTerms, sumCorrect, sumCount, sumCorr

    def getUnknownTermsByUser(self, userObj, termsScores):
        query = queries.getUnknownTermsByUser(userObj)
        resultTerms = self.graph.query(query)
        listTerms = []
        listTermObj = []
        sumCorr = {}
        sumCorrect = 0
        sumCount = 0
        for itemTerm in resultTerms:
            termObj = str(itemTerm['term'].toPython())
            termObj = re.sub(r'.*#',"", termObj)
            subjectArea = str(itemTerm['subjectArea'].toPython())
            subjectArea = re.sub(r'.*#',"", subjectArea)
            term = termObj.replace("_", " ")
            termStr = term[0].upper() + term[1:]
            if termObj in termsScores:
                item = {"termObj": termObj, "term": termStr, "sumCount": termsScores[termObj]["sum"], "sumCorrect": termsScores[termObj]["sumScore"], "subjectArea": subjectArea}
                listTerms.append(item)
                listTermObj.append(termObj)
                if subjectArea not in sumCorr:
                    sumCorr[subjectArea] = {"sumCorrect": termsScores[termObj]["sumScore"], "sumCount": termsScores[termObj]["sum"]}
                else:
                    sumCorr[subjectArea]["sumCorrect"] += termsScores[termObj]["sumScore"]
                    sumCorr[subjectArea]["sumCount"] += termsScores[termObj]["sum"]
                sumCorrect += termsScores[termObj]["sumScore"]
                sumCount += termsScores[termObj]["sum"]
        lectures = self.getLecturesByTerms(listTermObj)

        return listTerms, sumCorrect, sumCount, sumCorr, lectures

    def getTermsByUser(self, userObj, uid):
        termsScores = self.getTermsScoresByLastAttempts(userObj, uid)
        knownTerms, sumKnown, sumCountKnown, sumCorrKnown = self.getKnownTermsByUser(userObj, termsScores)
        unknownTerms, sumUnknown, sumCountUnknown, sumCorrUnknown, lectures = self.getUnknownTermsByUser(userObj, termsScores)
        sumScores = {}
        for field in sumCorrKnown:
            if field not in sumScores:
                sumScores[field] = {"sumCorrect": sumCorrKnown[field]["sumCorrect"], "sumCount": sumCorrKnown[field]["sumCount"]}
            else:
                sumScores[field]["sumCorrect"] += sumCorrKnown[field]["sumCorrect"]
                sumScores[field]["sumCount"] += sumCorrKnown[field]["sumCount"]
        for field in sumCorrUnknown:
            if field not in sumScores:
                sumScores[field] = {"sumCorrect": sumCorrUnknown[field]["sumCorrect"], "sumCount": sumCorrUnknown[field]["sumCount"]}
            else:
                sumScores[field]["sumCorrect"] += sumCorrUnknown[field]["sumCorrect"]
                sumScores[field]["sumCount"] += sumCorrUnknown[field]["sumCount"]
        
        item = {"knownTerms": knownTerms, "unknownTerms": unknownTerms, "sumScores": sumKnown + sumUnknown, "sumCount": sumCountKnown + sumCountUnknown, "sumScoresLite": sumScores, "lectures": lectures}
        return item

    def getSubjectAreas(self):
        query = queries.getSubjectAreas()
        resultAreas = self.graph.query(query)
        listAreas = []
        for itemArea in resultAreas:
            subjAreaObj = str(itemArea['subArea'].toPython())
            subjAreaObj = re.sub(r'.*#',"", subjAreaObj)

            subjAreaStr = subjAreaObj.replace("_", " ")
            subjAreaStr = subjAreaStr[0].upper() + subjAreaStr[1:]
            terms = self.getTermsBySubjArea(subjAreaObj)
            item = {"subjectAreaObj": subjAreaObj, "subjectArea": subjAreaStr, "terms": terms}
            listAreas.append(item)
        
        #print(listTerms)
        return listAreas

    def createTerm(self, nameTerm, subjectArea):
        with self.onto:
            class Предметная_область(Thing):
                pass
            class Область(Предметная_область):
                pass
            class Термин(Предметная_область):
                pass
            
        field = Область(subjectArea)
        nameTerm = nameTerm.replace(" ", "_")
        newTerm = Термин(nameTerm)

        termNormalize = getTokensFromTexts([nameTerm])
        prevTerm = Термин(subjectArea.replace(" ", "_"))

        newTerm.termNormalize = termNormalize[0][0]
        newTerm.isTermOf = field
        newTerm.hasPrevTerm = prevTerm
        newTerm.moveToPrev = False

        self.onto.save(self.path)

    def deleteTerm(self, nameTerm):
        with self.onto:
            class Предметная_область(Thing):
                pass
            class Термин(Предметная_область):
                pass
            
        nameTerm = nameTerm.replace(" ", "_")
        term = Термин(nameTerm)
        destroy_entity(term)

        self.onto.save(self.path)

    def deleteLecture(self, lectureObj, moduleObj):
        with self.onto:
            class Лекция(Thing):
                pass
            
        lecture = Лекция(lectureObj)
        destroy_entity(lecture)

        self.onto.save(self.path)

    def createTerms(self):
        with self.onto:
            class Предметная_область(Thing):
                pass
            class Область(Предметная_область):
                pass
            class Термин(Предметная_область):
                pass

        listTerms = [
            {
                "область": "палинология", 
                "term": "палинология",
                "termNormalize": getTokensFromTexts(["палинология"])[0],
                "prevTerm": "", 
                "moveToPrev": False,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": [],
            },
            {
                "область": "палинология", 
                "term": "морфологические_характеристики", 
                "termNormalize": getTokensFromTexts(["морфологические_характеристики"])[0],
                "prevTerm": "", 
                "moveToPrev": False,
                "divided_in_groups": ["высшие", "низшие"],
                "contains": [],
                "relates_to_the_group": [],    
            },
            {
                "область": "палинология", 
                "term": "характеристики", 
                "termNormalize": getTokensFromTexts(["характеристики"])[0],
                "prevTerm": "", 
                "moveToPrev": False,
                "divided_in_groups": ["высшие", "низшие"],
                "contains": [],
                "relates_to_the_group": [],    
            },
            {
                "область": "палинология", 
                "term": "апертура", 
                "termNormalize": getTokensFromTexts(["апертура"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["простая", "сложная"],
                "contains": [],
                "relates_to_the_group": ["морфологические характеристики"],    
            },
            {
                "область": "палинология", 
                "term": "простая_апертура",
                "termNormalize": getTokensFromTexts(["простая_апертура"])[0], 
                "prevTerm": "апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": ["борозды", "лептомы", "поры", "руги", "щели"],
                "relates_to_the_group": ["апертура"],
            },
            {
                "область": "палинология", 
                "term": "простая",
                "termNormalize": getTokensFromTexts(["простая"])[0], 
                "prevTerm": "апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": ["борозды", "лептомы", "поры", "руги", "щели"],
                "relates_to_the_group": ["апертура"],
            },
            {
                "область": "палинология", 
                "term": "сложная_апертура", 
                "termNormalize": getTokensFromTexts(["сложная_апертура"])[0],
                "prevTerm": "апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": ["бороздо-оровые", "бороздо-поровые", "порово-оровые"],
                "relates_to_the_group": ["апертура"],
            },
            {
                "область": "палинология", 
                "term": "сложная", 
                "termNormalize": getTokensFromTexts(["сложная"])[0],
                "prevTerm": "апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": ["бороздо-оровые", "бороздо-поровые", "порово-оровые"],
                "relates_to_the_group": ["апертура"],
            },
            {
                "область": "палинология", 
                "term": "борозды", 
                "termNormalize": getTokensFromTexts(["борозды"])[0],
                "prevTerm": "простая апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["простая апертура", "апертура"],    
            },
            {
                "область": "палинология", 
                "term": "лептомы", 
                "termNormalize": getTokensFromTexts(["лептомы"])[0],
                "prevTerm": "простая апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["простая апертура", "апертура"],  
            },
            {
                "область": "палинология", 
                "term": "поры", 
                "termNormalize": getTokensFromTexts(["поры"])[0],
                "prevTerm": "простая апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["простая апертура", "апертура"],     
            },
            {
                "область": "палинология", 
                "term": "руги", 
                "termNormalize": getTokensFromTexts(["руги"])[0],
                "prevTerm": "простая апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["простая апертура", "апертура"],     
            },
            {
                "область": "палинология", 
                "term": "щели", 
                "termNormalize": getTokensFromTexts(["щели"])[0],
                "prevTerm": "простая апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["простая апертура", "апертура"],     
            },
            {
                "область": "палинология", 
                "term": "бороздо-оровые", 
                "termNormalize": getTokensFromTexts(["бороздо-оровые"])[0],
                "prevTerm": "сложная апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["сложная апертура", "апертура"],     
            },
            {
                "область": "палинология", 
                "term": "бороздо-поровые", 
                "termNormalize": getTokensFromTexts(["бороздо-поровые"])[0],
                "prevTerm": "сложная апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["сложная апертура", "апертура"],    
            },
            {
                "область": "палинология", 
                "term": "порово-оровые", 
                "termNormalize": getTokensFromTexts(["порово-оровые"])[0],
                "prevTerm": "сложная апертура", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["сложная апертура", "апертура"],    
            },
            {
                "область": "палинология", 
                "term": "оболочка_пыльцевого_зерна", 
                "termNormalize": getTokensFromTexts(["оболочка_пыльцевого_зерна"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["интина", "экзина"],
                "contains": [],
                "relates_to_the_group": ["оболочка пыльцевого зерна"],    
            },
            {
                "область": "палинология", 
                "term": "оболочка", 
                "termNormalize": getTokensFromTexts(["оболочка"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["интина", "экзина"],
                "contains": [],
                "relates_to_the_group": ["оболочка пыльцевого зерна"],    
            },
            {
                "область": "палинология", 
                "term": "интина", 
                "termNormalize": getTokensFromTexts(["интина"])[0],
                "prevTerm": "оболочка_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": ["экзинтина", "эуинтина"],
                "contains": ["экзинтина", "эуинтина"],
                "relates_to_the_group": ["интина"], 
            },
            #{"область": "палинология", "term": "экзина", "prevTerm": "оболочка_пыльцевого_зерна", "moveToPrev": True},
            {
                "область": "палинология", 
                "term": "экзинтина", 
                "termNormalize": getTokensFromTexts(["экзинтина"])[0],
                "prevTerm": "интина", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["интина"], 
            },
            {
                "область": "палинология", 
                "term": "эуинтина", 
                "termNormalize": getTokensFromTexts(["эуинтина"])[0],
                "prevTerm": "интина", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["интина"],    
            },
            #{"область": "палинология", "term": "мэкзина", "prevTerm": "экзина", "moveToPrev": True},
            #{"область": "палинология", "term": "эктэкзина", "prevTerm": "экзина", "moveToPrev": True},
            #{"область": "палинология", "term": "эндэкзина", "prevTerm": "экзина", "moveToPrev": True},
            {
                "область": "палинология", 
                "term": "скульптура_пыльцевого_зерна", 
                "termNormalize": getTokensFromTexts(["скульптура_пыльцевого_зерна"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": [],
                "contains": ["бугорчатая", "гладкая", "зернистая", "морщинистая", "сетчатая", "столбчатая", "струйчатая", "шероховатая", "шиповватая", "ямчатая" ],
                "relates_to_the_group": ["морфологические признаки"],    
            },
            {
                "область": "палинология", 
                "term": "скульптура", 
                "termNormalize": getTokensFromTexts(["скульптура"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": [],
                "contains": ["бугорчатая", "гладкая", "зернистая", "морщинистая", "сетчатая", "столбчатая", "струйчатая", "шероховатая", "шиповватая", "ямчатая" ],
                "relates_to_the_group": ["морфологические признаки"],    
            },
            {
                "область": "палинология", 
                "term": "поверхность_пыльцевого_зерна", 
                "termNormalize": getTokensFromTexts(["поверхность_пыльцевого_зерна"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": [],
                "contains": ["бугорчатая", "гладкая", "зернистая", "морщинистая", "сетчатая", "столбчатая", "струйчатая", "шероховатая", "шиповватая", "ямчатая" ],
                "relates_to_the_group": ["морфологические признаки"],  
            },
            {
                "область": "палинология", 
                "term": "поверхность", 
                "termNormalize": getTokensFromTexts(["поверхность"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": [],
                "contains": ["бугорчатая", "гладкая", "зернистая", "морщинистая", "сетчатая", "столбчатая", "струйчатая", "шероховатая", "шиповватая", "ямчатая" ],
                "relates_to_the_group": ["морфологические признаки"],  
            },
            {
                "область": "палинология", 
                "term": "бугорчатая", 
                "termNormalize": getTokensFromTexts(["бугорчатая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "гладкая", 
                "termNormalize": getTokensFromTexts(["гладкая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            }
            ,
            {
          
                "область": "палинология", 
                "term": "зернистая", 
                "termNormalize": getTokensFromTexts(["зернистая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "морщинистая", 
                "termNormalize": getTokensFromTexts(["морщинистая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "сетчатая", 
                "termNormalize": getTokensFromTexts(["сетчатая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "столбчатая", 
                "termNormalize": getTokensFromTexts(["столбчатая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "струйчатая", 
                "termNormalize": getTokensFromTexts(["струйчатая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "шероховатая", 
                "termNormalize": getTokensFromTexts(["шероховатая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "шиповатая", 
                "termNormalize": getTokensFromTexts(["шиповатая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "ямчатая", 
                "termNormalize": getTokensFromTexts(["ямчатая"])[0],
                "prevTerm": "cкульптура_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["поверхность_пыльцевого_зерна", "скульптура_пыльцевого_зерна"], 
            },
            {
                "область": "палинология", 
                "term": "полярность_пыльцевого_зерна", 
                "termNormalize": getTokensFromTexts(["полярность_пыльцевого_зерна"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["неполярное", "равнополярное", "разнополярное"],
                "contains": ["неполярное", "равнополярное", "разнополярное"],
                "relates_to_the_group": ["морфологические характеристики"], 
            },
            {
                "область": "палинология", 
                "term": "полярность", 
                "termNormalize": getTokensFromTexts(["полярность"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["неполярное", "равнополярное", "разнополярное"],
                "contains": ["неполярное", "равнополярное", "разнополярное"],
                "relates_to_the_group": ["морфологические характеристики"], 
            },
            {
                "область": "палинология", 
                "term": "неполярное",
                "termNormalize": getTokensFromTexts(["неполярное"])[0],
                "prevTerm": "полярность_пыльцевого_зерна",
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["полярность_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "равнополярное", 
                "termNormalize": getTokensFromTexts(["равнополярное"])[0],
                "prevTerm": "полярность_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["полярность_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "разнополярное", 
                "termNormalize": getTokensFromTexts(["разнополярное"])[0],
                "prevTerm": "полярность_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["полярность_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "проекция_пыльцевого_зерна", 
                "termNormalize": getTokensFromTexts(["проекция_пыльцевого_зерна"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["полярная проекция", "экваториальная проекция"],
                "contains": [],
                "relates_to_the_group": ["морфологические_характеристики"],
            },
            {
                "область": "палинология", 
                "term": "проекция", 
                "termNormalize": getTokensFromTexts(["проекция"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["полярная проекция", "экваториальная проекция"],
                "contains": [],
                "relates_to_the_group": ["морфологические_характеристики"],
            },
            {
                "область": "палинология", 
                "term": "полярная", 
                "termNormalize": getTokensFromTexts(["полярная"])[0],
                "prevTerm": "проекция_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["проекция_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "экваториальная", 
                "termNormalize": getTokensFromTexts(["экваториальная"])[0],
                "prevTerm": "проекция_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["проекция_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "размер_пыльцевого_зерна", 
                "termNormalize": getTokensFromTexts(["размер_пыльцевого_зерна"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["мелкие", "очень мелкие", "средние", "крупные", "очень крупные", "гигантские"],
                "contains": [],
                "relates_to_the_group": ["морфологические_характеристики"],
            },
            {
                "область": "палинология", 
                "term": "размер", 
                "termNormalize": getTokensFromTexts(["размер"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["мелкие", "очень мелкие", "средние", "крупные", "очень крупные", "гигантские"],
                "contains": [],
                "relates_to_the_group": ["морфологические_характеристики"],
            },
            {
                "область": "палинология", 
                "term": "мелкие", 
                "termNormalize": getTokensFromTexts(["мелкие"])[0],
                "prevTerm": "размер_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["размер_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "очень_мелкие", 
                "termNormalize": getTokensFromTexts(["очень_мелкие"])[0],
                "prevTerm": "размер_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["размер_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "средние", 
                "termNormalize": getTokensFromTexts(["средние"])[0],
                "prevTerm": "размер_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["размер_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "крупные", 
                "termNormalize": getTokensFromTexts(["крупные"])[0],
                "prevTerm": "размер_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["размер_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "очень_крупные", 
                "termNormalize": getTokensFromTexts(["очень_крупные"])[0],
                "prevTerm": "размер_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["размер_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "гигантские", 
                "termNormalize": getTokensFromTexts(["гигантские"])[0],
                "prevTerm": "размер_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["размер_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "форма_пыльцевого_зерна", 
                "termNormalize": getTokensFromTexts(["форма_пыльцевого_зерна"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["выпукло-вогнутая", "лопастая", "округлая", "округло-угловатая", "плосковыпуклая", "прямоугольная", "ромбическая", "сжато-прямоугольная", "сжато-эллиптическая", "сфероидальная", "угловатая", "эллиптическая"],
                "contains": [],
                "relates_to_the_group": ["морфологические_характеристики"],
            },
            {
                "область": "палинология", 
                "term": "форма", 
                "termNormalize": getTokensFromTexts(["форма"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["выпукло-вогнутая", "лопастая", "округлая", "округло-угловатая", "плосковыпуклая", "прямоугольная", "ромбическая", "сжато-прямоугольная", "сжато-эллиптическая", "сфероидальная", "угловатая", "эллиптическая"],
                "contains": [],
                "relates_to_the_group": ["морфологические_характеристики"],
            },
            {
                "область": "палинология", 
                "term": "выпукло-вогнутая", 
                "termNormalize": getTokensFromTexts(["выпукло-вогнутая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "лопастая", 
                "termNormalize": getTokensFromTexts(["лопастая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "округлая", 
                "termNormalize": getTokensFromTexts(["округлая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "округло-угловатая", 
                "termNormalize": getTokensFromTexts(["округло-угловатая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "плосковыпуклая", 
                "termNormalize": getTokensFromTexts(["плосковыпуклая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "прямоугольная", 
                "termNormalize": getTokensFromTexts(["прямоугольная"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "ромбическая", 
                "termNormalize": getTokensFromTexts(["ромбическая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "сжато-прямоугольная", 
                "termNormalize": getTokensFromTexts(["сжато-прямоугольная"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "сжато-эллиптическая", 
                "termNormalize": getTokensFromTexts(["сжато-эллиптическая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "сфероидальная", 
                "termNormalize": getTokensFromTexts(["сфероидальная"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "угловатая", 
                "termNormalize": getTokensFromTexts(["угловатая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "эллиптическая", 
                "termNormalize": getTokensFromTexts(["эллиптическая"])[0],
                "prevTerm": "форма_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "клетки_пыльцевого_зерна", 
                "termNormalize": getTokensFromTexts(["клетки_пыльцевого_зерна"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["вегетативные", "генеративные"],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "клетки", 
                "termNormalize": getTokensFromTexts(["клетки"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["вегетативные", "генеративные"],
                "contains": [],
                "relates_to_the_group": ["форма_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "вегетативные", 
                "termNormalize": getTokensFromTexts(["вегетативные"])[0],
                "prevTerm": "клетки_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["клетки_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "генеративные", 
                "termNormalize": getTokensFromTexts(["генеративные"])[0],
                "prevTerm": "клетки_пыльцевого_зерна", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["клетки_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "ядро", 
                "termNormalize": getTokensFromTexts(["ядро"])[0],
                "prevTerm": "морфологические_характеристики", 
                "moveToPrev": False,
                "divided_in_groups": ["ядро вегетативной клетки", "ядро генеративной клетки"],
                "contains": [],
                "relates_to_the_group": ["клетки_пыльцевого_зерна"],
            },
            {
                "область": "палинология", 
                "term": "ядро_вегетативной_клетки",
                "termNormalize": getTokensFromTexts(["ядро_вегетативной_клетки"])[0],
                "prevTerm": "ядро", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["ядро"],
            },
            {
                "область": "палинология", 
                "term": "ядро_генеративной_клетки", 
                "termNormalize": getTokensFromTexts(["ядро_генеративной_клетки"])[0],
                "prevTerm": "ядро", 
                "moveToPrev": True,
                "divided_in_groups": [],
                "contains": [],
                "relates_to_the_group": ["ядро"],
            },
        ]

        for item in listTerms:
            field = Область(item["область"])
            print(item["term"].replace(" ", "_"))
            newTerm = Термин(item["term"].replace(" ", "_"))
            
            newTerm.isTermOf = field
            newTerm.moveToPrev = item["moveToPrev"]
            newTerm.termNormalize = item["termNormalize"][0]
            if item["prevTerm"] != "":
                prevTerm = Термин(item["prevTerm"].replace(" ", "_"))
                newTerm.hasPrevTerm = prevTerm
            for t in item["divided_in_groups"]:
                newTerm.divided_in_groups.append(t)
            for t in item["contains"]:
                newTerm.contains.append(t)
            for t in item["relates_to_the_group"]:
                newTerm.relates_to_the_group.append(t)

        self.onto.save(self.path) 

    def getDividedInGroupsByTerm(self, term):
        query = queries.getGroupsByTerm(term)
        resultGroups = self.graph.query(query)
        listGroups = []
        for itemGroup in resultGroups:
            group = str(itemGroup['group'].toPython())
            group = re.sub(r'.*#',"", group)

            listGroups.append({"answer": group, "correct": True})
        
        #print(listTerms)
        return listGroups

    def getAnswersByTypeTemplate(self, typeTemp, tokens, fieldObj):
        listTerms, listTermsNormalize = self.getTermsNormilizeOfField(fieldObj)
        for token in tokens:
            if token in listTermsNormalize:
                index = listTermsNormalize.index(token)
                term = listTerms[index]
                if typeTemp == typeTemplate.SubClasses.value:
                    listGroups = self.getDividedInGroupsByTerm(term)
                    return listGroups
        return []

    def getAnswersByTaskAuto(self, text, fieldObj):
        autoGen = AutoGeneration()
        print(text)
        typeTemp, tokens = autoGen.toDetermineType(text)
        listAnswers = []
        if typeTemp != "":
            listAnswers = self.getAnswersByTypeTemplate(typeTemp, tokens[0], fieldObj)
        return listAnswers

    def getTermsBySubjArea(self, fieldObj):
        query = queries.getTermsOfField(fieldObj)
        resultTerms = self.graph.query(query)
        listTerms = []
        for itemTerm in resultTerms:
            term = str(itemTerm['term'].toPython())
            term = re.sub(r'.*#',"", term)
            termNormalize = str(itemTerm['termNormalize'].toPython())
            termNormalize = re.sub(r'.*#',"", termNormalize)
            termStr = term.replace("_", " ")
            termStr = termStr[0].upper() + termStr[1:]
            item = {"term": term, "termNormalize": termNormalize, "termStr": termStr}
            listTerms.append(item)
        
        listTerms.sort(key=lambda x:x["term"])
        #print(listTerms)
        return listTerms

    def getLecturesByTerms(self, terms):
        lectures = {}
        for term in terms:
            query = queries.getLecturesByTerm(term)
            resultLectures = self.graph.query(query)
            listLectures = []
            for itemLecture in resultLectures:
                lectureObj = str(itemLecture['lectureObj'].toPython())
                lectureObj = re.sub(r'.*#',"", lectureObj)
                lectureName = str(itemLecture['lectureName'].toPython())
                lectureName = re.sub(r'.*#',"", lectureName)
                item = {"lectureObj": lectureObj, "lectureName": lectureName}
                listLectures.append(item)
            lectures[term] = listLectures

        #print(lectures)
        return lectures

def main():
    ont = TestingService()
    #ont.createTest(testObj)
    #ont.getTestsWithAnswers()
    #ont.updateTest({'testName': 'Морфология пыльцевых зерен', 'tasks': [{'taskObj': 'задание16', 'question': 'На какие две группы можно разделить все апертуры?', 'type': '1', 'answers': [], 'term': 'апертура'}, {'taskObj': 'задание17', 'question': 'Чем сложная апертура отличается от простой? Приведи примеры сложных и простых апертур.', 'type': '1', 'answers': [], 'term': 'апертура'}, {'taskObj': 'задание18', 'question': 'Как называется оболочка пыльцевого зерна?', 'type': '2', 'answers': [{'answerObj': 'ответ19', 'answer': 'Спородерма', 'correct': True}, {'answerObj': 'ответ20', 'answer': 'Экзина', 'correct': False}, {'answerObj': 'ответ21', 'answer': 'Периспорий', 'correct': False}, {'answerObj': 'ответ22', 'answer': 'Экзоспорий', 'correct': False}], 'term': 'оболочка_пыльцевого_зерна'}, {'taskObj': 'задание19', 'question': 'Как называется апертура, у которой отношение длины к ширине больше или равно 2?', 'type': '2', 'answers': [{'answerObj': 'ответ23', 'answer': 'Пора', 'correct': False}, {'answerObj': 'ответ24', 'answer': 'Ора', 'correct': False}, {'answerObj': 'ответ25', 'answer': 'Борозда', 'correct': True}, {'answerObj': 'ответ26', 'answer': 'Лептома', 'correct': False}], 'term': 'апертура'}, {'taskObj': 'задание20', 'question': 'К какой группе апертур относится ора?', 'type': '1', 'answers': [], 'term': 'апертура'}, {'taskObj': 'задание21', 'question': 'Что такое лептома?', 'type': '2', 'answers': [{'answerObj': 'ответ27', 'answer': 'Истончённая область спородермы на дистальной стороне п.з., выполняет функцию апертуры, характерна для голосеменных', 'correct': True}, {'answerObj': 'ответ28', 'answer': 'Поверхность зерна, ограниченная двумя соседними бороздами (порами)', 'correct': False}, {'answerObj': 'ответ29', 'answer': 'Внутренняя часть сложной апертуры, имеющая округлую или эллипсоидальную форму', 'correct': False}, {'answerObj': 'ответ30', 'answer': 'Простая апертура изогнутой формы.', 'correct': False}], 'term': 'апертура'}, {'taskObj': 'задание22', 'question': 'Как называется центральное утолщение поровой или бороздной мембраны?', 'type': '2', 'answers': [{'answerObj': 'ответ31', 'answer': 'Мезокольпиум', 'correct': False}, {'answerObj': 'ответ32', 'answer': 'Оперкулюм', 'correct': True}, {'answerObj': 'ответ33', 'answer': 'Мезопориум', 'correct': False}, {'answerObj': 'ответ34', 'answer': 'Апопориум', 'correct': False}], 'term': 'апертура'}, {'taskObj': 'задание23', 'question': 'Может ли пыльцевое зерно быть без апертуры?', 'type': '2', 'answers': [{'answerObj': 'ответ35', 'answer': 'Да', 'correct': True}, {'answerObj': 'ответ36', 'answer': 'Нет', 'correct': False}], 'term': 'апертура'}, {'taskObj': 'задание24', 'question': 'Что такое \
#скульптура п.з., приведи примеры нескольких типов структур?', 'type': '1', 'answers': [], 'term': 'скульптура_пыльцевого_зерна'}, {'taskObj': 'задание25', 'question': 'На какие слои можно подразделить экзину?', 'type': '1', 'answers': [], 'term': 'оболочка_пыльцевого_зерна'}, {'taskObj': 'задание26', 'question': 'На какие слои делится интина?', 'type': '1', 'answers': [], 'term': 'оболочка_пыльцевого_зерна'}, {'taskObj': 'задание27', 'question': 'Что относится к типам текстуры?', 'type': '2', 'answers': [{'answerObj': 'ответ37', 'answer': 'Внутрисетчатая', 'correct': True}, {'answerObj': 'ответ38', 'answer': 'Столбчатая', 'correct': False}, {'answerObj': 'ответ39', 'answer': 'Бугорчатая', 'correct': False}, {'answerObj': 'ответ40', 'answer': 'Шиповатая', 'correct': False}], 'term': 'скульптура_пыльцевого_зерна'}, {'taskObj': 'задание28', 'question': 'За счет элементов какого слоя спородермы образована структура?', 'type': '2', 'answers': [{'answerObj': 'ответ41', 'answer': 'Экзина', 'correct': True}, {'answerObj': 'ответ42', 'answer': 'Интина', 'correct': False}, {'answerObj': 'ответ43', 'answer': 'Эндоспорий', 'correct': False}, {'answerObj': 'ответ44', 'answer': 'Гиалина', 'correct': False}], 'term': 'оболочка_пыльцевого_зерна'}, {'taskObj': 'задание29', 'question': 'На какие группы делятся пыльцевые зерна по длине наибольшей оси?', 'type': '1', 'answers': [], 'term': 'размер_пыльцевого_зерна'}, {'taskObj': 'задание30', 'question': 'Для каких растений характерны щели? Выберете несколько ответов.', 'type': '3', 'answers': [{'answerObj': 'ответ45', 'answer': 'Мхов', 'correct': True}, {'answerObj': 'ответ46', 'answer': 'Лилейных', 'correct': False}, {'answerObj': 'ответ47', 'answer': 'Плаунов', 'correct': True}, {'answerObj': 'ответ48', 'answer': 'Злаковые', 'correct': False}, {'answerObj': 'ответ49', 'answer': 'Норичниковых', 'correct': False}, {'answerObj': 'ответ50', 'answer': 'Хвощей', 'correct': True}, {'answerObj': 'ответ51', 'answer': 'Папоротников', 'correct': True}], 'term': 'апертура'}, {'taskObj': 'задание31', 'question': 'Какие морфологические характеристики помогают определить таксономическую принадлежность пыльцевого зерна?', 'type': '1', 'answers': [], \
#'term': 'морфологические_характеристики'}, {'taskObj': 'задание32', 'question': 'Как называется часть поверхности пыльцевого зерна, обращённая к центру тетрады?', 'type': '3', 'answers': [], 'term': 'поверхность_пыльцевого_зерна'}, {'taskObj': 'задание33', 'question': 'Как называется часть поверхности пыльцевого зерна, обращённая наружу и максимально удаленная от тетрады?', 'type': '2', 'answers': [{'answerObj': 'ответ56', 'answer': 'Дистальный полюс', 'correct': True}, {'answerObj': 'ответ57', 'answer': 'Проксимальный полюс', 'correct': False}, {'answerObj': 'ответ58', 'answer': 'Экваториальная ось', 'correct': False}, {'answerObj': 'ответ59', 'answer': 'Полярная ось', 'correct': False}], 'term': 'поверхность_пыльцевого_зерна'}, {'taskObj': 'задание34', 'question': 'Как называется линия, соединяющая проксимальный и дистальный полюса?', 'type': '2', 'answers': [{'answerObj': 'ответ60', 'answer': 'Дистальный полюс', 'correct': False}, {'answerObj': 'ответ61', 'answer': 'Проксимальный полюс', 'correct': False}, {'answerObj': 'ответ62', 'answer': 'Экваториальная ось', 'correct': False}, {'answerObj': 'ответ63', 'answer': 'Полярная ось', 'correct': True}], 'term': 'полярность_пыльцевого_зерна'}, {'taskObj': 'задание35', 'question': 'Что зависит от соотношения длины полярной оси к экваториальному диаметру (P/E)?', 'type': '2', 'answers': [{'answerObj': 'ответ64', 'answer': 'Симметрия пыльцевого зерна', 'correct': False}, {'answerObj': 'ответ65', 'answer': 'форма пыльцевого зерна', 'correct': True}, {'answerObj': 'ответ66', 'answer': 'размер пыльцевого зерна', 'correct': False}, {'answerObj': 'ответ67', 'answer': 'структура пыльцевого зерна', 'correct': False}], 'term': 'форма_пыльцевого_зерна'}], 'prevNameTest': 'Морфология пыльцевых зерен'})
    #ont.deleteAnswer("ss")
    #ont.getAttempts("Ey0mfGCJ4kSVCNEZa2KzPGM8BYn1", "Test_10")
    #ont.getUser("OUXFGSzNAlOYes3UEbvo33kcGuE3")
    #ont.createTerms()
    #term = ont.getTermByTask({"question": "6.	Что такое лептома?"})
    user= {
        "userObj": "пользователь1",
        "uid": "Ey0mfGCJ4kSVCNEZa2KzPGM8BYn1",
    }
    ont.getTermsByUser("пользователь1", "Ey0mfGCJ4kSVCNEZa2KzPGM8BYn1")
    #ont.getTermsScoresByLastAttempts(user)

if __name__ == "__main__":
    main()