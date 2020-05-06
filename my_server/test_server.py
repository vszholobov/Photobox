import os, sys, inspect, pytest
from flask_server.server_functions import tags

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
src_path = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_path)


def test_tags_1():
    assert tags("#Тег первый #Тег второй") == ["#Тег_первый", "#Тег_второй"]

