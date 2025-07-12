from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.label = Label(text='Привет, Kivy!', font_size=32)
        self.button = Button(text='Нажми меня', size_hint=(1, 0.3), font_size=24)
        self.button.bind(on_press=self.change_text)

        self.add_widget(self.label)
        self.add_widget(self.button)

    def change_text(self, instance):
        self.label.text = 'Кнопка нажата!'

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()