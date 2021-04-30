from .mixins import OctiiObject

class User(OctiiObject):
    @classmethod
    def load_json(cls: type, data: any):
        instance = cls(data['id'])
        instance.is_disabled = data['disabled']
        instance.is_developer = data['developer']
        instance.state = data['state']
        instance.username = data['username']
        instance.email = data['email']
        instance.color = data['color']
        instance.avatar = data['avatar']
        instance.discriminator = data['discriminator']
        return instance

    def get_mention(self):
        return "<@" + self.id + ">"

    def __str__(self):
        return "<octii.User {}#{} (id {})>".format(self.username, str(self.discriminator).zfill(4), self.id)

    def __repr__(self):
        return "<octii.User {}#{} (id {})>".format(self.username, str(self.discriminator).zfill(4), self.id)