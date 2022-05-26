from re import I
from itsdangerous import json
from owlready2 import *
from enum import Enum

path_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(path_dir)
print(path_dir)

from testing.sparqlQueries.config import config
import testing.sparqlQueries.queries as queries
from testing.sparqlQueries.utils import checkCorrectAnswer, getTypeTaskValue

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
            testItem = {}
            nameTest = str(itemTest['nameTest'].toPython())
            nameTest = re.sub(r'.*#',"", nameTest)
            if nameTest != updateTest['nameTest']:
                continue
            groupTask = str(itemTest['groupTasks'].toPython())
            groupTask = re.sub(r'.*#',"", groupTask)
            groupTaskObj = Группа_заданий(groupTask)
            print("GROUP TASK: ", groupTaskObj)
            testItem["nameTest"] = nameTest
            
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
                query = queries.getCorrectAnswersByTask(taskObj, groupTask)
                resultCorrectAnswers = self.graph.query(query)
                listAnswers = []
                listCorrects = []
                for correctAnsw in resultCorrectAnswers:
                    correct = str(correctAnsw['answObj'].toPython())
                    correct = re.sub(r'.*#',"", correct)
                    listCorrects.append(correct)
                print("CORRECTS: ", listCorrects)
                for itemAnsw in resultAnswers:
                    answerObj = str(itemAnsw['answObj'].toPython())
                    answerObj = re.sub(r'.*#',"", answerObj)
                    answerText = str(itemAnsw['answText'].toPython())
                    answerText = re.sub(r'.*#',"", answerText)
                    listAnswers.append({"answer": answerText, "correct": checkCorrectAnswer(answerObj, listCorrects)})
                task["answers"] = listAnswers
                listTasks.append(task)
            testItem["tasks"] = listTasks
            listTests.append(testItem)
        print(listTests)
        return listTests

    def getTestWithAnswers(self, testName):
        tests = self.getTestsWithAnswers()
        for test in tests:
            if test['nameTest'].replace(" ", "_") == testName:
                return test
        return {}

def main():
    ont = TestingService()
    testObj = {
                "nameTest": "UNIX",
                "variant": "1",
                "tasks": [
                    {
                        "type": "1",
                        "question": "вопрос_1",
                        "answers": [
                            {
                                "answer": "ответ_1",
                                "correct": False,
                            },
                            {
                                "answer": "ответ_2",
                                "correct": True
                            },
                            {
                                "answer": "ответ_3",
                                "correct": True
                            }
                        ]
                    },
                    {
                        "type": "3",
                        "question": "вопрос_2",
                        "answers": [
                            {
                                "answer": "ответ 1",
                                "correct": False,
                            },
                            {
                                "answer": "ответ 2",
                                "correct": True
                            },
                            {
                                "answer": "ответ 3",
                                "correct": False,
                            },
                            {
                                "answer": "ответ 4",
                                "correct": True,
                            },
                        ]
                    },
                ]
            }
    #ont.createTest(testObj)
    #ont.getTestsWithAnswers()
    #ont.updateTest({})
    #ont.deleteAnswer("ss")

if __name__ == "__main__":
    main()