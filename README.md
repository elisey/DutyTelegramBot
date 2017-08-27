# DutyTelegramBot

## Настройка
Создать файл с настройками
```
cp connectTeamBot.config.example connectTeamBot.config
vi connectTeamBot.config
```
Убедиться что создан файл для хранеия текущего имени. При необходимости создать
```
touch duty_name.txt
```

## Запуск
```
python2 connectTeamBot.py
```

## Управление
Установить новое имя дежурного
```
/set_duty НовоеИмя
```

## Зависимости 
 * configparser
 * python-telegram-bot
