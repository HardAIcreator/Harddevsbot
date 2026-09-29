# HardDEV Telegram-бот

Визитка канала начинающего инди-девелопера.
Обложка — файл `cover.png`. ЛС автора: [@the_harddev](https://t.me/the_harddev)

## Что умеет

- `/start` — обложка и меню
- О канале
- Стек: JavaScript, Python, GDScript, Godot, Firebase, Render, GitHub, BotFather
- Проекты
- Подробности
- FAQ
- Об авторе
- Кнопка «Написать в ЛС»
- Выдача основного канала только через ЛС

## Как запустить

1. Открой [@BotFather](https://t.me/BotFather)
2. `/newbot` — придумай имя, например `HardDEV Guide`
3. Скопируй токен
4. Скопируй `.env.example` в `.env` и вставь токен:

```
BOT_TOKEN=123456:ABC...
```

5. Установи зависимости и запусти:

```bash
pip install -r requirements.txt
python bot.py
```

6. В BotFather можно поставить ту же картинку `cover.png` как аватар бота:
   `/setuserpic`

Чтобы бот работал всегда, потом выложи его на Render.
