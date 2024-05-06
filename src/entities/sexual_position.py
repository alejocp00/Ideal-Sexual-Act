class SexualPosition:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {"name": self.name}

    @staticmethod
    def from_dict(data):
        return SexualPosition(data["name"])
