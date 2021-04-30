from .mixins import OctiiObject

class CommunityBase(OctiiObject):
    @classmethod
    def load_json(cls: type, data: any):
        instance = cls(data['id'])
        instance.icon = data['community']['icon']
        instance.large = data['community']['large']
        instance.owner_id = data['community']['owner_id']
        instance.name = data['community']['name']
        return instance

    def __str__(self):
        return "<octii.CommunityBase {} icon={!r} large={!r} owner_id={!r} name={!r}>".format(self.id, self.icon, self.large, self.owner_id, self.name)

    def __repr__(self):
        return "<octii.CommunityBase {} icon={!r} large={!r} owner_id={!r} name={!r}>".format(self.id, self.icon, self.large, self.owner_id, self.name)

class Community(CommunityBase):
    @classmethod
    def load_json(cls: type, data: any):
        instance = cls(data['id'])
        instance.icon = data['icon']
        instance.large = data['large']
        instance.owner_id = data['owner_id']
        instance.system_channel_id = data['system_channel_id']
        instance.name = data['name']
        instance.base_permissions = data['base_permissions']
        instance.channel_ids = data['channels']
        instance.is_organization = data['organization']
        return instance