from db import *


def main_menu():
    print("Привет! Это приложение журнал")
    menu_message = """Выберите команду:
    1 - Работа с учениками
    2 - Работа с оценками
    3 - Работа с предметами"""
    student_message = """Выберите команду:
    1 - Список учеников
    2 - Добавить ученика
    3 - Удалить ученика"""
    marks_message = """Выберите команду:
    1 - Посмотреть оценки ученика по всем предметам
    2 - Посмотреть оценки ученика по определенному предмету
    3 - Посмотреть оценки всех учеников по определенному предмету
    4 - Выставить оценку ученику по определенному предмету"""
    subject_message = """Выберите команду:
    1 - Список предметов
    2 - Добавить предмет
    3 - Удалить предмет"""

    print(menu_message)
    command = input()
    if command.isdigit():
        if int(command) == 1:
            print("Работа с учениками")
            print(student_message)
            students_menu()
        elif int(command) == 2:
            print("Работа с оценками")
            print(marks_message)
            marks_menu()
        elif int(command) == 3:
            print("Работа с предметами")
            print(subject_message)
            subject_menu()
        else:
            print("Команда не распознана")
            main_menu()
    else:
        print("Введите команду одним числом")
        main_menu()


# Меню работы с учениками
def students_menu():
    command = input()
    if command.isdigit():
        if int(command) == 1:
            for student_id, student_name in students_list():
                print(student_id, "-", student_name)
            main_menu()
        elif int(command) == 2:
            print("Введите имя ученика: ")
            new_student()
        elif int(command) == 3:
            print("Введите id ученика, которого вы хотите удалить")
            delete_student()
        else:
            print("Команда не распознана")
            main_menu()
    else:
        print("Введите команду одним числом")
        main_menu()


def new_student():
    name = input()
    age = input("Введите возраст ученика: ")
    if age.isdigit():
        grade = input("Введите класс ученика: ")
        db_make_student(name, int(age), grade)
        print("Вы успешно добавили ученика")
    else:
        print("Влзраст должен быть числом")
    main_menu()


def delete_student():
    student_id = input()
    if student_id.isdigit():
        status = db_delete_student(int(student_id))
        if status == 0:
            print("Ученик под данным id не найден")
        else:
            print("Ученик успешно удален")
    else:
        print("id должен содержать только цифры")
    main_menu()


# Меню работы с оценками
def marks_menu():
    command = input()
    if command.isdigit():
        if int(command) == 1:
            print("Введите id ученика, оценки которого вы хотите узнать: ")
            student_mark()
        elif int(command) == 2:
            print("Введите id ученика, оценки которого вы хотите узнать: ")
            student_mark_subject()
        elif int(command) == 3:
            print("Введите название предмета: ")
            subject_mark()
        elif int(command) == 4:
            print("Введите id ученика, которому хотите выставить оценку")
            new_mark()
        else:
            print("Команда не распознана")
            main_menu()
    else:
        print("Введите команду одним числом")
        main_menu()


def student_mark():
    student_id = input()
    if student_id.isdigit():
        grouped_marks, status = db_get_student_marks(int(student_id))
        if status == 0:
            print("Ученик под данным id не найден")
        else:
            for subject, marks in grouped_marks:
                print(subject+":", *marks)
    else:
        print("id должен содержать только цифры")
    main_menu()


def student_mark_subject():
    student_id = input()
    if student_id.isdigit():
        subject = input("Введите название предмета:")
        marks, status = db_get_student_mark_by_subject(int(student_id), subject)
        if status == 0:
            print("Ученик под данным id не найден")
        elif status == 2:
            print("Предмет не найден")
        else:
            print(subject + ":", *marks)
    else:
        print("id должен содержать только цифры")
    main_menu()


def subject_mark():
    subject = input()
    grouped_marks, status = db_get_subject_marks(subject)
    if status == 0:
        print("Предмет не найден")
    else:
        for subject, marks in grouped_marks:
            print(subject, *marks)
    main_menu()


def new_mark():
    student_id = input()
    if student_id.isdigit():
        subject = input("Введите название предмета: ")
        grade = input("Введите оценку: ")
        if grade.isdigit():
            if 5 >= int(grade) >= 1:
                status = db_new_mark(int(student_id), subject, int(grade))
                if status == 0:
                    print("Ученик под данным id не найден")
                elif status == 2:
                    print("Предмет не найден")
                else:
                    print("Оценка выставлена")
            else:
                print("Оценка должна быть от 1 до 5 включительно")
        else:
            print("Оценка должна быть числом")
    else:
        print("id должен содержать только цифры")
    main_menu()


# Меню работы с предметами
def subject_menu():
    command = input()
    if command.isdigit():
        if int(command) == 1:
            subject_lists()
        elif int(command) == 2:
            print("Введите название нового предмета: ")
            new_subject()
        elif int(command) == 3:
            print("Введите название предмета: ")
            delete_subject()
        else:
            print("Команда не распознана")
            main_menu()
    else:
        print("Введите команду одним числом")
        main_menu()


def subject_lists():
    subjects = db_subject_list()
    print(*subjects)
    main_menu()


def new_subject():
    name = input()
    status = db_add_subject(name)
    if status == 0:
        print("Такой предмет уже существует")
    else:
        print("Предмет успешно добавлен")
    main_menu()


def delete_subject():
    name = input()
    status = db_delete_subject(name)
    if status == 0:
        print("Такой предмет не найден")
    else:
        print("Предмет успешно удален")
    main_menu()


if __name__ == "__main__":
    main_menu()
