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