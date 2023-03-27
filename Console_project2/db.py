import sqlalchemy
from sqlalchemy.orm import sessionmaker
from base import Students, Marks, Subjects

engine = sqlalchemy.create_engine("mysql+pymysql://root:root@localhost:3306/journal_app")
Session = sessionmaker(bind=engine)
session = Session()


def students_list() -> list:
    students = session.query(Students).all()
    return [[student.id, student.Name] for student in students]


def db_make_student(name: str, age: int, grade: str) -> None:
    new_student = Students(name, age, grade)
    session.add(new_student)
    session.commit()


def db_delete_student(student_id: int) -> int:  # Return a status: 0 - User not found; 1 - Success delete
    student = session.query(Students).filter(Students.id == student_id).first()
    if student is None:
        return 0
    else:
        session.query(Marks).filter(Marks.Student_id == student_id).delete()
        session.delete(student)
        session.commit()
        return 1


def db_get_student_marks(student_id: int) -> [list, int]:  # Return marks and a status: 0 - User not found; 1 - Found
    student = session.query(Students).filter(Students.id == student_id).first()
    if student is None:
        return [], 0
    marks = session.query(Marks.Mark, Subjects.Name).join(Subjects, Marks.Subject_id == Subjects.id).filter(Marks.Student_id == student_id).order_by(Subjects.Name).all()
    grouped_marks = []
    subj_id = -1  # index of list where we put our marks
    last_subj = ""  # group by subject
    for mark, subject in marks:
        if subject != last_subj:
            subj_id += 1
            grouped_marks.append([subject, []])
            last_subj = subject
        grouped_marks[subj_id][1].append(mark)
    return grouped_marks, 1  # Result must be [[Subject_name, [5, 5, 4, 3]], [Subject_name, [5, 5, 4, 3]]]


def db_get_student_mark_by_subject(student_id: int, subject: str) -> [list, int]:  # Return marks and
    # a status 0 - User not found; 1 - Success; 2 - subject not found
    student = session.query(Students).filter(Students.id == student_id).first()
    subject_obj = session.query(Subjects).filter(Subjects.Name == subject).first()
    if student is None:
        return [], 0
    elif subject_obj is None:
        return [], 2
    else:
        marks = session.query(Marks.Mark).filter(Marks.Student_id == student_id,
                                                    Marks.Subject_id == subject_obj.id).all()
        return [mark[0] for mark in marks], 1


def db_get_subject_marks(subject: str) -> [list, int]:  # Return marks and a status: 0 - Subject not found; 1 - Found
    subject_obj = session.query(Subjects).filter(Subjects.Name == subject).first()
    if subject_obj is None:
        return [], 0
    marks = session.query(Marks.Mark, Students.Name).join(Students, Marks.Student_id == Students.id).filter(Marks.Subject_id == subject_obj.id).order_by(Marks.Student_id).all()
    grouped_marks = []
    stud_id = -1  # index of list where we put our marks
    last_stud = ""  # group by subject
    for mark, student in marks:
        if student != last_stud:
            stud_id += 1
            grouped_marks.append([student, []])
            last_stud = student
        grouped_marks[stud_id][1].append(mark)
    return grouped_marks, 1  # Result must be [[Student_name, [5, 5, 4, 3]], [Student_name, [5, 5, 4, 3]]]


def db_new_mark(student_id: int, subject: str, mark: int) -> int:  # Return a status: 0 - User not found; 1 - Success;
    # 2 - subject not found
    student = session.query(Students).filter(Students.id == student_id).first()
    subject_obj = session.query(Subjects).filter(Subjects.Name == subject).first()
    print(subject_obj)
    if student is None:
        return 0
    elif subject_obj is None:
        return 2
    else:
        new_mark = Marks(student_id, subject_obj.id, mark)
        session.add(new_mark)
        session.commit()
        return 1


def db_subject_list() -> list:
    subjects = session.query(Subjects.Name).all()
    return [subject[0] for subject in subjects]


def db_add_subject(name: str) -> int:  # Return Status: 0 - Subject is exist; 1 - Success
    subject_obj = session.query(Subjects).filter(Subjects.Name == name).first()
    if subject_obj is None:
        new_subject = Subjects(name)
        session.add(new_subject)
        session.commit()
        return 1
    else:
        return 0


def db_delete_subject(name: str) -> int:  # Return Status: 0 - Subject is not found; 1 - Success
    subject_obj = session.query(Subjects).filter(Subjects.Name == name).first()
    if subject_obj is None:
        return 0
    else:
        session.delete(subject_obj)
        session.commit()
        return 1
