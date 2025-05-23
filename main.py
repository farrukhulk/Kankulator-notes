from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
import re
import os

AUTO_SAVE_INTERVAL = 300

class NotesApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.notes = {}
        self.current_note = None

        button_bar = BoxLayout(size_hint_y=0.1)
        for label, callback in [
            ("Новая", self.new_note),
            ("Сохранить", self.save_note),
            ("Вычислить", self.calculate),
            ("Поиск", self.search_notes)
        ]:
            btn = Button(text=label)
            btn.bind(on_release=callback)
            button_bar.add_widget(btn)

        self.search_input = TextInput(hint_text="Поиск...", size_hint_x=0.3)
        button_bar.add_widget(self.search_input)
        self.add_widget(button_bar)

        self.note_list = BoxLayout(size_hint_y=0.1)
        self.add_widget(self.note_list)

        self.text_area = TextInput(text='', font_size=18, multiline=True)
        self.add_widget(self.text_area)

        self.load_last_session()
        Clock.schedule_interval(lambda dt: self.auto_save(), AUTO_SAVE_INTERVAL)

    def new_note(self, *args):
        note_name = f"note_{len(self.notes)+1}"
        self.notes[note_name] = ''
        self.current_note = note_name
        self.update_note_list()
        self.text_area.text = ''

    def update_note_list(self):
        self.note_list.clear_widgets()
        for name in self.notes:
            btn = Button(text=name)
            btn.bind(on_release=lambda instance, n=name: self.switch_note(n))
            self.note_list.add_widget(btn)

    def switch_note(self, name):
        self.notes[self.current_note] = self.text_area.text
        self.current_note = name
        self.text_area.text = self.notes[name]

    def save_note(self, *args):
        if not self.current_note:
            return
        text = self.text_area.text
        filename = f"{self.current_note}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        self.show_popup("Сохранено", f"Заметка сохранена в {filename}")

    def calculate(self, *args):
        text = self.text_area.text
        def replace_expr(match):
            expr = match.group(1).strip()
            try:
                result = eval(expr, {"__builtins__": None, "math": __import__('math')})
                return f"= {expr} → {result}"
            except:
                return match.group(0)
        updated_text = re.sub(r'=\s*(.*?)(?=\n|$)', replace_expr, text)
        self.text_area.text = updated_text

    def search_notes(self, *args):
        query = self.search_input.text.strip()
        if not query:
            return
        content = self.text_area.text
        if query in content:
            self.show_popup("Найдено", f"Найдено в текущей заметке.")
        else:
            self.show_popup("Не найдено", f""{query}" не найдено.")

    def auto_save(self):
        if self.current_note:
            with open(f"autosave_{self.current_note}.txt", "w", encoding="utf-8") as f:
                f.write(self.text_area.text)

    def load_last_session(self):
        for fname in os.listdir():
            if fname.startswith("autosave_note_"):
                name = fname.replace("autosave_", "").replace(".txt", "")
                with open(fname, "r", encoding="utf-8") as f:
                    self.notes[name] = f.read()
        if self.notes:
            first = list(self.notes.keys())[0]
            self.current_note = first
            self.update_note_list()
            self.text_area.text = self.notes[first]

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

class MainApp(App):
    def build(self):
        return NotesApp()

if __name__ == '__main__':
    MainApp().run()