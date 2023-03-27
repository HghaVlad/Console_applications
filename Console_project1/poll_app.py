import pymysql
import datetime

user_login = 1

connection = pymysql.connect(host="localhost", user="root", password="root", database="poll_app")
cursor = connection.cursor()


# Главное меню
def main_menu():
    if user_login is None:
        print("Вы еще не авторизованы, для прохождения опроса необходимо авторизоваться или зарегистрироваться")
        print("Нажмите 1 для регистрации\nНажмите 2 для авторизации")
    print("""Нажмите 3 для просмотра доступных опросов
Нажмите 4 для прохождения опроса""")
    result = input()
    try:
        if (int(result) == 1 or int(result) == 2) and user_login is not None:
            print("Вы уже авторизованы")
        elif int(result) == 1:
            register_user()
        elif int(result) == 2:
            login_user()
        elif int(result) == 3:
            polls_list()
        elif int(result) == 4:
            select_poll()
        else:
            main_menu()
    except ValueError:
        print("Введите число")
        main_menu()
    except Exception as e:
        print(e)
        print("Неизвестная ошибка")


# Регистрация пользователя
def register_user():
    name = input("Введите имя: ")
    age = input("Введите возраст: ")
    login = input("Введите логин: ")
    if len(name) < 4:
        print("Имя должно состоять минимум из 4 символов")
        main_menu()
    elif age.isdigit() is False:
        print("Возраст должен быть целым числом")
        main_menu()
    elif len(login) < 4:
        print("Логин должен состоять минимум из 4 символов")
        main_menu()

    cursor.execute("SELECT id FROM Users WHERE login = %s ", (login, ))
    result = cursor.fetchone()
    if result:
        print("Пользователь с таким логином уже существует")
        main_menu()

    cursor.execute("INSERT INTO Users (user_name, age, login) VALUES (%s, %s, %s)", (name, age, login))
    connection.commit()
    print("Вы успешно зарегистрировались!")
    main_menu()


# Авторизация пользователя
def login_user():
    login = input("Введите логин: ")

    cursor.execute("SELECT id FROM Users WHERE login = %s ", (login, ))
    result = cursor.fetchone()
    if not result:
        print("Пользователь с таким логином не найден")
    else:
        global user_login
        user_login = result[0]
        print("Вы успешно авторизовались")
    main_menu()


# Список доступных опросов
def polls_list():
    get_polls_titles = "SELECT id, title from Polls"
    cursor.execute(get_polls_titles)
    polls = cursor.fetchall()

    # Если пользователь авторизован, получаем id опросов, где он участвовал
    user_polls = []
    if user_login is not None:
        cursor.execute(f"SELECT poll_id FROM Results WHERE user_id = {user_login}")
        user_polls = [int(x[0]) for x in cursor.fetchall()]

    if len(polls) == 0:
        print("Нет доступных опросов")

    for poll in polls:
        if poll[0] in user_polls:
            print(poll[1], "-Пройден")
        else:
            print(poll[1])
    main_menu()


# Получить список доступных опросов и выбрать опрос
def select_poll():
    if user_login is None:
        print("Необходимо авторизоваться")
        main_menu()
    else:
        cursor.execute(f"SELECT id, title FROM Polls WHERE id not in (SELECT poll_id FROM Results WHERE user_id = {user_login})")
        available_polls = cursor.fetchall()
        if len(available_polls) == 0:
            print("Нет доступных для прохождения опросов")
            main_menu()
        else:
            print("Введите номер опроса")
            for poll in available_polls:
                print(poll[0], "-", poll[1])
            poll_id = input()
            if int(poll_id) in [x[0] for x in available_polls]:
                ask_questions(int(poll_id))
            else:
                print("Данного опроса не существует")
                main_menu()


# Получение результатов от пользователя и запись их в базу
def ask_questions(poll_id: int):
    cursor.execute(f"SELECT questions FROM Polls WHERE id = {poll_id} ")
    result = cursor.fetchone()[0]
    questions = result.split(';')  # разделение вопросов по точке с запятой
    answers = []
    for question in questions:
        answer = input(question.strip() + '\n')
        answers.append(answer)
    print("Ваши ответы")
    for question, answer in zip(questions, answers):
        print(question, ": ", answer, sep="")
    print("Отправить результат? Да/Нет")
    send_answer = input()
    if send_answer == "Да":
        cursor.execute("INSERT INTO Results (answers, answer_date, poll_id, user_id) VALUES (%s, %s, %s, %s)", (";".join(answers), datetime.datetime.today().date(), poll_id, user_login))
        connection.commit()
        print("Вы успешно отправили ответы")
    else:
        print("Вы отменили отправку ответов")
    main_menu()


if __name__ == "__main__":
    print("Привет!\nЭто приложение для заполнения опросов")
    main_menu()
