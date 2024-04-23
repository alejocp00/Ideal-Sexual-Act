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

    def remove_sexual_position(self, name):
        self._sexual_positions.pop(name)

    def get_pleasure_of_position(self, name):
        return self._sexual_positions[name]["pleasure"]

    def get_hardness_of_position(self, name):
        return self._sexual_positions[name]["hardness"]
