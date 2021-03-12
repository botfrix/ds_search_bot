from json import JSONEncoder
import datetime


class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return {'tag': obj.tag, 'user': obj.user, 'command_text': obj.command_text,
                    'date': obj.date.strftime('%d.%m.%y')}


class Message(MyEncoder):

    def __init__(self, tag, user, command_text):
        super().__init__()
        self.tag = tag
        self.user = user.display_name
        self.date = datetime.datetime.now()
        self.command_text = command_text
