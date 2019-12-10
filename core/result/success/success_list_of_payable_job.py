from core.messages.keys import Keys
from core.result import Result


class SuccessListOfPayableJob(Result):
    def dictionary_creator(self):
        jobs = []

        job = []
        # res = set()
        for list_item in self.params:
            dic = {}
            car_p = []
            dic['job_id'] = list_item.Job.id
            dic['price'] = str(list_item.Job.price)
            dic['start_schedule'] = list_item.Job.start_schedule
            dic['plate_number'] = list_item.Car.plate_number
            dic['business_owner_name'] = list_item.User.name
            dic['auto_type'] = list_item.Car.cars_list.name
            for items in list_item.Job.car_problems:
                # dic['service_category'] = items.services_definition.service_category
                # dic['service_grade'] = items.services_definition.service_grade
                # dic['service_type'] = items.services_definition.service_type
                # job.append(dic)

                car_problems = {}

                car_problems['service_category'] = items.services_definition.service_category
                car_problems['service_grade'] = items.services_definition.service_grade
                car_problems['service_type'] = items.services_definition.service_type.name

                car_p.append(car_problems)
            dic['car_problem'] = car_p

            jobs.append(dic)

            # items = set()
            # for result in jobs:
            #     items.add(result)
            # print jobs

        return {Keys.STATUS: 200, Keys.MESSAGE: Result.language.SUCCESS_LIST, Keys.PARAMS: jobs}
