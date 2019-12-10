from zeep import Client


class Kandu:
    _send_client = None
    _username = 'mkhalidji'
    _password = 'KIAsms@1'
    _sender = '100013570606'


    @staticmethod
    def initialize_client():
        Kandu._send_client = Client('http://api.payamak-panel.com/post/Send.asmx?wsdl')


    @staticmethod
    def send_sms(receiver, message):
        Kandu.initialize_client()
        return Kandu._send_client.service.SendSimpleSMS2(Kandu._username, Kandu._password, receiver, Kandu._sender, message,
                                                         False)
