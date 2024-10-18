import logging
from app.commands import Command

class GreetCommand(Command):
    def execute(self):
        logging.info("GreetCommand executed: Hello, World!")
        print("Hello, World!")