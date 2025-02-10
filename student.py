import csv

class Student:
    all_students = dict()  # Use id as key 

    def __init__(self, student_id: str, student_name: str, student_class: str, student_email: str):
        self.student_id = student_id
        self.student_name = student_name
        self.student_email = student_email
        self.student_class = student_class
        Student.all_students[student_id] = self

    @classmethod
    def instantiate_from_csv(cls, csv_file):
        with open(csv_file, 'r') as students_csv:
            reader = csv.DictReader(students_csv)
            students_list: list = list(reader)
            try:
                field_names = [field for field in students_list[0]]
                for student in students_list:
                    Student(student_id=student[field_names[0]],
                            student_name=student[field_names[1]], 
                            student_class=student[field_names[2]],
                            student_email=student[field_names[3]])
            except IndexError:
                print("There is no record")

    def __repr__(self):
        return f"Student(id: {self.student_id}, name: {self.student_name}, email: {self.student_email}, class: {self.student_class})"

def main() -> None:
    Student.instantiate_from_csv("students.csv")
    for student in Student.all_students.values():
        print(student)

if __name__ == '__main__':
    main()
