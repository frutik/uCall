from crm.adapters.abstract_adapter import AbstractAdapter

class SimpleCrmAdapter(AbstractAdapter):

    def __init__(self, params):
	pass

    def findUserByPhone(self, phone_number):

        result = {'firstname': 'test', 'lastname': 'test', 'title': 'test'}

        return result
