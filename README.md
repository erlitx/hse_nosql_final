# 📚 Структура базы данных

## 1. Общая концепция

База данных предназначена для учёта оценок студентов университета. Основные пользователи:

- **Студенты** (могут просматривать свои оценки).
- **Преподаватели** (ставят оценки студентам).
- **Деканат** (анализирует академическую успеваемость).

---

## 2. Схема базы данных

В **MongoDB** храним информацию в 4 коллекциях:

### 1️⃣ students (Студенты)
```json
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
}
```

### 2️⃣ courses (Курсы)
```json
{
    "_id": ObjectId("..."),
    "course_id": "CS101",
    "name": "Алгоритмы и структуры данных",
    "instructor": {
        "first_name": "Сергей",
        "last_name": "Петров",
        "email": "petrov@university.edu"
    },
    "semester": "Весна 2025"
}
```

### 3️⃣ grades (Оценки)
```json
{
    "_id": ObjectId("..."),
    "student_id": "S12345",
    "course_id": "CS101",
    "grade": 5,
    "date": ISODate("2025-03-10T12:00:00Z"),
    "instructor": "Сергей Петров"
}
```

### 4️⃣ instructors (Преподаватели)
```json
{
    "_id": ObjectId("..."),
    "first_name": "Сергей",
    "last_name": "Петров",
    "email": "petrov@university.edu",
    "courses": ["CS101", "CS102"]
}
```

---

## 3. Индексы

Создаём вторичные индексы для оптимизации запросов:
```sh
db.students.createIndex({ "student_id": 1 }, { unique: true })
db.courses.createIndex({ "course_id": 1 }, { unique: true })
db.grades.createIndex({ "student_id": 1, "course_id": 1 })
db.instructors.createIndex({ "email": 1 }, { unique: true })
```

---

## 4. Запросы к базе данных

### 📌 1. Получить все курсы студента
```sh
db.grades.aggregate([
  { $match: { student_id: "S1001" } },
  { $lookup: {
      from: "courses",
      localField: "course_id",
      foreignField: "course_id",
      as: "course_info"
    }
  },
  { $unwind: "$course_info" },
  { $project: { _id: 0, course_name: "$course_info.name", grade: 1 } }
])
```

### 📌 2. Найти всех студентов конкретного курса
```sh
db.grades.find({ course_id: "CS101" })
```

### 📌 3. Найти средний балл студента
```sh
db.grades.aggregate([
  { $match: { student_id: "S1001" } },
  { $group: { _id: "$student_id", avg_grade: { $avg: "$grade" } } }
])
```

### 📌 4. Найти средний балл по курсу
```sh
db.grades.aggregate([
  { $match: { course_id: "CS101" } },
  { $group: { _id: "$course_id", avg_grade: { $avg: "$grade" } } }
])
```

### 📌 5. Найти студентов с баллом выше 4
```sh
db.grades.find({ grade: { $gt: 4 } }, { student_id: 1, grade: 1, _id: 0 })
```

### 📌 6. Найти последние 5 оценок студента
```sh
db.grades.find({ student_id: "S1001" }).sort({ date: -1 }).limit(5)
```

### 📌 7. Найти всех преподавателей, ведущих курс
```sh
db.courses.find({ course_id: "CS101" }, { instructor: 1, _id: 0 })
```

### 📌 8. Найти все курсы преподавателя
```sh
db.courses.find({ "instructor": "Сергей Петров" }, { course_id: 1, name: 1, _id: 0 }).pretty()
```

### 📌 9. Найти количество студентов по курсу
```sh
db.students.find({ student_id: "S1001" }, { _id: 0, name: 1, courses: 1 }).pretty()
```

### 📌 10. Найти самого успешного студента
```sh
db.grades.aggregate([
  { $group: { _id: "$student_id", avg_grade: { $avg: "$grade" } } },
  { $sort: { avg_grade: -1 } },
  { $limit: 1 }
])
```


