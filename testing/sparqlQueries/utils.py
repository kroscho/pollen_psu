def getTypeTaskValue(typeStr):
    if typeStr == "Текстовый":
        return "1"
    elif typeStr == "Единственный":
        return "2"
    elif typeStr == "Множественный":
        return "3"
    else:
        return "4"

def checkCorrectAnswer(answer, correctsAnswers):
    for correct in correctsAnswers:
        if answer == correct:
            return True
    return False

def checkAnswer(trueTask, userTask):
    userAnswer = userTask['answer']
    if userTask['type'] != "3":
        for answer in trueTask['answers']:
            if answer['answer'] == userAnswer and answer['correct'] == True:
                return {"sum": 1, "answerObj": [answer["answerObj"]], "correct": [True]}
            elif answer['answer'] == userAnswer:
                return {"sum": 0, "answerObj": [answer["answerObj"]], "correct": [False]}
    else:
        result = {"sum": 0, "answerObj": [], "correct": []}
        if userTask['type'] != "1":
            correctAnswers = []
            allAnswers = []
            objAnswers = []
            for answer in trueTask['answers']:
                if answer['correct'] == True:
                    correctAnswers.append(answer['answer'])
                allAnswers.append(answer["answer"])
                objAnswers.append(answer['answerObj'])

            print("UserAnswers CorrectAnswers: ", userAnswer, correctAnswers)
            for userAnsw in userAnswer:
                if userAnsw in correctAnswers:
                    result["sum"] += 1
                    index = allAnswers.index(userAnsw)
                    result["answerObj"].append(objAnswers[index])
                    result["correct"].append(True)
                else:
                    result["sum"] -= 1
                    index = allAnswers.index(userAnsw)
                    result["answerObj"].append(objAnswers[index])
                    result["correct"].append(False)
            if result["sum"] <= 0:
                result["sum"] = 0
            else:
                result["sum"] = result["sum"] / len(correctAnswers)
            return result
        return {"sum": 0, "answerObj": [], "correct": []}