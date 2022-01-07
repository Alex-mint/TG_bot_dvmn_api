# Devman Bot

Бот отправляет уведомления о проверке работ на курсе [Девман](https://dvmn.org/modules/)

### Как установить

- Python3 должен быть уже установлен.
- Склонируйте репозиторий на свой компьютер.
```commandline
git clone https://github.com/Alex-mint/DMN_TG_bot.git
```  
- Установите зависимости:
```commandline
pip install -r requirements.txt
```

### Переменные окружения

Создайте файл .env в корневой папке с кодом и запишите туда:
```python
DVMN_TOKEN=Твой_токен_на_девмане
TG_TOKEN=Телеграм_токен
CHAT_ID=Твой_телеграм_chat_id
```
### Запуск

Для запуска программы необходимо написать в терминале следующее:
```commandline
python3 manage.py bot
```
