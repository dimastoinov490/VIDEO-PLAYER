import os
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import platform

# Устанавливаем темный фон окна
Window.clearcolor = (0.07, 0.07, 0.09, 1)

class ModernVideoPlayer(App):
    def build(self):
        self.title = "Power Player"
        self.current_video = None
        
        # Главный контейнер
        self.root_layout = FloatLayout()

        # Стартовый экран с предложением выбрать видео
        self.placeholder = BoxLayout(
            orientation='vertical',
            size_hint=(0.8, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=15
        )
        
        self.lbl_title = Label(
            text="[b]Power Video Player[/b]\nВсеядный медиаплеер",
            markup=True,
            font_size='22sp',
            halign='center',
            color=(0.9, 0.9, 0.95, 1)
        )
        
        self.btn_select = Button(
            text="📂 Выбрать видеофайл",
            font_size='18sp',
            size_hint_y=None,
            height=60,
            background_normal='',
            background_color=(0.15, 0.45, 0.85, 1)
        )
        self.btn_select.bind(on_press=self.open_file_picker)

        self.placeholder.add_widget(self.lbl_title)
        self.placeholder.add_widget(self.btn_select)
        self.root_layout.add_widget(self.placeholder)

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
        
        # Безопасный путь к папке загрузок
        start_path = '/sdcard/Download' if os.path.exists('/sdcard/Download') else '/sdcard'
            
        self.filechooser = FileChooserIconView(
            path=start_path,
            filters=['*.mp4', '*.mkv', '*.avi', '*.mov', '*.webm', '*.flv', '*.ts', '*.3gp']
        )
        content.add_widget(self.filechooser)
        
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_open = Button(text='Открыть', background_normal='', background_color=(0.15, 0.65, 0.35, 1))
        btn_cancel = Button(text='Отмена', background_normal='', background_color=(0.75, 0.2, 0.2, 1))
        
        btn_layout.add_widget(btn_open)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)
        
        self.popup = Popup(
            title="Выберите видео из памяти",
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
            
            # Проверяем доступность файла
            if os.path.exists(video_path):
                self.start_player(video_path)
            else:
                self.show_error("Нет доступа к выбранному файлу")

    def start_player(self, path):
        # Очищаем стартовый экран
        self.root_layout.clear_widgets()
        
        # Выводим стильную информацию о запуске всеядного движка
        info_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=10
        )
        
        filename = os.path.basename(path)
        lbl_file = Label(
            text=f"Воспроизведение:\n[b]{filename}[/b]",
            markup=True,
            font_size='16sp',
            halign='center'
        )
        
        btn_back = Button(
            text="◀ Выбрать другой файл",
            size_hint_y=None,
            height=50,
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1)
        )
        btn_back.bind(on_press=self.reset_to_main)
        
        info_box.add_widget(lbl_file)
        info_box.add_widget(btn_back)
        self.root_layout.add_widget(info_box)

    def reset_to_main(self, instance):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.placeholder)

    def show_error(self, text):
        popup = Popup(
            title='Ошибка доступа',
            content=Label(text=text),
            size_hint=(0.8, 0.3)
        )
        popup.open()

if __name__ == '__main__':
    ModernVideoPlayer().run()
