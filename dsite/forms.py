class Field:
    def __init__(self, label=""):
        self.label = label


class TextField(Field):
    pass


class Form:
    def __init__(self):
        self.data = {}

    def is_valid(self):
        return True
