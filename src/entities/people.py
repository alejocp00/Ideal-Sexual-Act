class People:
    def __init__(self, name):
        self._name = name
        self._sexual_positions = {}
        self.initial_energy = 100
        self.initial_pleasure = 0
        self.current_energy = 100
        self.current_pleasure = 0
        self.orgasm_pleasure = 100

    @property
    def name(self):
        return self._name

    def add_sexual_position(self, name, pleasure, hardness):
        self._sexual_positions[name] = {"pleasure": pleasure, "hardness": hardness}

    def add_sexual_positions(self, positions):
        for position in positions:
            self.add_sexual_position(
                position,
                positions[position]["pleasure"],
                positions[position]["hardness"],
            )

    def remove_sexual_position(self, name):
        self._sexual_positions.pop(name)

    def get_pleasure_of_position(self, name):
        return self._sexual_positions[name]["pleasure"]

    def get_hardness_of_position(self, name):
        return self._sexual_positions[name]["hardness"]

    def to_dict(self):
        return {
            "name": self.name,
            "sexual_positions": self._sexual_positions,
            "initial_energy": self.initial_energy,
            "initial_pleasure": self.initial_pleasure,
            "current_energy": self.current_energy,
            "current_pleasure": self.current_pleasure,
            "orgasm_pleasure": self.orgasm_pleasure,
        }

    @staticmethod
    def from_dict(data):
        people = People(data["name"])
        people.add_sexual_positions(data["sexual_positions"])
        people.initial_energy = data["initial_energy"]
        people.initial_pleasure = data["initial_pleasure"]
        people.current_energy = data["current_energy"]
        people.current_pleasure = data["current_pleasure"]
        people.orgasm_pleasure = data["orgasm_pleasure"]
        return people
