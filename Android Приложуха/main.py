from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from screens import MainMenuScreen, InstructionsScreen, RegisterScreen, LoginScreen, ActionSelectionScreen, CreateTestScreen, TestScreen, TestSelectionScreen, ResultsScreen
from database import Database

class TestApp(App):
    def build(self):
        # Создание экземпляра Database
        self.database = Database("my_database.db")
        self.selected_test_id = None  # Добавленный атрибут

        # Создание экземпляра ScreenManager
        self.sm = ScreenManager()

        # Создаем экземпляр TestSelectionScreen с именем 'test_selection'
        test_selection_screen = TestSelectionScreen(name='test_selection')

        results_screen = ResultsScreen(name='results', database=self.database)

        # Добавление экранов в ScreenManager
        self.sm.add_widget(ActionSelectionScreen(name='action_selection'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainMenuScreen(name='main_menu'))
        self.sm.add_widget(InstructionsScreen(name='instructions'))
        self.sm.add_widget(CreateTestScreen(name='create_test'))
        self.sm.add_widget(test_selection_screen)
        self.sm.add_widget(results_screen)

        return self.sm

if __name__ == '__main__':
    TestApp().run()