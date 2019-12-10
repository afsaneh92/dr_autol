from core.messages.keys import Keys
from core.result import Result


class SuccessLogin(Result):
    def dictionary_creator(self):
        return {Keys.STATUS: self.status, Keys.MESSAGE: self.message, "param": "yes of course",
                "params": {"name": self.params["name"], "id": self.params["id"]}}
