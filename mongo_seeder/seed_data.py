import os
import pymongo
from datetime import datetime
from random import choice, randint

# Подключение к MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin@mongo:27017/university?authSource=admin")
print(f'---------------{MONGO_URI}')
client = pymongo.MongoClient(MONGO_URI)
db = client.university

# Очистка коллекций (если уже есть данные)
db.students.delete_many({})
db.courses.delete_many({})
db.grades.delete_many({})
db.instructors.delete_many({})

# Данные
# students = [
#     {"student_id": "S1001", "first_name": "Иван", "last_name": "Иванов", "group": "B-01", "faculty": "ФКН", "enrollment_year": 2023},
#     {"student_id": "S1002", "first_name": "Мария", "last_name": "Петрова", "group": "B-01", "faculty": "ФКН", "enrollment_year": 2023},
#     {"student_id": "S1003", "first_name": "Алексей", "last_name": "Сидоров", "group": "B-02", "faculty": "ФКН", "enrollment_year": 2023},
# ]

students = [
    {
        "student_id": "S1001",
        "first_name": "Иван",
        "last_name": "Иванов",
        "group": "B-01",
        "faculty": "ФКН",
        "enrollment_year": 2023,
        "courses": [
            {"course_id": "CS101", "name": "Алгоритмы", "semester": "Весна 2025", "grade": 90},
            {"course_id": "CS102", "name": "Базы данных", "semester": "Осень 2025", "grade": 85}
        ]
    },
    {
        "student_id": "S1002",
        "first_name": "Мария",
        "last_name": "Петрова",
        "group": "B-01",
        "faculty": "ФКН",
        "enrollment_year": 2023,
        "courses": [
            {"course_id": "CS101", "name": "Алгоритмы", "semester": "Весна 2025", "grade": 92},
            {"course_id": "CS103", "name": "Машинное обучение", "semester": "Осень 2025", "grade": 88}
        ]
    },
    {
        "student_id": "S1003",
        "first_name": "Алексей",
        "last_name": "Сидоров",
        "group": "B-02",
        "faculty": "ФКН",
        "enrollment_year": 2023,
        "courses": [
            {"course_id": "CS102", "name": "Базы данных", "semester": "Осень 2025", "grade": 80},
            {"course_id": "CS104", "name": "Компьютерные сети", "semester": "Весна 2025", "grade": 78}
        ]
    }
]


courses = [
    {"course_id": "CS101", "name": "Алгоритмы", "semester": "Весна 2025", "instructor": "Сергей Петров"},
    {"course_id": "CS102", "name": "Базы данных", "semester": "Осень 2025", "instructor": "Анна Смирнова"},
]

instructors = [
    {"first_name": "Сергей", "last_name": "Петров", "email": "petrov@university.edu", "courses": ["CS101"]},
    {"first_name": "Анна", "last_name": "Смирнова", "email": "smirnova@university.edu", "courses": ["CS102"]},
]

grades = [
    {"student_id": "S1001", "course_id": "CS101", "grade": 5, "date": datetime(2025, 3, 10), "instructor": "Сергей Петров"},
    {"student_id": "S1002", "course_id": "CS101", "grade": 4, "date": datetime(2025, 3, 11), "instructor": "Сергей Петров"},
    {"student_id": "S1003", "course_id": "CS102", "grade": 5, "date": datetime(2025, 3, 12), "instructor": "Анна Смирнова"},
]

# Добавление данных в MongoDB
db.students.insert_many(students)
db.courses.insert_many(courses)
db.instructors.insert_many(instructors)
db.grades.insert_many(grades)

print("✅ Данные успешно добавлены в MongoDB!")
