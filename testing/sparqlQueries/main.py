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
from testing.sparqlQueries.utils import checkAnswer, checkCorrectAnswer, getTypeTaskValue

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
            
    def createTest(self, testObj):

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


        newTest = Тест()
        newGroupOfTasks = Группа_заданий()

        newTest.testName = testObj['nameTest']
        listTasks = testObj['tasks']

        for task in listTasks:
            newTask = Задание()
            newQuestion = Вопрос()
            tTask = task['type']
            if tTask == typeTask.Text.value:
                newQuestion = Текстовый()
                newQuestion.textQuestion = task['question']
            else:
                if tTask == typeTask.Single.value:
                    newQuestion = Единственный()
                elif tTask == typeTask.Multiple.value:
                    newQuestion = Множественный()
                else:
                    newQuestion = Логический()

                newQuestion.textQuestion = task['question']
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
        
        newTest.has_group_of_task.append(newGroupOfTasks)
        newGroupOfTasks.is_group_of_task.append(newTest)

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
            if updateTest['prevNameTest'] != updateTest['nameTest']:
                curTest = Тест(testObj)
                curTest.testName = updateTest['nameTest']

            self.deleteTasks(groupTask)
            
            for task in updateTest['tasks']:
                newTask = Задание()
                newQuestion = Вопрос()
                tTask = task['type']
                if tTask == typeTask.Text.value:
                    newQuestion = Текстовый()
                    newQuestion.textQuestion = task['question']
                else:
                    if tTask == typeTask.Single.value:
                        newQuestion = Единственный()
                    elif tTask == typeTask.Multiple.value:
                        newQuestion = Множественный()
                    else:
                        newQuestion = Логический()

                    newQuestion.textQuestion = task['question']
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
            if nameTest != deleteTest['nameTest']:
                continue
            groupTask = str(itemTest['groupTasks'].toPython())
            groupTask = re.sub(r'.*#',"", groupTask)
            groupTaskObj = Группа_заданий(groupTask)
            print("GROUP TASK: ", groupTaskObj)
            testItem["nameTest"] = nameTest
            
            self.deleteTasks(groupTask)
            destroy_entity(Группа_заданий(groupTaskObj))
            destroy_entity(Тест(testObj))
        print("Тест удален!")
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
            testItem["nameTest"] = nameTest
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
            testItem["nameTest"] = nameTest
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
            if test['nameTest'].replace(" ", "_") == testName.replace(" ", "_"):
                return test
        return {}

     # получение даты прохождения теста в виде объекта
    def getNowDate(self):
        now = datetime.now()
        strDate = datetime(now.year, now.month, now.day, 0, 0, 0).isoformat()
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
            class Попытка_прохождения_теста(Thing):
                pass
            class Элемент_теста(Thing):
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
        for i in range(len(tasks)):
            newTestElement = Элемент_теста()
            newAttempt.has_test_element.append(newTestElement)
            newTestElement.is_test_element_of.append(newAttempt)
            task = Задание(tasks[i]["taskObj"])
            newTestElement.has_task.append(task)
            if userAnswers[i]["type"] != "1":
                result = checkAnswer(trueAnswers[i], userAnswers[i])
                print("RESULT SUM: ", result["sum"])
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
                    newAnsw.rightAnswer = answ_correct
                    newAnsw.textAnswer = textAnswer
                    newTestElement.has_answer.append(newAnsw)
            else:
                newAnsw = ОтветыСтудента()
                newAnsw.rightAnswer = False
                newAnsw.textAnswer = userAnswers[i]["answer"]
                newTestElement.has_answer.append(newAnsw)
        succesfullAttempt = False
        if sum / len(tasks) > 0.3:
            succesfullAttempt = True
        newAttempt.succesfullAttempt = succesfullAttempt
        newAttempt.dateAndTime = self.getNowDate()
        newAttempt.percentCompleteOfTest = sum / len(tasks)

        self.onto.save(self.path)
        return sum
    
    def getResultAttempt(self, answers, user):
        nameTest = answers['nameTest']
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
            userItem = {"userObj": userObj, "firstName": firstName, "lastName": lastName, "email": email, "role": role, "uid": uid}
        
        return userItem
    
    def getAttempts(self, user_uid, nameTest):
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
            testCopy["percentComplete"] = percentComplete
            testCopy["succesfull"] = succesfull
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
                    correctAnsw = True if correctAnsw == "True" else False
                    if taskType == "1":
                        answersCopy = [{"answerObj": answObj, "answer": answText, "correct": False, "correctByUser": correctAnsw}]
                        print("ASNWERSCOPY: ", answersCopy)
                    for j in range(len(answersCopy)):
                        if answersCopy[j]['answer'] == answText:
                            answersCopy[j]["correctByUser"] = correctAnsw
                        if "correctByUser" not in answersCopy[j]:
                            answersCopy[j]["correctByUser"] = None
                    testCopy["tasks"][i]["answers"] = answersCopy
                i += 1
            listAttempts.append(testCopy)
        return listAttempts


def main():
    ont = TestingService()
    #ont.createTest(testObj)
    #ont.getTestsWithAnswers()
    #ont.updateTest({})
    #ont.deleteAnswer("ss")
    ont.getAttempts("Ey0mfGCJ4kSVCNEZa2KzPGM8BYn1", "Test_10")

if __name__ == "__main__":
    main()