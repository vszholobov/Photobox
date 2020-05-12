import pytest
from flask_server.server_functions import tags


def test_tags_1():
    assert tags("#Тег первый #Тег второй") == ["#Тег_первый", "#Тег_второй"]


def test_tags_2():
    assert tags("#Тег первый") == ['#Тег_первый']


def test_tags_3():
    assert tags("#Тег второй #Тег первый") == ["#Тег_второй", "#Тег_первый"] 


def test_tags_4():
    assert tags("#Тег____первый") == ["#Тег_первый"]    


def test_tags_5():
    assert tags("Тег первый") == []


def test_tags_6():
    assert tags("##Тег первый") != ["#Тег_первый"]    


def test_tags_7():
    assert tags("# #Тег первый") != ["#Тег_первый"]    


def test_tags_8():
    assert tags("#Тег первый") != ["#Тег_второй"]    


def test_tags_9():
    assert tags("#Тег первый") == ["#Тег_первый"]    


def test_tags_10():
    assert tags("##Тег первый") == [] 


def test_tags_11():
    assert tags("#Тег первый") != 1


def test_tags_12():
    assert tags("#Тег_первый") == ["#Тег_первый"]


def test_tags_13():
    assert tags("#Тег первый") != ["#Тег первый"]


def test_tags_14():
    assert tags("Тегпервый") == []


def test_tags_15():
    assert tags("#Тег____второй #Тег____третий #Тег____первый") == ["#Тег_второй", "#Тег_третий", "#Тег_первый"]


def test_tags_16():
     assert tags("# #Тег_первый") == []


def test_tags_17():
    assert tags("##Тег____второй # #Тег____третий ##Тег____первый") == []


def test_tags_18():
     assert tags("#Тег_первый") == tags("#Тег__первый") == tags("#Тег___первый")


def test_tags_19():
    assert tags("#Тег_первый" "#Тег_второй" "#Тег_третий") == ["#Тег_первый", "#Тег_второй", "#Тег_третий"]


def test_tags_20():
    assert tags("##Тег__первый") == tags("# #Тег___первый") == []


def test_tags_21():
    assert tags("##Тег__первый") == tags("# #Тег_второй") == []


def test_tags_22():
    assert tags("Тег____второй Тег____третий Тег____первый") == []


def test_tags_23():
    assert tags("#Тегпервый") == ['#Тегпервый']


def test_tags_24():
    assert tags("##Тег__первый") == tags("Тег____второй") == []


def test_tags_25():
    assert tags("#__Тегпервый") == ['#_Тегпервый']


def test_tags_26():
    assert tags("1#Тег первый") == ['#Тег_первы']


def test_tags_27():
    assert tags("#Тег первый""Тег второй") == ['#Тег_первыйТег_второй']


def test_tags_28():
    assert tags("Тег второй""#Тег первый") == ['#'] 


def test_tags_29():
    assert tags("#") == []


def test_tags_30():
    assert tags("#Тег 'Тег второй' первый") == ["#Тег_'Тег_второй'_первый"]

