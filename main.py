import os
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.videoplayer import VideoPlayer
from kivy.utils import platform

class PowerVideoPlayerApp(App):
    def build(self):
        # Главный контейнер
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Плеер на базе ffpyplayer (FFmpeg)
        self.player = VideoPlayer(options={'allow_stretch': True})
        self.player.state = 'stop'
        self.main_layout.add_widget(self.player)
        
        # Панель управления
        controls = BoxLayout(size_hint_y=None, height=50)
        btn_open = Button(
            text='Открыть файл',
            background_color=(0.2, 0.6, 1, 1)
        )
        btn_open.bind(on_press=self.open_file_dialog)
        controls.add_widget(btn_open)
        
        self.main_layout.add_widget(controls)
        return self.main_layout

    def on_start(self):
        # Запрос разрешений при запуске на Android
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_VIDEO
            ])

    def open_file_dialog(self, instance):
        content = BoxLayout(orientation='vertical')
        
        # Корневой каталог памяти Android
        start_path = '/sdcard' if os.path.exists('/sdcard') else '.'
        filechooser = FileChooserIconView(path=start_path)
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=None, height=45)
        btn_select = Button(text='Воспроизвести', background_color=(0.1, 0.8, 0.3, 1))
        btn_cancel = Button(text='Отмена', background_color=(0.9, 0.2, 0.2, 1))
        
        btn_layout.add_widget(btn_select)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title="Выберите видеофайл",
            content=content,
            size_hint=(0.95, 0.95)
        )
        
        def select_file(btn_instance):
            if filechooser.selection:
                filepath = filechooser.selection[0]
                self.play_video(filepath)
                popup.dismiss()
                
        btn_select.bind(on_press=select_file)
        btn_cancel.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def play_video(self, filepath):
        self.player.state = 'stop'
        self.player.source = filepath
        self.player.state = 'play'

if __name__ == '__main__':
    PowerVideoPlayerApp().run()
