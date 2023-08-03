import sqlite3

def create_tables_and_insert_data():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS countries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        area REAL DEFAULT 0,
                        country_id INTEGER,
                        FOREIGN KEY (country_id) REFERENCES countries (id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        city_id INTEGER,
                        FOREIGN KEY (city_id) REFERENCES cities (id)
                    )''')


    countries = [('Кыргызстан',), ('Германия',), ('Китай',), ('США',), ('Франция',), ('Россия',), ('Япония',)]
    cursor.executemany("INSERT INTO countries (title) VALUES (?)", countries)

    cities = [
        ('Бишкек', 1285, 1), ('Ош', 325, 1), ('Берлин', 891.68, 2), ('Пекин', 16410.54, 3),
        ('Нью-Йорк', 783.84, 4), ('Париж', 105.4, 5), ('Москва', 2561.52, 6), ('Токио', 2187.66, 7)
    ]
    cursor.executemany("INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)", cities)

    employees = [
        ('Иван', 'Иванов', 1), ('Петр', 'Петров', 2), ('Мария', 'Сидорова', 3),
        ('John', 'Doe', 4), ('Jean', 'Dupont', 5), ('Иван', 'Смирнов', 6),
        ('Таро', 'Ямада', 7), ('Анна', 'Иванова', 1), ('Robert', 'Johnson', 4),
        ('Marie', 'Martin', 5), ('Дмитрий', 'Петров', 6), ('Сакура', 'Танака', 7),
        ('Kate', 'Smith', 4), ('Александр', 'Сергеев', 6), ('Люси', 'Харрис', 3)
    ]
    cursor.executemany("INSERT INTO employees (first_name, last_name, city_id) VALUES (?, ?, ?)", employees)

    conn.commit()
    conn.close()

def print_cities():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM cities')
    cities = cursor.fetchall()
    print('Список городов:')
    for city in cities:
        print(f"{city[0]}. {city[1]}")
    print('')
    conn.close()

def print_employees_by_city(city_id):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT e.first_name, e.last_name, co.title, c.title, c.area
                      FROM employees e
                      INNER JOIN cities c ON e.city_id = c.id
                      INNER JOIN countries co ON c.country_id = co.id
                      WHERE e.city_id = ?''', (city_id,))
    employees = cursor.fetchall()
    if employees:
        print('Сотрудники живущие в этом городе:')
        for emp in employees:
            print(f"Имя: {emp[0]}, Фамилия: {emp[1]}, Страна: {emp[2]}, Город: {emp[3]}, Площадь города: {emp[4]} км²")
    else:
        print('В этом городе нет сотрудников.')
    print('')
    conn.close()

def main():
    create_tables_and_insert_data()

    print("Вы можете отобразить список сотрудников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
    print_cities()
    while True:
        try:
            city_id = int(input("Введите id города: "))
            if city_id == 0:
                break
            print_employees_by_city(city_id)
        except ValueError:
            print("Введите целое число.")

if __name__ == "__main__":
    main()
