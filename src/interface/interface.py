import os
from typing import List
from src.entities.sexual_position import SexualPosition
from src.entities.people import People
from src.problems.abstract_problem import AbstractProblem, ProblemsTypes
from src.problems.implementations.max_min_pleasure import MaxMinPleasure
from src.problems.implementations.max_time import MaxTime
from json import dumps, loads


# This will be a console interface for a Lineal Programming problem
# The problem is about find the best sexual act for a group of people
# The interface need to manage:
# - Creation of a sexual position
# - Delete a sexual position
# - Edit a sexual position
# - List all sexual positions
# - Creation of a people
# - When a people is created, need to specify how pleasure he can get from each sexual position, and how hard is to do each sexual position
# - Delete a people
# - Edit a people
# - List all people
# - List all people and their pleasure and hardness for each sexual position
# - Select a problem to solve
# - Show the solution of the problem
class Options:
    CANCEL_KEY = "c"
    SELECT_OPTION = "Select an option"
    CREATE_SEXUAL_POSITION = "Create a sexual position"
    DELETE_SEXUAL_POSITION = "Delete a sexual position"
    EDIT_SEXUAL_POSITION = "Edit a sexual position"
    LIST_SEXUAL_POSITIONS = "List all sexual positions"
    CREATE_PEOPLE_NAME = "Create a people"
    CREATE_PEOPLE_PLEASURE = "6"
    CREATE_PEOPLE_ORGASM_PLEASURE = "7"
    CREATE_PEOPLE_HARDNESS = "8"
    CREATE_PEOPLE_INITIAL_ENERGY = "9"
    CREATE_PEOPLE_INITIAL_PLEASURE = "10"
    DELETE_PEOPLE = "Delete a people"
    EDIT_PEOPLE = "Edit a people"
    LIST_PEOPLE = "List all people"
    LIST_PEOPLE_AND_POSITIONS = (
        "List all people and their pleasure and hardness for each sexual position"
    )
    SELECT_PROBLEM = "Choose a problem to solve"
    EXPORT_DATA = "Export people and positions to a file"
    LOAD_DATA = "Load people and positions from a file"
    FILE_NAME = "data.json"


class Interface:

    def __init__(self):
        self.__sexual_positions: List[SexualPosition] = []
        self.__people: List[People] = []
        self.__problems: List[ProblemsTypes] = [
            ProblemsTypes.MAX_TIME,
            ProblemsTypes.MAX_MIN_PLEASURE,
            ProblemsTypes.MINIMIZE_MAX_TIRED,
            ProblemsTypes.MINIMIZE_INITIAL_ENERGY,
            ProblemsTypes.MAX_INITIAL_PLEASURE,
        ]
        self.options = {
            Options.CREATE_SEXUAL_POSITION: self.__create_sexual_position,
            Options.EDIT_SEXUAL_POSITION: self.__edit_sexual_position,
            Options.DELETE_SEXUAL_POSITION: self.__delete_sexual_position,
            Options.LIST_SEXUAL_POSITIONS: self.__List_sexual_positions,
            Options.CREATE_PEOPLE_NAME: self.__create_people,
            Options.EDIT_PEOPLE: self.__edit_people,
            Options.DELETE_PEOPLE: self.__delete_people,
            Options.LIST_PEOPLE: self.__List_people,
            Options.LIST_PEOPLE_AND_POSITIONS: self.__List_people_and_positions,
            Options.SELECT_PROBLEM: self.__select_problem,
            Options.EXPORT_DATA: self.__export_data,
            Options.LOAD_DATA: self.__load_data,
        }

    def _update_people_sexual_positions(self, new_position_name):
        for people in self.__people:
            pleasure = self._handle_input(
                f"Enter the pleasure of {people.name} for {new_position_name}: ",
                Options.CREATE_PEOPLE_PLEASURE,
            )
            hardness = self._handle_input(
                f"Enter the hardness of {people.name} for {new_position_name}: ",
                Options.CREATE_PEOPLE_HARDNESS,
            )
            if pleasure and hardness:
                pleasure = float(pleasure)
                hardness = float(hardness)
                people.add_sexual_position(new_position_name, pleasure, hardness)
            else:
                self.__sexual_positions.pop()
                break

    def __create_sexual_position(self):
        name = self._handle_input(
            "Enter the name of the sexual position: ", Options.CREATE_SEXUAL_POSITION
        )
        if name:
            self.__sexual_positions.append(SexualPosition(name))
            self._update_people_sexual_positions(name)

    def __delete_sexual_position(self):
        """Show all sexual positions and ask for the name of the sexual position to delete"""
        self.print_sexual_positions()
        index = self._handle_input(
            "Select the index of the sexual position to delete: ",
            Options.DELETE_SEXUAL_POSITION,
        )
        if index:
            index = int(index)
            deleted_sexual_position = self.__sexual_positions.pop(int(index))
            for people in self.__people:
                people.remove_sexual_position(deleted_sexual_position.name)

    def __edit_sexual_position(self):
        """Show all sexual positions and ask for the name of the sexual position to edit"""
        self.print_sexual_positions()
        index = self._handle_input(
            "Select the index of the sexual position to edit: ",
            Options.EDIT_SEXUAL_POSITION,
        )
        if index:
            index = int(index)
            old_name = self.__sexual_positions[index].name
            new_name = self._handle_input(
                f"Enter the new name for {old_name}: ", Options.EDIT_SEXUAL_POSITION
            )
            if new_name:
                self.__sexual_positions[index] = SexualPosition(new_name)

                for people in self.__people:
                    people.add_sexual_position(
                        new_name,
                        people.get_pleasure_of_position(old_name),
                        people.get_hardness_of_position(old_name),
                    )
                    people.remove_sexual_position(old_name)

    def __List_sexual_positions(self):
        """Print all sexual positions"""
        self.print_sexual_positions()
        input("Press any key to continue")

    def __create_people(self):
        name = self._handle_input(
            "Enter the name of the people: ", Options.CREATE_PEOPLE_NAME
        )
        if name:
            self.__people.append(People(name))
            for sexual_position in self.__sexual_positions:
                pleasure = self._handle_input(
                    f"Enter the pleasure of {name} for {sexual_position.name}: ",
                    Options.CREATE_PEOPLE_PLEASURE,
                )
                hardness = self._handle_input(
                    f"Enter the hardness of {name} for {sexual_position.name}: ",
                    Options.CREATE_PEOPLE_HARDNESS,
                )
                if pleasure and hardness:
                    pleasure = float(pleasure)
                    hardness = float(hardness)
                    self.__people[-1].add_sexual_position(
                        sexual_position.name, pleasure, hardness
                    )
                else:
                    self.__people.pop()
                    break

            if name in [people.name for people in self.__people]:
                orgasm_pleasure = self._handle_input(
                    f"Enter the orgasm pleasure of {name}: ",
                    Options.CREATE_PEOPLE_ORGASM_PLEASURE,
                )
                initial_energy = self._handle_input(
                    f"Enter the initial energy of {name}: ",
                    Options.CREATE_PEOPLE_INITIAL_ENERGY,
                )
                initial_pleasure = self._handle_input(
                    f"Enter the initial pleasure of {name}: ",
                    Options.CREATE_PEOPLE_INITIAL_PLEASURE,
                )
                if orgasm_pleasure and initial_energy and initial_pleasure:
                    orgasm_pleasure = float(orgasm_pleasure)
                    initial_energy = float(initial_energy)
                    initial_pleasure = float(initial_pleasure)

                    self.__people[-1].orgasm_pleasure = orgasm_pleasure
                    self.__people[-1].current_energy = initial_energy
                    self.__people[-1].current_pleasure = initial_pleasure
                    self.__people[-1].initial_energy = initial_energy
                    self.__people[-1].initial_pleasure = initial_pleasure
                else:
                    self.__people.pop(name)

    def __delete_people(self):
        """Show all people and ask for the name of the people to delete"""
        self.print_people()
        index = self._handle_input(
            "Enter the index of the people to delete: ", Options.DELETE_PEOPLE
        )
        if index:
            index = int(index)
            self.__people.pop(int(index))

    def __edit_people(self):
        """Show all people and ask for the name of the people to edit"""
        self.print_people()
        index = self._handle_input(
            "Enter the index of the people to edit: ", Options.EDIT_PEOPLE
        )
        if index:
            index = int(index)
            old_name = self.__people[index].name
            target_people = self.__people[index]
            new_name = self._handle_input(
                f"Enter the new name for {old_name}: ", Options.CREATE_PEOPLE_NAME
            )

            if new_name:
                self.__people[index] = People(new_name)
                for sexual_position in self.__sexual_positions:
                    pleasure = self._handle_input(
                        f"Enter the pleasure of {new_name} for {sexual_position.name}. The current value is {target_people.get_pleasure_of_position(sexual_position.name)}: ",
                        Options.CREATE_PEOPLE_PLEASURE,
                    )
                    hardness = self._handle_input(
                        f"Enter the hardness of {new_name} for {sexual_position.name}. The current value is {target_people.get_hardness_of_position(sexual_position.name)}: ",
                        Options.CREATE_PEOPLE_HARDNESS,
                    )
                    if pleasure and hardness:
                        pleasure = float(pleasure)
                        hardness = float(hardness)
                        self.__people[-1].add_sexual_position(
                            sexual_position.name, pleasure, hardness
                        )
                    else:
                        return

                orgasm_pleasure = self._handle_input(
                    f"Enter the orgasm pleasure of {new_name}. The current value is {target_people.orgasm_pleasure}: ",
                    Options.CREATE_PEOPLE_ORGASM_PLEASURE,
                )
                initial_energy = self._handle_input(
                    f"Enter the initial energy of {new_name}. The current value is {target_people.initial_energy}: ",
                    Options.CREATE_PEOPLE_INITIAL_ENERGY,
                )
                initial_pleasure = self._handle_input(
                    f"Enter the initial pleasure of {new_name}. The current value is {target_people.initial_pleasure}: ",
                    Options.CREATE_PEOPLE_INITIAL_PLEASURE,
                )
                if orgasm_pleasure and initial_energy and initial_pleasure:
                    orgasm_pleasure = float(orgasm_pleasure)
                    initial_energy = float(initial_energy)
                    initial_pleasure = float(initial_pleasure)
                    self.__people[-1].orgasm_pleasure = orgasm_pleasure
                    self.__people[-1].current_energy = initial_energy
                    self.__people[-1].current_pleasure = initial_pleasure
                    self.__people[-1].initial_energy = initial_energy
                    self.__people[-1].initial_pleasure = initial_pleasure

    def __List_people(self):
        """Print all people"""
        self.print_people()
        input("Press any key to continue")

    def _handle_input(self, text: str, option: Options):
        """Ask the user for an input and return it

        Args:
            text (str): Text to show to the user
            option (Options): Option to show to the user
        """

        entry = input(text)

        while not self._valid_input(entry, option):
            os.system("clear")
            print("Invalid input")
            entry = input(text)

        if entry.lower() == Options.CANCEL_KEY:
            return None

        return entry

    def _valid_input(self, entry: str, option: Options):
        """Check if the entry is valid

        Args:
            entry (str): Entry to check
            option (Options): Option to check

        Returns:
            bool: True if the entry is not valid, False otherwise
        """

        def is_float(entry):
            try:
                float(entry)
                return True
            except ValueError:
                return False

        def is_int(entry):
            try:
                int(entry)
                return True
            except ValueError:
                return False

        def in_range(entry, min_value, max_value):
            return min_value <= int(entry) <= max_value

        if entry.lower() == Options.CANCEL_KEY:
            return True

        if (
            option == Options.CREATE_SEXUAL_POSITION
            or option == Options.CREATE_PEOPLE_NAME
        ):
            return entry
        elif (
            option == Options.DELETE_SEXUAL_POSITION
            or option == Options.EDIT_SEXUAL_POSITION
        ):
            return is_int(entry) and in_range(
                entry, 0, len(self.__sexual_positions) - 1
            )
        elif (
            option == Options.CREATE_PEOPLE_PLEASURE
            or option == Options.CREATE_PEOPLE_ORGASM_PLEASURE
            or option == Options.CREATE_PEOPLE_HARDNESS
            or option == Options.CREATE_PEOPLE_INITIAL_ENERGY
            or option == Options.CREATE_PEOPLE_INITIAL_PLEASURE
        ):
            return is_float(entry) and in_range(float(entry), 0, 100)
        elif option == Options.DELETE_PEOPLE or option == Options.EDIT_PEOPLE:
            return is_int(entry) and in_range(int(entry), 0, len(self.__people) - 1)
        elif option == Options.SELECT_OPTION:
            return is_int(entry) and in_range(entry, 0, len(self.options) - 1)
        elif option == Options.SELECT_PROBLEM:
            return is_int(entry) and in_range(entry, 0, len(self.__problems) - 1)
        else:
            return False

    def print_sexual_positions(self):
        """Print all sexual positions"""
        for index, sexual_position in enumerate(self.__sexual_positions):
            print(f"{index}: {sexual_position.name}")

    def print_people(self):
        """Print all people"""
        for index, people in enumerate(self.__people):
            print(f"{index}: {people.name}")

    def __List_people_and_positions(self):
        """Print all people and their pleasure and hardness for each sexual position"""
        for people in self.__people:
            print(f"{people.name}:")
            for sexual_position in self.__sexual_positions:
                print(
                    f"    {sexual_position.name}: Pleasure: {people.get_pleasure_of_position(sexual_position.name)}, Hardness: {people.get_hardness_of_position(sexual_position.name)}"
                )
        input("Press any key to continue")

    def __select_problem(self):
        """Select a problem to solve"""
        if not self.__people or not self.__sexual_positions:
            print("You need to create at least one people and one sexual position")
            input("Press any key to continue")
            return

        print("Select a problem to solve:")
        for index, problem in enumerate(self.__problems):
            print(f"{index}: {problem}")

        index = self._handle_input(
            "Select a problem to solve: ", Options.SELECT_PROBLEM
        )

        if index:
            if index.lower() == Options.CANCEL_KEY:
                return
            index = int(index)

            problem = self.__get_problem(index)
            solution = problem.solve()
            print(solution)
            input("Press any key to continue")

    def __get_problem(self, index):
        if self.__problems[index] == ProblemsTypes.MAX_TIME:
            return MaxTime(self.__people, self.__sexual_positions)
        if self.__problems[index] == ProblemsTypes.MAX_MIN_PLEASURE:
            return MaxMinPleasure(self.__people, self.__sexual_positions)
        raise NotImplementedError("The problem is not implemented yet")
        # Todo: poner los problemas restantes

    def run(self):
        """Main function to run the interface"""

        while True:
            os.system("clear")
            print("Options:")
            for index, option in enumerate(self.options):
                print(f"{index}: {option}")

            entry = self._handle_input("Select an option: ", Options.SELECT_OPTION)

            if entry:
                os.system("clear")
                self.options[List(self.options.keys())[int(entry)]]()
            else:
                break

        print("Goodbye!")

    def __export_data(self):
        """Export people and positions to a file"""
        data = {
            "people": [people.to_dict() for people in self.__people],
            "positions": [position.to_dict() for position in self.__sexual_positions],
        }
        with open(Options.FILE_NAME, "w") as file:
            file.write(dumps(data))

        print("Data exported successfully")
        input("Press any key to continue")

    def __load_data(self):
        """Load people and positions from a file"""
        try:
            with open(Options.FILE_NAME, "r") as file:
                data = loads(file.read())
                self.__people = [People.from_dict(people) for people in data["people"]]
                self.__sexual_positions = [
                    SexualPosition.from_dict(position) for position in data["positions"]
                ]
                print("Data loaded successfully")
                input("Press any key to continue")
        except FileNotFoundError:
            print("The file does not exist")
            input("Press any key to continue")
        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press any key to continue")
