[app]

# (str) Title of your application
title = SteganoScan Sentinel

# (str) Package name
package.name = steganoscan

# (str) Package domain (needed for android/ios packaging)
package.domain = org.cyberwarlab

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,opencv-python-headless,numpy,scipy,pyjnius,watchdog

# (str) Custom source folders for requirements
# packagelist.include_patterns = 

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, POST_NOTIFICATIONS, FOREGROUND_SERVICE

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) Use --private data storage (True) or shared storage (False)
android.private_storage = True

# (list) Services to create
# Each service is a line with name:object
# e.g. services = monitor:service.py
services = SentinelService:service.py

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (list) Supported orientations
# Valid values are: landscape, portrait, portrait-upside-down, all
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_PY

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

# (str) Path to build artifact storage, can be absolute or relative
# build_dir = ./.buildozer

# (str) Path to bin directory
# bin_dir = ./bin
