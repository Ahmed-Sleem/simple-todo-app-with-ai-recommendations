import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import google.generativeai as genai


class TODOs(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        todo_label = toga.Label(
            "Add TODO:",
            style=Pack(padding=(0, 5), font_size=16),
        )

        self.todo_input = toga.TextInput(style=Pack(flex=1, padding=5))

        todo_box = toga.Box(style=Pack(direction=ROW, padding=(0, 5)))
        todo_box.add(todo_label)
        todo_box.add(self.todo_input)

        button = toga.Button(
            "Add",
            on_press=self.add_todo_item,
            style=Pack(padding=5, background_color='steelblue', color='white', font_size=14),
        )

        self.todos = toga.Box(style=Pack(direction=COLUMN, padding=(0, 10)))

        main_box.add(todo_box)
        main_box.add(button)
        main_box.add(self.todos)

        self.main_window = toga.MainWindow(title=self.formal_name, size=(400, 500))
        self.main_window.content = main_box
        self.main_window.show()

    def add_todo_item(self, *_: any):
        todo = self.todo_input.value.strip()
        if not todo:
            return
        todo_text = f"- {todo}"  # Adding "-" before todo text
        recommendations = self.recommend(todo_text)  # Assuming recommend() returns recommendation

        todo_label = toga.Label(todo_text, style=Pack(padding=(0, 5), flex=1, font_size=14))
        todo_button = toga.Button(
            "X",
            on_press=self.delete_todo_item,
            style=Pack(padding=5, background_color='tomato', color='white', font_size=12),
        )

        # Label to display recommendations
        recommendation_label = toga.Label(
            recommendations,
            style=Pack(padding=(0, 5), font_size=10, color='gray'),  # Adjusted style
        )

        # Box to contain todo label and "X" button
        todo_content_box = toga.Box(style=Pack(direction=ROW, padding=5))
        todo_content_box.add(todo_label)
        todo_content_box.add(todo_button)

        todo_box = toga.Box(style=Pack(direction=COLUMN, padding=5, alignment=CENTER))
        todo_box.add(todo_content_box)  # Add todo content box
        todo_box.add(recommendation_label)  # Add recommendation label under todo label
        self.todos.add(todo_box)
        self.todo_input.value = ""

    def delete_todo_item(self, widget: toga.Button, **_: any):
        if widget.parent is None:
            return
        # Removing todo box instead of its parent
        self.todos.remove(widget.parent.parent)

    def chat(self, inp):
        api_key = "YOUR API KEY FOR GOOGLE GEMINI"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content(inp)
        if response.text:
            return response.text
        else:
            print("error:")
            print(response)
            return response

    def recommend(self, todo):
        prompt = f"""
            I will provide you with a todo list item from my todo list and I need you to give me a small sized recommendation like a website url or something,
            this recommendation must be short and useful, please make the max char in the line = 80 and wrap the text to next line if needed
            My todo item: "{todo}"
        """
        response = self.chat(prompt)
        return response


def main():
    return TODOs()
