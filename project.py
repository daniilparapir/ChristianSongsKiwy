# main.py — Христианский песенник на KivyMD
import json
from pathlib import Path
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget


# ----------- Данные песен (создаётся songs.json при первом запуске)
DEFAULT_SONGS = [
    {
        "number": 1,
        "title": "Твоя милость",
        "lyrics": """
1. Твоя милость превозносится надо мной,  
   Осеняя, как крылья орла.  
   И я знаю — среди бури земной  
   Ты укроешь меня у стола.

Припев:  
   Твоя милость…   Твоя милость…  
   Превозносится надо мной!
"""
    },
    {
        "number": 2,
        "title": "Наш Бог велик",
        "lyrics": """
1. Свет во тьме сияет,  
   Наш Бог, Ты так велик!  
   И каждый пусть познает,  
   Наш Бог, Ты так велик!

Припев:  
   Наш Бог велик — пой со мной:  
   Наш Бог велик — пусть видит весь народ:  
   Наш Бог, наш Бог велик!
"""
    },
]

SONG_FILE = Path("songs.json")
if not SONG_FILE.exists():
    SONG_FILE.write_text(json.dumps(DEFAULT_SONGS, ensure_ascii=False, indent=2), encoding="utf-8")

# ----------- KV-разметка интерфейса
KV = '''
<GradientBg@Widget>:
    canvas.before:
        Color:
            rgba: (0.12, 0.14, 0.36, 1)
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: (0.40, 0.45, 0.80, 1)
        Rectangle:
            pos: self.x, self.y + self.height/2
            size: self.width, self.height/2

<MainScreen>:
    name: "main"
    GradientBg:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)

        MDTopAppBar:
            title: "Христианский песенник"
            elevation: 8
            md_bg_color: 0,0,0,0
            specific_text_color: 1,1,1,1

        MDTextField:
            id: search_field
            hint_text: "Поиск песни…"
            mode: "rectangle"
            icon_right: "magnify"
            on_text: app.filter_songs(self.text)

        ScrollView:
            MDList:
                id: song_list

<SongScreen>:
    name: "song"
    song_title: ""
    lyrics: ""
    GradientBg:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)

        MDTopAppBar:
            title: root.song_title
            left_action_items: [["arrow-left", lambda x: app.back_to_list()]]
            elevation: 8
            md_bg_color: 0,0,0,0
            specific_text_color: 1,1,1,1

        ScrollView:
            MDLabel:
                id: lyrics_label
                text: root.lyrics
                markup: True
                font_style: "Body1"
                halign: "left"
                padding: dp(6), dp(6)
                size_hint_y: None
                height: self.texture_size[1]
'''

# ----------- Экраны
class MainScreen(MDScreen):
    pass

class SongScreen(MDScreen):
    song_title = StringProperty()
    lyrics = StringProperty()


# ----------- Приложение
class HymnalApp(MDApp):
    def build(self):
        self.icon = "atlas://data/images/defaulttheme/audio-volume-high"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Dark"

        self.songs = json.loads(SONG_FILE.read_text(encoding="utf-8"))
        Builder.load_string(KV)

        self.sm = MDScreenManager()
        self.main_screen = MainScreen()
        self.song_screen = SongScreen()
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.song_screen)

        self.populate_song_list()
        return self.sm

    # Создание кнопки для списка песен
    def make_song_button(self, index, title):
        item = OneLineAvatarListItem(text=title)
        item.add_widget(ImageLeftWidget(source="atlas://data/images/defaulttheme/audio-volume-high"))
        item.bind(on_release=lambda instance: self.open_song(index))
        return item

    # Список всех песен
    def populate_song_list(self):
        song_list = self.main_screen.ids.song_list
        song_list.clear_widgets()
        for idx, song in enumerate(self.songs):
            item = self.make_song_button(idx, f"{song['number']}. {song['title']}")
            song_list.add_widget(item)

    # Фильтр песен
    def filter_songs(self, query):
        query = query.lower()
        song_list = self.main_screen.ids.song_list
        song_list.clear_widgets()
        for idx, song in enumerate(self.songs):
            if query in song["title"].lower():
                item = self.make_song_button(idx, f"{song['number']}. {song['title']}")
                song_list.add_widget(item)

    # Показать выбранную песню
    def open_song(self, index):
        song = self.songs[index]
        self.song_screen.song_title = song["title"]
        self.song_screen.lyrics = song["lyrics"]
        self.sm.current = "song"

    # Вернуться к списку
    def back_to_list(self):
        self.sm.current = "main"


if __name__ == "__main__":
    HymnalApp().run()