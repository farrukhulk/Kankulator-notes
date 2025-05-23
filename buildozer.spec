[app]
title = Ultimate Notes
package.name = ultinotes
package.domain = org.example
source.dir = .
source.include_exts = py,txt
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = armeabi-v7a

[android.logcat]
filters = *:S python:D