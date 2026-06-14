"""Student Grade Calculator

This program loads student records from student_grades.txt, allows adding new
records, calculates averages and letter grades automatically, displays a
formatted student table, shows class statistics, searches by name, and saves
records back to the file.
"""

from dataclasses import dataclass
from typing import List, Optional

DATA_FILE = "student_grades.txt"

@dataclass
class Student:
    name: str
    id: str
    test1: float
    test2: float
    test3: float
    average: float
    grade: str


def calculate_average(test1: float, test2: float, test3: float) -> float:
    return round((test1 + test2 + test3) / 3.0, 2)


def calculate_grade(average: float) -> str:
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def load_students(filename: str) -> List[Student]:
    students: List[Student] = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                parts = line.strip().split("|")
                if len(parts) != 7:
                    print(f"Skipping malformed line: {line.strip()}")
                    continue
                name, student_id, test1, test2, test3, average, grade = parts
                try:
                    student = Student(
                        name=name,
                        id=student_id,
                        test1=float(test1),
                        test2=float(test2),
                        test3=float(test3),
                        average=float(average),
                        grade=grade,
                    )
                except ValueError:
                    print(f"Skipping invalid record values: {line.strip()}")
                    continue
                students.append(student)
    except FileNotFoundError:
        print(f"No existing data found. Starting with an empty record list.")
    except OSError as error:
        print(f"Error reading {filename}: {error}")
    return students


def save_students(filename: str, students: List[Student]) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    f"{student.name}|{student.id}|{student.test1:.2f}|"
                    f"{student.test2:.2f}|{student.test3:.2f}|{student.average:.2f}|{student.grade}\n"
                )
    except OSError as error:
        print(f"Error saving records to {filename}: {error}")


def prompt_string(prompt: str) -> Optional[str]:
    value = input(prompt).strip()
    if value.upper() == "ESC":
        return None
    return value


def prompt_score(prompt: str) -> Optional[float]:
    while True:
        raw = input(prompt).strip()
        if raw.upper() == "ESC":
            return None
        try:
            score = float(raw)
            if score < 0 or score > 100:
                print("Please enter a score between 0 and 100.")
                continue
            return score
        except ValueError:
            print("Invalid score. Enter a numeric value like 87.50 or type ESC to cancel.")


def add_student(students: List[Student]) -> None:
    print("\nAdd New Student Record (type ESC anytime to return to the menu)")
    name = prompt_string("Student name: ")
    if name is None:
        return
    student_id = prompt_string("Student ID: ")
    if student_id is None:
        return
    test1 = prompt_score("Test 1 score: ")
    if test1 is None:
        return
    test2 = prompt_score("Test 2 score: ")
    if test2 is None:
        return
    test3 = prompt_score("Test 3 score: ")
    if test3 is None:
        return

    average = calculate_average(test1, test2, test3)
    grade = calculate_grade(average)

    student = Student(
        name=name,
        id=student_id,
        test1=test1,
        test2=test2,
        test3=test3,
        average=average,
        grade=grade,
    )
    students.append(student)
    save_students(DATA_FILE, students)
    print(f"Added {name} with average {average:.2f} and grade {grade}.")


def display_students(students: List[Student]) -> None:
    if not students:
        print("\nNo students to display.")
        return

    print("\nAll Students")
    print("=" * 90)
    print(
        f"{'Name':<20} {'ID':<12} {'Test 1':>7} {'Test 2':>7} {'Test 3':>7} "
        f"{'Average':>9} {'Grade':>6}"
    )
    print("-" * 90)
    for student in students:
        print(
            f"{student.name:<20} {student.id:<12} {student.test1:7.2f} "
            f"{student.test2:7.2f} {student.test3:7.2f} {student.average:9.2f} "
            f"{student.grade:>6}"
        )
    print("=" * 90)


def display_statistics(students: List[Student]) -> None:
    if not students:
        print("\nNo student records available for statistics.")
        return

    averages = [student.average for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = round(sum(averages) / len(averages), 2)

    highest_student = max(students, key=lambda s: s.average)
    lowest_student = min(students, key=lambda s: s.average)

    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for student in students:
        grade_counts[student.grade] = grade_counts.get(student.grade, 0) + 1

    print("\nClass Statistics")
    print("=" * 40)
    print(f"Class average    : {class_average:.2f}")
    print(f"Highest average : {highest:.2f} ({highest_student.name})")
    print(f"Lowest average  : {lowest:.2f} ({lowest_student.name})")
    print("\nGrade Distribution:")
    for grade in ["A", "B", "C", "D", "F"]:
        print(f"  {grade}: {grade_counts[grade]} student(s)")
    print("=" * 40)


def search_student(students: List[Student]) -> None:
    if not students:
        print("\nNo student records available to search.")
        return

    query = prompt_string("Enter student name to search: ")
    if query is None:
        return

    query_lower = query.lower()
    matches = [student for student in students if query_lower in student.name.lower()]

    if not matches:
        print(f"No students found matching '{query}'.")
        return

    print(f"\nSearch results for '{query}':")
    print("=" * 90)
    for student in matches:
        print(
            f"{student.name:<20} {student.id:<12} {student.test1:7.2f} "
            f"{student.test2:7.2f} {student.test3:7.2f} {student.average:9.2f} "
            f"{student.grade:>6}"
        )
    print("=" * 90)


def main() -> None:
    students = load_students(DATA_FILE)

    print("STUDENT GRADE CALCULATOR")
    print("=" * 40)
    print("Type ESC at any prompt to exit.")

    while True:
        print("\nMain Menu")
        print("1. Add new student record")
        print("2. Display all students")
        print("3. Show class statistics")
        print("4. Search student by name")
        print("5. Save and exit")
        print("ESC. Exit program")

        choice = input("Select an option (1-5) or press ESC to exit: ").strip()
        if choice.upper() == "ESC":
            break

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            display_statistics(students)
        elif choice == "4":
            search_student(students)
        elif choice == "5":
            save_students(DATA_FILE, students)
            print("Saving records...")
            print(f"✓ Saved {len(students)} student record(s) to file.")
            print("Thank you for using Student Grade Calculator!")
            return
        else:
            print("Invalid selection. Please enter 1-5 or ESC.")

    save_students(DATA_FILE, students)
    print("\nSaving records...")
    print(f"✓ Saved {len(students)} student record(s) to file.")
    print("Thank you for using Student Grade Calculator!")


if __name__ == "__main__":
    main()
1