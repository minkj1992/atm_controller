from src import main


def test_hello():
    assert main.say_hello() == "Hello World"
