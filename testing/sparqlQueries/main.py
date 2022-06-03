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
                term = self.getTermByTask(task)
            else:
                if tTask == typeTask.Single.value:
                    newQuestion = Единственный()
                elif tTask == typeTask.Multiple.value:
                    newQuestion = Множественный()
                else:
                    newQuestion = Логический()

                newQuestion.textQuestion = task['question']
                term = self.getTermByTask(task)
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
            if term:
                termObj = Термин(term["term"])
                newTask.hasTerm = termObj
        
        newTest.has_group_of_task.append(newGroupOfTasks)
        newGroupOfTasks.is_group_of_task.append(newTest)
        module.has_test.append(newTest)
        newTest.is_test_of.append(module)

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

        course = Курс(courseObj)
        newModule = Модуль()

        newModule.nameModule = module['nameModule']
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
                    term = self.getTermByTask(task)
                else:
                    if tTask == typeTask.Single.value:
                        newQuestion = Единственный()
                    elif tTask == typeTask.Multiple.value:
                        newQuestion = Множественный()
                    else:
                        newQuestion = Логический()

                    newQuestion.textQuestion = task['question']
                    term = self.getTermByTask(task)
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
                if term:
                    termObj = Термин(term["term"])
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
                questionText = str(itemTask['questText'].toPython())
                questionText = re.sub(r'.*#',"", questionText)
                typeQuestion = str(itemTask['taskType'].toPython())
                typeQuestion = re.sub(r'.*#',"", typeQuestion)

                task = {"taskObj": taskObj, "question": questionText, "type": getTypeTaskValue(typeQuestion)}

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
                    termsScores[termObj]["sumScore"] += sum
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
                        print("ASNWERSCOPY: ", answersCopy)
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

    def getModulesOfCourse(self, courseObj):
        query = queries.getModulesOfCourse(courseObj)
        resultModules = self.graph.query(query)
        listModules = []
        for itemModule in resultModules:
            moduleObj = str(itemModule['moduleObj'].toPython())
            moduleObj = re.sub(r'.*#',"", moduleObj)
            nameModule = str(itemModule['nameModule'].toPython())
            nameModule = re.sub(r'.*#',"", nameModule)
            listTests = self.getTestsOfModule(moduleObj)
            item = {"moduleObj": moduleObj, "nameModule": nameModule, "tests": listTests}
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
                if termObj != "":
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

    def getTermByTask(self, task):
        tokens = getTokensFromTexts([task["question"]])
        terms = self.getTermsOfField("палинология")
        print(tokens)
        term = getTermFromText(tokens[0], terms)
        print(term)
        return term

    def getKnownTermsByUser(self, userObj):
        query = queries.getKnownTermsByUser(userObj)
        resultTerms = self.graph.query(query)
        listTerms = []
        for itemTerm in resultTerms:
            term = str(itemTerm['term'].toPython())
            term = re.sub(r'.*#',"", term)
            listTerms.append(term)
        
        return listTerms

    def getUnknownTermsByUser(self, userObj):
        query = queries.getUnknownTermsByUser(userObj)
        resultTerms = self.graph.query(query)
        listTerms = []
        for itemTerm in resultTerms:
            term = str(itemTerm['term'].toPython())
            term = re.sub(r'.*#',"", term)
            listTerms.append(term)
        
        return listTerms

    def getTermsByUser(self, userObj):
        knownTerms = self.getKnownTermsByUser(userObj)
        unknownTerms = self.getUnknownTermsByUser(userObj)
        item = {"knownTerms": knownTerms, "unknownTerms": unknownTerms}
        return item

    def createTerms(self):
        with self.onto:
            class Предметная_область(Thing):
                pass
            class Область(Предметная_область):
                pass
            class Термин(Предметная_область):
                pass

        listTerms = [
            {"область": "палинология", "term": "палинология", "prevTerm": "", "moveToPrev": False},
            {"область": "палинология", "term": "морфологические_характеристики", "prevTerm": "", "moveToPrev": False},
            {"область": "палинология", "term": "апертура", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "простая апертура", "prevTerm": "апертура", "moveToPrev": True},
            {"область": "палинология", "term": "сложная апертура", "prevTerm": "апертура", "moveToPrev": True},
            {"область": "палинология", "term": "борозды", "prevTerm": "простая апертура", "moveToPrev": True},
            {"область": "палинология", "term": "лептомы", "prevTerm": "простая апертура", "moveToPrev": True},
            {"область": "палинология", "term": "поры", "prevTerm": "простая апертура", "moveToPrev": True},
            {"область": "палинология", "term": "руги", "prevTerm": "простая апертура", "moveToPrev": True},
            {"область": "палинология", "term": "щели", "prevTerm": "простая апертура", "moveToPrev": True},
            {"область": "палинология", "term": "бороздо-оровые", "prevTerm": "сложная апертура", "moveToPrev": True},
            {"область": "палинология", "term": "бороздо-поровые", "prevTerm": "сложная апертура", "moveToPrev": True},
            {"область": "палинология", "term": "порово-оровые", "prevTerm": "сложная апертура", "moveToPrev": True},
            {"область": "палинология", "term": "оболочка_пыльцевого_зерна", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "интина", "prevTerm": "оболочка_пыльцевого_зерна", "moveToPrev": True},
            #{"область": "палинология", "term": "экзина", "prevTerm": "оболочка_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "экзинтина", "prevTerm": "интина", "moveToPrev": True},
            {"область": "палинология", "term": "эуинтина", "prevTerm": "интина", "moveToPrev": True},
            #{"область": "палинология", "term": "мэкзина", "prevTerm": "экзина", "moveToPrev": True},
            #{"область": "палинология", "term": "эктэкзина", "prevTerm": "экзина", "moveToPrev": True},
            #{"область": "палинология", "term": "эндэкзина", "prevTerm": "экзина", "moveToPrev": True},
            {"область": "палинология", "term": "скульптура_пыльцевого_зерна", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "поверхность_пыльцевого_зерна", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "бугорчатая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "гладкая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "зернистая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "морщинистая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "сетчатая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "столбчатая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "струйчатая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "шероховатая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "шиповватая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "ямчатая", "prevTerm": "cкульптура_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "полярность_пыльцевого_зерна", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "неполярное", "prevTerm": "полярность_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "равнополярное", "prevTerm": "полярность_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "разнополярное", "prevTerm": "полярность_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "проекция_пыльцевого_зерна", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "полярная", "prevTerm": "проекция_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "экваториальная", "prevTerm": "проекция_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "размер_пыльцевого_зерна", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "мелкие", "prevTerm": "размер_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "очень мелкие", "prevTerm": "размер_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "средние", "prevTerm": "размер_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "крупные", "prevTerm": "размер_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "очень крупные", "prevTerm": "размер_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "гигантские", "prevTerm": "размер_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "форма_пыльцевого_зерна", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "выпукло-вогнутая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "лопастая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "округлая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "округло-угловатая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "плосковыпуклая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "прямоугольная", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "ромбическая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "сжато-прямоугольная", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "сжато-эллиптическая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "сфероидальная", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "угловатая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "эллиптическая", "prevTerm": "форма_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "клетки_пыльцевого_зерна", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "вегетативные", "prevTerm": "клетки_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "генеративные", "prevTerm": "клетки_пыльцевого_зерна", "moveToPrev": True},
            {"область": "палинология", "term": "ядро", "prevTerm": "морфологические_характеристики", "moveToPrev": False},
            {"область": "палинология", "term": "ядро вегетативной клетки", "prevTerm": "ядро", "moveToPrev": True},
            {"область": "палинология", "term": "ядро генеративной клетки", "prevTerm": "ядро", "moveToPrev": True},
        ]

        for item in listTerms:
            field = Область(item["область"])
            print(item["term"].replace(" ", "_"))
            newTerm = Термин(item["term"].replace(" ", "_"))
            
            newTerm.isTermOf = field
            newTerm.moveToPrev = item["moveToPrev"]
            if item["prevTerm"] != "":
                prevTerm = Термин(item["prevTerm"].replace(" ", "_"))
                newTerm.hasPrevTerm = prevTerm

        self.onto.save(self.path) 

def main():
    ont = TestingService()
    #ont.createTest(testObj)
    #ont.getTestsWithAnswers()
    #ont.updateTest({})
    #ont.deleteAnswer("ss")
    #ont.getAttempts("Ey0mfGCJ4kSVCNEZa2KzPGM8BYn1", "Test_10")
    #ont.getUser("OUXFGSzNAlOYes3UEbvo33kcGuE3")
    #ont.createTerms()
    #term = ont.getTermByTask({"question": "6.	Что такое лептома?"})


if __name__ == "__main__":
    main()