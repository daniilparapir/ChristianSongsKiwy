from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem


KV = '''
<MainScreen>:
    canvas.before:
        Color:
            rgba: app.bg_color
        Rectangle:
            pos: self.pos
            size: self.size

    FloatLayout:
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(12)
            spacing: dp(10)

            MDTopAppBar:
                id: topbar
                title: "Христианский песенник"
                elevation: 0
                md_bg_color: 0.188, 0.188, 0.188, 1
                specific_text_color: app.title_text_color
                right_action_items: [["theme-light-dark", lambda x: app.toggle_theme()]]

            MDTextField:
                id: search
                hint_text: "Поиск песни…"
                mode: "rectangle"
                icon_right: "magnify"
                on_text: app.filter_songs(self.text)
                fill_color: (0.15, 0.15, 0.2, 0.9) if app.is_dark else (0.85, 0.85, 0.85, 0.9)
                text_color: (1, 1, 1, 1) if app.is_dark else (0, 0, 0, 1)
                hint_text_color: 0.7, 0.7, 0.7, 1
                line_color_focus: (1, 1, 1, 1) if app.is_dark else (0, 0, 0, 1)

            ScrollView:
                MDList:
                    id: song_list


<SongScreen>:
    song_title: ""
    lyrics: ""

    canvas.before:
        Color:
            rgba: app.bg_color
        Rectangle:
            pos: self.pos
            size: self.size

    FloatLayout:
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(12)
            spacing: dp(10)

            MDTopAppBar:
                title: root.song_title
                left_action_items: [["arrow-left", lambda x: app.back_to_list()]]
                elevation: 0
                md_bg_color: 0.188, 0.188, 0.188, 1
                specific_text_color: app.title_text_color
                right_action_items: [["theme-light-dark", lambda x: app.toggle_theme()]]

            ScrollView:
                MDLabel:
                    id: lyrics_label
                    text: root.lyrics
                    markup: True
                    halign: "left"
                    color: (1, 1, 1, 1) if app.is_dark else (0, 0, 0, 1)
                    padding: dp(6), dp(6)
                    size_hint_y: None
                    height: self.texture_size[1]
                    font_size: app.current_font_size


ScreenManager:
    id: screen_manager

    MainScreen:
        name: "main"

    SongScreen:
        name: "song"
'''


class MainScreen(MDScreen):
    pass


class SongScreen(MDScreen):
    song_title = StringProperty()
    lyrics = StringProperty()


class HymnalApp(MDApp):
    current_font_size = NumericProperty(18)
    is_dark = True

    title_text_color = ListProperty([1, 1, 1, 1])  # белый по умолчанию
    bg_color = ListProperty([0.188, 0.188, 0.188, 1])   # темный фон по умолчанию

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Dark"

        Builder.load_string(KV)

        self.songs = [
            {
                "number": 1,
                "title": "Твоя милость",
                "lyrics": """Твоя милость превозносится надо мной,
Осеняя, как крылья орла.
И я знаю — среди бури земной
Ты укроешь меня у стола.

[b]Припев:[/b]
Твоя милость… Твоя милость…
Превозносится надо мной!"""
            },
            {
                "number": 2,
                "title": "Наш Бог велик",
                "lyrics": """Свет во тьме сияет,
Наш Бог, Ты так велик!
И каждый пусть познает,
Наш Бог, Ты так велик!

[b]Припев:[/b]
Наш Бог велик — пой со мной:
Наш Бог велик — пусть видит весь народ:
Наш Бог, наш Бог велик!"""
            },
        ]

        self.sm = MDScreenManager()
        self.main_screen = MainScreen(name="main")
        self.song_screen = SongScreen(name="song")
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.song_screen)

        self.populate_song_list()
        Window.bind(on_key_down=self.on_key_down)

        return self.sm

    def populate_song_list(self):
        list_widget = self.main_screen.ids.song_list
        list_widget.clear_widgets()
        for idx, song in enumerate(self.songs):
            item = OneLineListItem(text=f"{song['number']}. {song['title']}")
            item.bind(on_release=lambda inst, i=idx: self.open_song(i))
            list_widget.add_widget(item)

    def filter_songs(self, query):
        query = query.lower()
        list_widget = self.main_screen.ids.song_list
        list_widget.clear_widgets()
        for idx, song in enumerate(self.songs):
            if query in song["title"].lower():
                item = OneLineListItem(text=f"{song['number']}. {song['title']}")
                item.bind(on_release=lambda inst, i=idx: self.open_song(i))
                list_widget.add_widget(item)

    def open_song(self, index):
        song = self.songs[index]
        self.song_screen.song_title = song["title"]
        self.song_screen.lyrics = song["lyrics"]
        self.song_screen.ids.lyrics_label.font_size = self.current_font_size
        self.sm.current = "song"

    def back_to_list(self):
        self.sm.current = "main"

    def toggle_theme(self):
        if self.is_dark:
            self.title_text_color = [0, 0, 0, 1]
            self.bg_color = [1, 1, 1, 1]
            self.theme_cls.theme_style = "Light"
            self.is_dark = False
        else:
            self.title_text_color = [1, 1, 1, 1]
            self.bg_color = [0.188, 0.188, 0.188, 1]
            self.theme_cls.theme_style = "Dark"
            self.is_dark = True
        self.populate_song_list()

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        # volume up = 24, volume down = 25
        if key == 24:
            self.current_font_size = min(self.current_font_size + 2, 40)
            self.update_font_sizes()
            return True
        elif key == 25:
            self.current_font_size = max(self.current_font_size - 2, 12)
            self.update_font_sizes()
            return True
        return False

    def update_font_sizes(self):
        if self.sm.current == "song":
            self.song_screen.ids.lyrics_label.font_size = self.current_font_size


if __name__ == "__main__":
    HymnalApp().run()
