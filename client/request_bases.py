from abc import ABCMeta


class JSONRequest:
    __metaclass__ = ABCMeta
    json = None

    def __init__(self):
        pass


class RequestBase:
    method = None
    __metaclass__ = ABCMeta

    def __init__(self):
        pass


class HttpRequest(RequestBase, JSONRequest):
    json = {}
    method = ""
    is_json = False

    def __init__(self):
        super(HttpRequest, self).__init__()
