class ObjectList(list):

    def __getattr__(self, item):
        if eval(f"callable(self[0].{item})"):
            # item being grabbed is a method
            return lambda *a, **kw: [getattr(element, item)(*a, **kw) for element in self]
        return [getattr(element, item) for element in self]
