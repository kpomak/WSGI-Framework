from threading import local


class Session:
    current = local()

    def __init__(self):
        self.created_instanses = []
        self.updated_instanses = []
        self.deleted_instanses = []

    def register_model(self, registry):
        self.registry = registry

    def add_created(self, instanse):
        self.created_instanses.append(instanse)

    def add_updated(self, instanse):
        self.updated_instanses.append(instanse)

    def add_deleted(self, instanse):
        self.deleted_instanses.append(instanse)

    def commit(self):
        self.insert()
        self.update()
        self.delete()

        self.created_instanses.clear()
        self.updated_instanses.clear()
        self.deleted_instanses.clear()

    def insert(self):
        for instanse in self.created_instanses:
            self.registry.get_mapper(instanse).insert(instanse)

    def update(self):
        for instanse in self.updated_instanses:
            self.registry.get_mapper(instanse).update(instanse)

    def delete(self):
        for instanse in self.deleted_instanses:
            self.registry.get_mapper(instanse).delete(instanse)

    @classmethod
    def new_current(cls):
        cls.current.session = Session()

    @classmethod
    def get_current(cls):
        return cls.current.session


class Objects:
    def create(self):
        Session.get_current().add_created(self)

    def update(self):
        Session.get_current().add_updated(self)

    def delete(self):
        Session.get_current().add_deleted(self)
