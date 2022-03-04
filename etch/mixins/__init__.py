from etch.api import Mixin

class ListMixin(list, metaclass=Mixin):
    def intify(self):
        return [int(i) for i in self]