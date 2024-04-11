import os
import random
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backup_file_path = os.path.join(current_dir, 'backup.txt')
write_file_path = os.path.join(current_dir, 'file.txt')


class Student:
    def __init__(self, student_id, name, answers):
        self.id = student_id
        self.name = name
        self.answers = answers

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_answers(self):
        return self.answers

    def set_answers(self, answers):
        self.answers = answers


def create_the_list():
    try:
        with open(backup_file_path, 'r') as reader:
            txt = reader.readlines()
    except FileNotFoundError:
        return "Backup file not found."
    with open(write_file_path, 'w') as writer:
        for j, line in enumerate(txt, 1):
            writer.write(f"{j} {line}")
    return "List has been rewritten."


def pick_students(students, n):
    set()
    min_answers = min([student.get_answers() for student in students])
    students_left = [student for student in students if student.get_answers() == min_answers]
    students_removed = [student for student in students if student.get_answers() == min_answers + 1]

    size_of_left = len(students_left)
    if size_of_left == n:
        names = set([student.get_name() for student in students_left])
    elif size_of_left > n:
        random.shuffle(students_left)
        names = set([student.get_name() for student in students_left[:n]])
    else:
        n -= size_of_left
        random.shuffle(students_removed)
        names = set([student.get_name() for student in students_removed[:n]])
        names.update([student.get_name() for student in students_left])

    return names


def main():
    global FILEPATH
    try:
        if len(sys.argv) > 1:
            FILEPATH = sys.argv[1]
    except IndexError:
        pass

    students = []  # Create a list to store student objects

    is_reseted = ""
    ask1 = input("Do you want to reset the list of students?\n\tY/N: ")
    if ask1.lower() == "y":
        ask2 = input("Are you sure? ")
        if ask2.lower() == "y":
            is_reseted = create_the_list()  # Reset the list if confirmed by the user

    with open(write_file_path, 'r') as file:
        # Read student data from the file and create Student objects
        for line in file:
            temp = line.split(" ")
            students.append(Student(int(temp[0]), temp[1], int(temp[2])))

    # Prompt the user to input the number of students to select
    while True:
        try:
            n = int(input(is_reseted + "\nInput how many students will answer today: "))
            if 0 < n <= len(students):
                break
            elif n == 0:
                sys.exit(0)
        except ValueError:
            pass

    while True:
        result_set = pick_students(students, n)  # Pick students randomly
        while True:
            result = input(str(result_set) + "\nAre You Satisfied with result?\n\tY(yes)/N(no)/Q(quit): ")
            if result.lower() in ["y", "n", "q"]:
                break
        if result.lower() == "q":
            sys.exit(0)  # Exit the program if user wants to quit
        if result.lower() == "y":
            break  # Repeat until user is satisfied

    # Update the number of times each student has been selected
    for student in students:
        if student.get_name() in result_set:
            student.set_answers(student.get_answers() + 1)

    students.sort(key=lambda x: x.get_id())  # Sort the students by ID

    with open(write_file_path, 'w') as file:
        # Write the updated student data back to the file
        for i, student in enumerate(students, 1):
            file.write(f"{i} {student.get_name()} {student.get_answers()}\n")


if __name__ == "__main__":
    main()
