# запрос на получение названий тестов и групп заданий
def getTestsNames():
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?nameTest ?groupTasks ?testObj " \
            "WHERE { " \
            "?testObj rdf:type tst:Тест. " \
            "?testObj tst:testName ?nameTest. " \
            "?testObj tst:has_group_of_task ?groupTasks. " \
            "}"
    return query

# запрос на получение заданий и их вопросов
def getTasksQuestions(groupTask):
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?task ?questText ?taskType ?quest " \
            "WHERE { " \
            "?task tst:is_task_of tst:%s. " \
            "?task tst:task_has_question ?quest. " \
            "?quest tst:textQuestion ?questText. " \
            "?quest rdf:type ?taskType. " \
            "?taskType rdfs:subClassOf ?obj " \
            "}" % (groupTask)
    return query

# запрос на получение ответов на задание
def getAnswersByTask(taskObj, groupTask):
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?answObj ?answText " \
            "WHERE { " \
            "tst:%s tst:is_task_of ?%s. " \
            "tst:%s tst:task_has_answer ?answObj. " \
            "?answObj tst:textAnswer ?answText. " \
            "}" % (taskObj, groupTask, taskObj)
    return query

# запрос на получение правильных ответов на задание
def getCorrectAnswersByTask(taskObj, groupTask):
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?answObj ?answText " \
            "WHERE { " \
            "tst:%s tst:is_task_of ?%s. " \
            "tst:%s tst:task_has_answer ?answObj. " \
            "?answObj tst:textAnswer ?answText. " \
            "?answObj tst:is_correct_answer_of ?corrects. " \
            "}" % (taskObj, groupTask, taskObj)
    return query

# запрос на получение пользователя
def getUsers():
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?userObj ?uid ?firstName ?lastName ?email ?role " \
            "WHERE { " \
            "?userObj rdf:type tst:Пользователь. " \
            "?userObj tst:uid ?uid. " \
            "?userObj tst:firstName ?firstName. " \
            "?userObj tst:lastName ?lastName. " \
            "?userObj tst:email ?email. " \
            "?userObj tst:role ?role. " \
            "}"
    return query

# запрос на получение попыток пользователя
def getAttempts(userObj, testObj):
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?attemptObj ?percentComplete ?succesfull " \
            "WHERE { " \
            "tst:%s tst:has_attempt_to_pass_test ?attemptObj. " \
            "?attemptObj tst:relates_to_test tst:%s. " \
            "?attemptObj tst:percentCompleteOfTest ?percentComplete. " \
            "?attemptObj tst:succesfullAttempt ?succesfull. " \
            "}" % (userObj, testObj)
    return query

# запрос на получение элементов теста попытки
def getTestElements(attemptObj):
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?testElem " \
            "WHERE { " \
            "tst:%s tst:has_test_element ?testElem. " \
            "}" % (attemptObj)
    return query

# запрос на получение ответов элемента теста и их корректность
def getAnswersAndCorrectByTestElem(testElementObj):
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?answerObj ?correct ?textAnswer " \
            "WHERE { " \
            "tst:%s tst:has_answer ?answerObj. " \
            "?answerObj tst:rightAnswer ?correct. " \
            "?answerObj tst:textAnswer ?textAnswer. " \
            "}" % (testElementObj)
    return query

# запрос на получение текста ответа
def getTextAnswerByAnswer(answerObj):
    query = "PREFIX tst: <http://www.semanticweb.org/nike0/ontologies/2022/4/untitled-ontology-16#>" \
            "SELECT ?textAnswer " \
            "WHERE { " \
            "tst:%s tst:textAnswer ?textAnswer. " \
            "}" % (answerObj)
    return query