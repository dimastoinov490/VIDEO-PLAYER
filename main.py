import os
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform

# Тёмная тема окна
Window.clearcolor = (0.05, 0.05, 0.07, 1)

class HyperVideoPlayer(App):
    def build(self):
        self.title = "Hyper Player"
        
        # Главный контейнер
        self.root_layout = FloatLayout()

        # Виджет видео (FFmpeg / ffpyplayer)
        self.video = VideoPlayer(
            options={'allow_stretch': True, 'eos': 'stop'},
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        # Отключаем стандартную старую панель Kivy
        self.video.use_system_control = False
        self.root_layout.add_widget(self.video)

        # Кастомная капельная панель управления (HyperOS / VLC Style)
        self.controls = BoxLayout(
            orientation='vertical',
            size_hint=(0.94, None),
            height=110,
            pos_hint={'center_x': 0.5, 'y': 0.03},
            padding=[15, 10],
            spacing=5
        )
        
        # Ползунок прогресса (Timeline)
        self.timeline = Slider(min=0, max=100, value=0, size_hint_y=None, height=30)
        self.timeline.bind(on_touch_up=self.on_seek)
        self.controls.add_widget(self.timeline)

        # Ряд кнопок
        btn_row = BoxLayout(orientation='horizontal', spacing=12)

        self.btn_open = Button(
            text="📁",
            font_size='20sp',
            size_hint=(None, None),
            size=(50, 50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 0.8)
        )
        self.btn_open.bind(on_press=self.open_file_picker)

        self.btn_rewind = Button(
            text="≪ 10s",
            font_size='14sp',
            size_hint=(None, None),
            size=(70, 50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 0.8)
        )
        self.btn_rewind.bind(on_press=lambda x: self.seek_relative(-10))

        self.btn_play = Button(
            text="►",
            font_size='22sp',
            size_hint=(None, None),
            size=(60, 50),
            background_normal='',
            background_color=(0.12, 0.52, 0.95, 0.9)
        )
        self.btn_play.bind(on_press=self.toggle_play)

        self.btn_forward = Button(
            text="10s ≫",
            font_size='14sp',
            size_hint=(None, None),
            size=(70, 50),
            background_normal='',
            background_color=(0.15, 0.15, 0.2, 0.8)
        )
        self.btn_forward.bind(on_press=lambda x: self.seek_relative(10))

        self.lbl_status = Label(
            text="Выберите файл",
            font_size='13sp',
            color=(0.8, 0.8, 0.8, 1),
            halign='right'
        )

        btn_row.add_widget(self.btn_open)
        btn_row.add_widget(self.btn_rewind)
        btn_row.add_widget(self.btn_play)
        btn_row.add_widget(btn_forward)
        btn_row.add_widget(self.lbl_status)

        self.controls.add_widget(btn_row)
        self.root_layout.add_widget(self.controls)

        # Таймер обновления Timeline
        Clock.schedule_interval(self.update_timeline, 0.5)

        return self.root_layout

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_VIDEO
            ])

    def open_file_picker(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        start_path = '/sdcard/Download' if os.path.exists('/sdcard/Download') else '/sdcard'

        self.filechooser = FileChooserIconView(
            path=start_path,
            filters=['*.mp4', '*.mkv', '*.avi', '*.mov', '*.webm', '*.flv', '*.ts', '*.3gp']
        )
        content.add_widget(self.filechooser)

        btn_layout = BoxLayout(size_hint_y=None, height=45, spacing=10)
        btn_open = Button(text='Воспроизвести', background_normal='', background_color=(0.12, 0.6, 0.3, 1))
        btn_cancel = Button(text='Отмена', background_normal='', background_color=(0.7, 0.2, 0.2, 1))

        btn_layout.add_widget(btn_open)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        self.popup = Popup(
            title="Выбор видео (Все форматы)",
            content=content,
            size_hint=(0.95, 0.95)
        )

        btn_open.bind(on_press=self.load_selected_video)
        btn_cancel.bind(on_press=lambda x: self.popup.dismiss())
        self.popup.open()

    def load_selected_video(self, instance):
        if self.filechooser.selection:
            video_path = self.filechooser.selection[0]
            self.popup.dismiss()
            
            if os.path.exists(video_path):
                self.video.source = video_path
                self.video.state = 'play'
                self.btn_play.text = "❚❚"
                self.lbl_status.text = os.path.basename(video_path)[:18] + "..."
            else:
                self.lbl_status.text = "Ошибка файла"

    def toggle_play(self, instance):
        if not self.video.source:
            self.open_file_picker(None)
            return

        if self.video.state == 'play':
            self.video.state = 'pause'
            self.btn_play.text = "►"
        else:
            self.video.state = 'play'
            self.btn_play.text = "❚❚"

    def seek_relative(self, seconds):
        if self.video.duration > 0:
            target = max(0, min(self.video.duration, self.video.position + seconds))
            self.video.seek(target / self.video.duration)

    def on_seek(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.video.duration > 0:
            self.video.seek(self.timeline.value_pct)

    def update_timeline(self, dt):
        if self.video.duration > 0:
            self.timeline.max = self.video.duration
            self.timeline.value = self.video.position

if __name__ == '__main__':
    HyperVideoPlayer().run()
