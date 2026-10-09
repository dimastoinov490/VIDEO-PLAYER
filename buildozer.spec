[app]
title = VideoPlayer
package.name = videoplayer
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Библиотеки: ffpyplayer подтягивает все видео/аудио кодеки FFmpeg
requirements = python3,kivy,ffpyplayer

orientation = portrait
fullscreen = 0

# Разрешения Android для доступа к памяти и видеофайлам
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
