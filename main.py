# main.py — Христианский песенник (песни прямо в коде)
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget


# ----------- KV-разметка интерфейса
KV = '''
<GradientBg@Widget>:
    canvas.before:
        Color:
            rgba: (0.12, 0.14, 0.36, 1)  # тёмно-фиолетовый
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: (0.12, 0.14, 0.36, 1)  # светло-фиолетовый
        Rectangle:
            pos: self.x, self.y + self.height / 2
            size: self.width, self.height / 2

<MainScreen>:
    name: "main"
    FloatLayout:
        GradientBg:
            pos: self.pos
            size: self.size

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(12)
            spacing: dp(10)
            size_hint: 1, 1

            MDTopAppBar:
                title: "Христианский песенник"
                elevation: 8
                md_bg_color: 0, 0, 0, 0  # прозрачный
                specific_text_color: 1, 1, 1, 1  # белый текст

            MDTextField:
                id: search_field
                hint_text: "Поиск песни…"
                mode: "rectangle"
                icon_right: "magnify"
                on_text: app.filter_songs(self.text)
                fill_color: 0.2, 0.2, 0.2, 1  # тёмное поле
                text_color: 1, 1, 1, 1
                hint_text_color: 0.7, 0.7, 0.7, 1
                line_color_focus: 1, 1, 1, 1

            ScrollView:
                MDList:
                    id: song_list


<SongScreen>:
    name: "song"
    song_title: ""
    lyrics: ""
    FloatLayout:
        GradientBg:
            pos: self.pos
            size: self.size

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(12)
            spacing: dp(10)
            size_hint: 1, 1

            MDTopAppBar:
                title: root.song_title
                left_action_items: [["arrow-left", lambda x: app.back_to_list()]]
                elevation: 8
                md_bg_color: 0, 0, 0, 0
                specific_text_color: 1, 1, 1, 1

            ScrollView:
                MDLabel:
                    id: lyrics_label
                    text: root.lyrics
                    markup: True
                    font_style: "Body1"
                    halign: "left"
                    color: 1, 1, 1, 1
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

        Builder.load_string(KV)

        self.songs = [
            {
                "number": 1,
                "title": "О Молитва, О Молитва",
                "lyrics": """О молитва, о молитва Песнь Возрождения

1 куплет:  
  Am                            Dm
О молитва, о молитва!
                  Am           E7    Am
В жизни Богом ты дана.
    Am                                    Dm
В скорбной жизни среди битвы
           Am         E7      Am   A7
Поднимала ты меня.
                 Dm                  G
Темной ночью я не спал,
               C             F
На коленях все стоял
               Dm      E             Am  A7
И душою с Богом говорил:
               Dm                      G
"Ты услышь меня, мой Бог,
               C                    F
Среди жизненных тревог
             Dm           E            Am
Помоги, я выбился из сил!"

2 куплет:  
За окном бушует ветер,
Хлещет снегом ледяным
И такой же бурей в сердце
В этот вечер я томим.
Но, смирившийся во прах,
Со слезами на очах
Я в скорбях Иисуса умолял:
"О мой Бог! Ты знаешь все,
На душе так тяжело,
Я измучен и почти упал".

3 куплет:  
Боже мой, я жизни легкой
И беспечной не хочу,
Пусть страдания и скорби
На пути своем найду.
Об одном прошу лишь я,
Чтоб я чувствовал всегда,
Как Твоя всесильная рука
На плечах лежит моих
И среди житейских битв
Ободряет ласково меня.

4 куплет:  
О молитва, о молитва!
Благодарностью горю,
Прославляю Божью силу,
Благодати глубину.
Боже! Ты в любви святой
Укреплял дух слабый мой,
Когда в бурю падал я без сил.
К небесам сердечный вздох
Возносился средь тревог,
Я в молитве радость получал.
"""
            },
            {
                "number": 2,
                "title": "За любовь за милость",
                "lyrics": """За любовь, за милость, за спасение Песнь Возрождения

1 куплет:  
Am                   Dm
За любовь, за милость, за спасение,
 E7                                                Am   E7
Благодарность Ты прими от нас.
 Am                Dm
Пусть несется песнь благодарения
 E7                                               Am
Господу - Он кровию нас спас.

Припев:  
  Am          Dm7       G7            C-E7
Благодарим, благодарим, за Твою любовь благодарим!
 Am         Dm7          E7            Am
Достоин Ты вечной хвалы, за Твою любовь благодарим!

2 куплет:  
За Твои Голгофские страдания,
За спасенье, данное Тобой,
И за все Твои благодеяния
Сердце для Тебя звучит хвалой!

3 куплет:  
За прекрасный дом в лазурном небе,
За святую вечность без конца
Пусть звучит сегодня гимн хваления,
Эту песнь поют наши сердца.
"""
            },
            {
                "number": 3,
                "title": "Господь — моя скала",
                "lyrics": """Господь — моя скала и прибежище,  
Моя защита и сила в беде.  
Я уповаю на имя Его —  
Он не оставит меня никогда!"""
            },
        ]

        self.sm = MDScreenManager()
        self.main_screen = MainScreen()
        self.song_screen = SongScreen()
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.song_screen)

        self.populate_song_list()
        return self.sm

    # Создание кнопки песни
    def make_song_button(self, index, title):
        item = OneLineAvatarListItem(text=title)
        item.add_widget(ImageLeftWidget(source="atlas://data/images/defaulttheme/audio-volume-high"))
        item.bind(on_release=lambda instance: self.open_song(index))
        return item

    # Показ всех песен
    def populate_song_list(self):
        song_list = self.main_screen.ids.song_list
        song_list.clear_widgets()
        for idx, song in enumerate(self.songs):
            item = self.make_song_button(idx, f"{song['number']}. {song['title']}")
            song_list.add_widget(item)

    # Поиск
    def filter_songs(self, query):
        query = query.lower()
        song_list = self.main_screen.ids.song_list
        song_list.clear_widgets()
        for idx, song in enumerate(self.songs):
            if query in song["title"].lower():
                item = self.make_song_button(idx, f"{song['number']}. {song['title']}")
                song_list.add_widget(item)

    # Открытие песни
    def open_song(self, index):
        song = self.songs[index]
        self.song_screen.song_title = song["title"]
        self.song_screen.lyrics = song["lyrics"]
        self.sm.current = "song"

    # Назад
    def back_to_list(self):
        self.sm.current = "main"


if __name__ == "__main__":
    HymnalApp().run()
