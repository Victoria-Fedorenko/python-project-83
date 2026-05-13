import multiprocessing
import os

# Привязка к порту (Render передает PORT)
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# Количество рабочих процессов
workers = (multiprocessing.cpu_count() * 2) + 1

# КЛЮЧЕВОЙ ПАРАМЕТР для решения SSL проблемы
preload_app = True

# Таймаут
timeout = 120

# Файлы логов
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Модуль с приложением Flask
# Указываем путь: page_analyzer.app - значит файл app.py в папке page_analyzer
# :app - означает переменную app внутри этого файла
module = "page_analyzer.app:app"