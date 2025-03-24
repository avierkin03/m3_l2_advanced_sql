import sqlite3

# Підключення до бази даних
conn = sqlite3.connect("university.db")
cursor = conn.cursor()


# Створення таблиць
cursor.execute('''CREATE TABLE IF NOT EXISTS students(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    major TEXT
               )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_name TEXT,
                    instructor TEXT
                )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS student_courses (
                    student_id INTEGER,
                    course_id INTEGER,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (course_id) REFERENCES courses(course_id),
                    PRIMARY KEY (student_id, course_id)
                )''')


# Інтерфейс користувача
while True:
    print("\n1. Додати нового студента")
    print("2. Додати новий курс")
    print("3. Показати список студентів")
    print("4. Показати список курсів")
    print("5. Зареєструвати студента на курс")
    print("6. Показати студентів на конкретному курсі")
    print("7. Вийти")

    choice = input("Оберіть опцію (1-7): ")

    # Додавання нового студента
    if choice == "1":
        name = input("Введіть ім'я студента: ")
        age = int(input("Введіть вік студента: "))
        major = input("Введіть спеціальність студента: ")
        cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
        conn.commit()

    # Додавання нового курсу
    elif choice == "2":
        course_name = input("Введіть назву курсу: ")
        instructor = input("Введіть викладача курсу: ")
        cursor.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (course_name, instructor))
        conn.commit()

    # Показати список студентів
    elif choice == "3":
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
 
        if not students:
            print("У базі даних немає зареєстрованих студентів.")
        else:
            print("\nСписок студентів:")
            for student in students:
                print(f"ID: {student[0]}, Ім'я: {student[1]}, Вік: {student[2]}, Спеціальність: {student[3]}")
        
    # Показати список курсів
    elif choice == "4":
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
 
        if not courses:
            print("У базі даних немає зареєстрованих курсів.")
        else:
            print("\nСписок курсів:")
            for course in courses:
                print(f"ID: {course[0]}, Назва курсу: {course[1]}, Викладач: {course[2]}")
    
    # Зареєструвати студента на курс
    elif choice == "5":
        student_id = int(input("Введіть ID студента: "))
        course_id = int(input("Введіть ID курсу: "))
 
        # Перевірка існування студента
        cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
        student_exists = cursor.fetchone()
        
        # Перевірка існування курсу
        cursor.execute("SELECT course_id FROM courses WHERE course_id = ?", (course_id,))
        course_exists = cursor.fetchone()
        
        if not student_exists:
            print(f"Студента з ID {student_id} немає в базі даних.")
        elif not course_exists:
            print(f"Курсу з ID {course_id} немає в базі даних.")
        else:
            try:
                cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
                conn.commit()
                print(f"Студент з ID {student_id} успішно зареєстрований на курс з ID {course_id}.")
            except sqlite3.IntegrityError:
                print(f"Студент з ID {student_id} уже зареєстрований на курс з ID {course_id}.")


    # Показати студентів на конкретному курсі
    elif choice == "6":
        course_id = int(input("Введіть ID курсу для фільтрації: "))
        cursor.execute('''SELECT students.id, students.name, students.age, students.major
                          FROM students, student_courses
                          WHERE students.id = student_courses.student_id
                          AND student_courses.course_id = ?''', (course_id,))
        students_on_course = cursor.fetchall()
 
        if not students_on_course:
            print(f"На курсі з ID {course_id} немає зареєстрованих студентів.")
        else:
            print(f"\nСписок студентів на курсі з ID {course_id}:")
            for student in students_on_course:
                print(f"ID: {student[0]}, Ім'я: {student[1]}, Вік: {student[2]}, Спеціальність: {student[3]}")
        
       
    elif choice == "7":
        break

    else:
        print("Некоректний вибір. Будь ласка, введіть число від 1 до 7.")