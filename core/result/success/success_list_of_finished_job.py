from core.messages.keys import Keys
from core.result import Result


class SuccessListOfFinishedJob(Result):
    def dictionary_creator(self):
        params = []
        for index in range(len(self.params)):
            param = self.params[index]
            dct = {
                Keys.BUSINESS_OWNER_NAME: param.BusinessOwner.name,
                Keys.JOB_ID: param.Job.id,
                Keys.BUSINESS_OWNER_IMAGE: param.BusinessOwner.uuid + "/profile-pic",
                Keys.TYPE_OF_SERVICE: param.Job.type,
                Keys.WORK_SPACE_NAME: param.BusinessOwner.workspace_name
            }
            questions = []
            key_question = None

            for question in param.Job.question_sets.question_to_question_set:
                if question.is_key:
                    key_question = question.question.question
                else:
                    questions.append(question.question.question)
            dct[Keys.POLL_QUESTIONS] = questions
            dct[Keys.KEY_QUESTION] = key_question
            params.append(dct)

        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.SUCCESS_LIST, Keys.PARAMS: params}
