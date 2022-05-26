
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