import pytest
from bots.bot_functions import analyze_text
from bots.bot_functions import activators, answers, Commands, add_person


list_of_commands = []
commands = []
for key in activators:
    list_of_commands.append(Commands(activators[key], list(map(add_person, answers[key]))))
    commands.extend(activators[key])

    
def test_analyze_text_1():
    assert analyze_text("привет", commands) == "привет"
   

def test_analyze_text_2():
    assert analyze_text("здравствуй", commands) == "здравствуй"


def test_analyze_text_3():
    assert analyze_text("прощай", commands) == "прощай"


def test_analyze_text_4():
    assert analyze_text("пока", commands) == "пока"


def test_analyze_text_5():
    assert analyze_text("досвидания", commands) == "досвидания"


def test_analyze_text_6():
    assert analyze_text("какдела?", commands) == "какдела?"


def test_analyze_text_7():
    assert analyze_text("ктоты?", commands) == "ктоты?"


def test_analyze_text_8():
    assert analyze_text("случайно", commands) == "случайно"


def test_analyze_text_9():
    assert analyze_text("рандом", commands) == "рандом"


def test_analyze_text_10():
    assert analyze_text("фотобокс", commands) == "фотобокс"


def test_analyze_text_11():
    assert analyze_text("ктотебясоздал", commands) == "ктотебясоздал"


def test_analyze_text_12():
    assert analyze_text("ссылка", commands) == "ссылка"


def test_analyze_text_13():
    assert analyze_text("сайт", commands) == "сайт"


def test_analyze_text_14():
    assert analyze_text("фото", commands) == "фото"


def test_analyze_text_15():
    assert analyze_text("фотография", commands) == "фотография"


def test_analyze_text_16():
    assert analyze_text("картинка", commands) == "картинка"


def test_analyze_text_17():
    assert analyze_text("команда", commands) == "команда"


def test_analyze_text_18():
    assert analyze_text("чтотыумеешь", commands) == "чтотыумеешь"


def test_analyze_text_19():
    assert analyze_text("управление", commands) == "управление"


def test_analyze_text_20():
    assert analyze_text("икит", commands) == "икит"


def test_analyze_text_21():
    assert analyze_text("прив", commands) == "привет"


def test_analyze_text_22():
    assert analyze_text("ик", commands) == "икит"


def test_analyze_text_23():
    assert analyze_text("здравствуйте", commands) == "здравствуй"


def test_analyze_text_24():
    assert analyze_text("кортинка", commands) == "картинка"


def test_analyze_text_25():
    assert analyze_text("ававвав", commands) == "Nope"


def test_analyze_text_26():
    assert analyze_text("доставка", commands) == "Nope"


def test_analyze_text_27():
    assert analyze_text("какдела", commands) == "какдела?"


def test_analyze_text_28():
    assert analyze_text("ктоты", commands) == "ктоты?"


def test_analyze_text_29():
    assert analyze_text("привет бот", commands) == "привет"


def test_analyze_text_30():
    assert analyze_text("рандомно", commands) == "рандом"
