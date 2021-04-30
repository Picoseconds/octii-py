from .mixins import OctiiObject

class Message(OctiiObject):
    @classmethod
    def load_json(cls: type, data: any):
        instance = cls(data['id'])
        instance.author_id = data['author']['id'] if 'author' in data else data['author_id']
        instance.created_at = data['created_at']
        instance.updated_at = data['updated_at']
        instance.message_type = data['type'] if 'type' in data else 1
        instance.content = data['content']
        return instance

    def __str__(self):
        return "Message: " + self.content

    def __repr__(self):
        return "<octii.Message {}>".format(self.id)