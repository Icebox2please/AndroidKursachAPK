from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from database import Database
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.uix.dropdown import DropDown


class ActionSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ActionSelectionScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Select Action', font_size=50))
        layout.add_widget(Button(text='Register', on_press=self.register_action))
        layout.add_widget(Button(text='Login', on_press=self.login_action))
        self.add_widget(layout)

    def register_action(self, instance):
        self.manager.current = 'register'

    def login_action(self, instance):
        self.manager.current = 'login'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Register', font_size=50))
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(Button(text='Register', on_press=self.register))
        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            popup = Popup(title='Error', content=Label(text='Please enter both username and password.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        db = Database("my_database.db")
        db.create_users_table()

        try:
            db.register_user(username, password)
            popup = Popup(title='Success', content=Label(text='Registration successful!'), size_hint=(None, None), size=(400, 200))
            popup.open()
            self.manager.current = 'login'
        except Exception as e:
            popup = Popup(title='Error', content=Label(text=str(e)), size_hint=(None, None), size=(400, 200))
            popup.open()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Login', font_size=50))
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(Button(text='Login', on_press=self.login))
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            popup = Popup(title='Error', content=Label(text='Please enter both username and password.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        db = Database("my_database.db")
        db.create_users_table()

        if db.login_user(username, password):
            popup = Popup(title='Success', content=Label(text='Login successful!'), size_hint=(None, None), size=(400, 200))
            popup.open()
            self.manager.current = 'main_menu'
        else:
            popup = Popup(title='Error', content=Label(text='Invalid username or password.'), size_hint=(None, None), size=(400, 200))
            popup.open()

class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super(InstructionsScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Instructions', font_size=50))
        layout.add_widget(Label(text='Welcome to our app!', font_size=20))
        layout.add_widget(Label(text='Instructions:'))
        layout.add_widget(Label(text='- To create a new test, press "Create Test" on the main menu.'))
        layout.add_widget(Label(text='- To start a test, press "Start Test" on the main menu.'))
        layout.add_widget(Label(text='- To view results, press "View Results" on the main menu.'))
        layout.add_widget(Button(text='Back to Main Menu', on_press=self.back_to_main_menu))
        self.add_widget(layout)

    def back_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text='Main Menu', font_size=50))
        layout.add_widget(Button(text='Start Test', on_press=self.show_test_selection))  # Изменено на вызов метода show_test_selection
        layout.add_widget(Button(text='View Results', on_press=self.show_results))
        layout.add_widget(Button(text='Instructions', on_press=self.show_instructions))
        layout.add_widget(Button(text='Create Test', on_press=self.create_test))
        self.add_widget(layout)

    def show_results(self, instance):
        self.manager.current = 'results'

    def show_test_selection(self, instance):
        self.manager.current = 'test_selection'  # Переходим на экран с выбором тестов

    def show_instructions(self, instance):
        self.manager.current = 'instructions'

    def create_test(self, instance):
        current_test_id = 1
        create_test_screen = CreateTestScreen(current_test_id=current_test_id)
        self.manager.current = 'create_test'


class TestSelectionScreen(Screen):
    selected_test_id = None

    def __init__(self, **kwargs):
        super(TestSelectionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Choose Test', on_press=self.show_test_selection))
        self.add_widget(layout)

    def show_test_selection(self, instance):
        app = App.get_running_app()  # Получаем экземпляр текущего приложения
        db = app.database  # Получаем экземпляр базы данных из текущего приложения
        available_tests = db.get_available_tests()

        if not available_tests:
            popup = Popup(title='No Tests Available', content=Label(text='There are no tests available.'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        popup_content = BoxLayout(orientation='vertical', padding=10)
        popup = Popup(title='Choose Test', content=popup_content, size_hint=(None, None), size=(400, 400))

        for test_id, test_name in available_tests:
            button = Button(text=test_name, size_hint=(1, None), height=40)
            button.bind(on_press=lambda instance, test_id=test_id: self.select_test(test_id, popup))
            popup_content.add_widget(button)

        popup.open()

    def select_test(self, test_id, popup):
        self.selected_test_id = test_id
        app = App.get_running_app()  # Получаем текущий экземпляр приложения
        first_question_index = app.database.get_first_question_index(
            test_id)  # Получаем номер первого вопроса для выбранного теста
        test_screen = TestScreen(name='test', test_id_value=test_id,
                                 database_instance=app.database,
                                 current_question_index=first_question_index)  # Передаем базу данных из текущего экземпляра приложения и номер первого вопроса
        self.manager.add_widget(test_screen)
        self.manager.current = 'test'
        popup.dismiss()


class TestScreen(Screen):
    def __init__(self, test_id_value=None, database_instance=None, current_question_index=0, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.test_id_value = test_id_value
        self.database_instance = database_instance
        self.current_question_index = current_question_index
        self.answers = []  # Список для хранения ответов пользователя

        # Создаем вертикальный контейнер для размещения элементов
        layout = BoxLayout(orientation='vertical')

        # Метка с вопросом
        self.question_label = Label(text="", font_size=20, size_hint=(1, None), height=dp(200), halign='center')
        layout.add_widget(self.question_label)

        # Поле для ввода ответа
        self.answer_input = TextInput(hint_text="Enter your answer", multiline=False)
        layout.add_widget(self.answer_input)

        # Кнопка для перехода к следующему вопросу
        next_button = Button(text="Next Question", size_hint=(None, None), size=(150, 50))
        next_button.bind(on_press=self.next_question)
        layout.add_widget(next_button)

        # Добавляем контейнер на экран
        self.add_widget(layout)

        self.load_question()  # Загружаем первый вопрос при создании экрана

    def load_question(self):
        test_id = self.test_id_value
        question = self.database_instance.load_question_from_test(test_id, self.current_question_index) # Используем текущий индекс вопроса
        print("current_question_index:", self.current_question_index)
        if question:
            self.question_label.text = question
        else:
            self.question_label.text = "No questions found for the selected test."
            self.ids.next_question_button.text = "Finish Test"

    def next_question(self, instance):
        # Получаем ответ пользователя
        user_answer = self.answer_input.text
        # Добавляем его в список ответов
        self.answers.append(user_answer)

        # Загружаем следующий вопрос
        test_id = self.test_id_value
        self.current_question_index += 1
        print("Current question index:", self.current_question_index)  # Добавляем отладочный вывод
        question = self.database_instance.load_next_question(test_id, self.current_question_index, self.answers)
        if question:
            self.question_label.text = question
            self.answer_input.text = ""  # Очищаем поле ввода
        else:
            # Если вопросы закончились, изменяем поведение кнопки "Next Question"
            instance.text = "Finish Test"
            instance.unbind(on_press=self.next_question)
            instance.bind(on_press=self.finish_test)

    def finish_test(self, instance):
        # Переходим на экран меню
        self.manager.current = "main_menu"

        # Проверяем, были ли сохранены ответы
        if self.answers:
            # Выводим результаты теста
            print("Test finished. User answers:")
            for i, answer in enumerate(self.answers):
                print(f"Question {i + 1}: {answer}")

            # Загружаем правильные ответы для выбранного теста
            correct_answers = self.database_instance.load_answers_for_test(self.test_id_value)

            # Сравниваем ответы пользователя с правильными ответами
            correct_count = sum(1 for user_answer, correct_answer in zip(self.answers, correct_answers) if
                                user_answer == correct_answer)
            total_questions = len(correct_answers)
            print(f"Correct Answers: {correct_count}/{total_questions}")

            # Сохраняем результаты теста в базе данных
            self.database_instance.save_test_result(self.test_id_value, correct_count, total_questions)

        else:
            print("No answers were provided.")

        # Выводим содержимое списка сохраненных ответов
        print("Saved answers:", self.answers)


    def back_to_menu(self, instance):
        self.manager.current = "main_menu"



class ResultsScreen(Screen):
    def __init__(self, database, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.database = database

        # Добавим выпадающий список для выбора теста
        self.dropdown = DropDown()

        # По умолчанию покажем заглушку
        self.results_label = Label(text="Select a test to view results", font_size=20)

        # Создаем главный макет, используя вертикальное расположение
        main_layout = BoxLayout(orientation='vertical')

        # Создаем макет для кнопки Select Test, используя горизонтальное расположение
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Добавляем кнопку для открытия списка тестов
        self.dropdown_button = Button(text='Select Test')
        self.dropdown_button.bind(on_release=self.dropdown.open)

        # Добавляем кнопку для выхода в меню
        self.menu_button = Button(text='Menu')
        self.menu_button.bind(on_release=self.go_to_menu)

        # Добавляем кнопки в макет
        button_layout.add_widget(self.dropdown_button)
        button_layout.add_widget(self.menu_button)

        # Добавляем макет с кнопкой в главный макет
        main_layout.add_widget(button_layout)

        # Добавляем метку для отображения результатов в главный макет
        main_layout.add_widget(self.results_label)

        # Добавляем главный макет на экран
        self.add_widget(main_layout)

        # Загружаем список тестов из базы данных
        self.load_tests()

    def load_tests(self):
        # Получаем список доступных тестов из базы данных
        tests = self.database.get_available_tests()

        # Добавляем каждый тест в выпадающий список
        for test_id, test_name in tests:
            btn = Button(text=test_name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.show_results(self.database.get_test_id_by_name(btn.text)))
            self.dropdown.add_widget(btn)

    def show_results(self, selected_test_id):
        # Загружаем результаты выбранного теста из базы данных
        results = self.database.load_results_for_test(selected_test_id)

        # Очищаем предыдущие результаты из метки
        self.results_label.text = ""

        # Проверяем, есть ли результаты для выбранного теста
        if results:
            # Добавляем заголовок с информацией о тесте
            self.results_label.text += "Results for Test {}: \n".format(selected_test_id)

            # Перебираем результаты и добавляем их в метку
            for result in results:
                self.results_label.text += "Result ID from bd: {}, Correct Answers: {}, Total Questions: {}\n".format(
                    result[0], result[2], result[3])
        else:
            # Если результатов нет, отображаем соответствующее сообщение
            self.results_label.text = "No results available for selected test"

    def go_to_menu(self, instance):
        self.manager.current = "main_menu"


class CreateTestScreen(Screen):
    def __init__(self, current_test_id=None, **kwargs):
        super(CreateTestScreen, self).__init__(**kwargs)
        self.current_test_id = current_test_id
        layout = GridLayout(cols=1, padding=10)

        self.question_input = TextInput(hint_text='Enter question', multiline=False)
        self.answer_input = TextInput(hint_text='Enter answer', multiline=False)

        self.next_question_button = Button(text='Next Question', on_press=self.next_question)
        self.finish_button = Button(text='Finish Test', on_press=self.finish_test)
        self.back_to_main_menu_button = Button(text='Back to Main Menu', on_press=self.back_to_main_menu)

        layout.add_widget(Label(text='Create Test', font_size=50))
        layout.add_widget(self.question_input)
        layout.add_widget(self.answer_input)
        layout.add_widget(self.next_question_button)
        layout.add_widget(self.finish_button)
        layout.add_widget(self.back_to_main_menu_button)

        self.add_widget(layout)

        self.db = Database("my_database.db")  # Путь к вашей базе данных

        # Создание пустого списка вопросов при создании экрана
        self.questions_list = []

    def next_question(self, instance):
        question = self.question_input.text
        answer = self.answer_input.text

        # Добавляем вопрос и ответ в список вопросов
        self.questions_list.append((question, answer))

        # Очищаем поля ввода
        self.question_input.text = ''
        self.answer_input.text = ''

    def finish_test(self, instance):
        if self.questions_list:
            # Создаем всплывающее окно для ввода имени теста
            popup_content = GridLayout(cols=1, padding=10)
            test_name_input = TextInput(hint_text='Enter test name', multiline=False)
            ok_button = Button(text='OK', size_hint=(1, None), height=40)
            popup_content.add_widget(test_name_input)
            popup_content.add_widget(ok_button)
            popup = Popup(title='Enter Test Name', content=popup_content, size_hint=(None, None), size=(400, 200))
            ok_button.bind(on_press=lambda instance: self.save_test(test_name_input.text, popup))
            popup.open()
        else:
            # Предупреждение, если список вопросов пуст
            popup = Popup(title='Warning', content=Label(text='Please add at least one question.'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def save_test(self, test_name, popup):
        # Вызываем метод save_test из базы данных, передавая имя теста и список вопросов
        self.db.save_test(test_name, self.questions_list)

        # Закрываем всплывающее окно
        popup.dismiss()

        # Переходим на главное меню
        self.manager.current = 'main_menu'

    def back_to_main_menu(self, instance):
        self.manager.current = 'main_menu'
