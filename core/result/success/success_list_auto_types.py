from core.messages.keys import Keys
from core.result import Result


class SuccessListAutoTypes(Result):
    def dictionary_creator(self):
        params = []
        for param in self.params:
            dct = {'label': param.name, 'id': param.id}
            models = []
            for model in param.auto_models:
                model_dct= {'id': model.id, 'label': model.name}
                models.append(model_dct)
            dct['models'] = models
            params.append(dct)
        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.SUCCESS_LIST, Keys.PARAMS: params}
