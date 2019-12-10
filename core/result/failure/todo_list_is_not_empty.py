from core.messages.keys import Keys
from core.result import Result


class TodoListNotEmpty(Result):
    def dictionary_creator(self):

        return {Keys.STATUS: self.status, Keys.MESSAGE: Result.language.TODO_LIST_IS_NOT_EMPTY, Keys.PARAMS: None}