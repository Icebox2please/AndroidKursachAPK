import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.loaded_question_ids = []  # сделаем его публичным
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_questions_table()
        self.create_users_table()
        self.create_tests_table()
        self.create_results_table()  # Добавляем вызов метода create_results_table

    def create_questions_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                                id INTEGER PRIMARY KEY,
                                test_id INTEGER,
                                question TEXT,
                                answer TEXT
                                )''')
        self.conn.commit()

    def load_random_question(self):
        self.cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
        question = self.cursor.fetchone()
        return question

    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT,
                                password TEXT
                                )''')
        self.conn.commit()

    def create_tests_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tests (
                                id INTEGER PRIMARY KEY,
                                test_name TEXT
                                )''')
        self.conn.commit()

    def create_results_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                                id INTEGER PRIMARY KEY,
                                test_id INTEGER,
                                correct_answers INTEGER,
                                total_questions INTEGER
                                )''')
        self.conn.commit()

    def save_question(self, test_id, question, answer):
        self.cursor.execute('''INSERT INTO questions (test_id, question, answer) VALUES (?, ?, ?)''', (test_id, question, answer))
        self.conn.commit()

    def register_user(self, username, password):
        self.cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
        self.conn.commit()

    def login_user(self, username, password):
        self.cursor.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False

    def save_test(self, test_name, questions):
        self.cursor.execute('''INSERT INTO tests (test_name) VALUES (?)''', (test_name,))
        self.conn.commit()
        test_id = self.cursor.lastrowid
        for question, answer in questions:
            self.save_question(test_id, question, answer)

    def get_available_tests(self):
        self.cursor.execute("SELECT id, test_name FROM tests")
        tests = self.cursor.fetchall()
        return tests

    def load_test(self, test_id):
        self.cursor.execute("SELECT * FROM tests WHERE id=?", (test_id,))
        test = self.cursor.fetchone()
        return test

    def load_question_from_test(self, test_id, current_question_index):
        self.cursor.execute("SELECT question FROM questions WHERE test_id=? AND id=?",
                            (test_id, current_question_index))
        question = self.cursor.fetchone()
        print("Question:", question)  # Добавим эту строку для отладочного вывода
        if question:
            return question[0]  # Возвращаем текст вопроса
        else:
            return "No question found for the specified test ID"

    def load_next_question(self, test_id, current_question_index, loaded_question_ids):
        print("Loaded question IDs:", loaded_question_ids)  # Добавляем отладочный вывод
        query = "SELECT question FROM questions WHERE test_id=? AND id >= ? AND id NOT IN ({}) ORDER BY id LIMIT 1".format(
            ','.join('?' * len(loaded_question_ids)))
        params = (test_id, current_question_index, *loaded_question_ids)
        print("Query:", query)
        print("Params:", params)
        self.cursor.execute(query, params)
        next_question = self.cursor.fetchone()
        print("Next question:", next_question)
        if next_question:
            return next_question[0]
        else:
            return None

    def save_test_result(self, test_id, correct_answers, total_questions):
        self.cursor.execute(
            '''INSERT INTO results (test_id, correct_answers, total_questions) VALUES (?, ?, ?)''',
            (test_id, correct_answers, total_questions))
        self.conn.commit()

    def load_answers_for_test(self, test_id):
        self.cursor.execute("SELECT answer FROM questions WHERE test_id=?", (test_id,))
        results = self.cursor.fetchall()
        answers = [result[0] for result in results]
        print("correct ans", answers)
        return answers


    def get_user_id(self, username):
        self.cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Возвращаем id пользователя из запроса
        else:
            return None  # Возвращаем None, если пользователь не найден

    def reset_loaded_questions(self):
        self.loaded_question_ids = []

    def get_questions_for_test(self, test_id):
        print("Requested test_id:", test_id)  # Отладочный вывод для проверки запрошенного test_id
        self.cursor.execute("SELECT question FROM questions WHERE test_id=?", (test_id,))
        questions = self.cursor.fetchall()
        print("Retrieved questions:", questions)  # Отладочный вывод для проверки полученных вопросов
        return questions

    def get_test_name(self, test_id):
        self.cursor.execute("SELECT test_name FROM tests WHERE id=?", (test_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Возвращаем имя теста из запроса
        else:
            return None  # Возвращаем None, если тест не найден

    def get_questions_count(self, test_id):
        self.cursor.execute("SELECT COUNT(*) FROM questions WHERE test_id=?", (test_id,))
        count = self.cursor.fetchone()[0]
        return count

    def get_first_question_index(self, test_id):
        self.cursor.execute("SELECT MIN(id) FROM questions WHERE test_id=?", (test_id,))
        first_question_index = self.cursor.fetchone()[0]
        return first_question_index

    def load_results_for_test(self, test_id):
        self.cursor.execute("SELECT * FROM results WHERE test_id=?", (test_id,))
        results = self.cursor.fetchall()
        return results

    def get_test_id_by_name(self, test_name):
        self.cursor.execute("SELECT id FROM tests WHERE test_name=?", (test_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Возвращаем id теста из запроса
        else:
            return None  # Возвращаем None, если тест с указанным именем не найден