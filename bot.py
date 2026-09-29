import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_USERNAME = "the_harddev"
ADMIN_URL = f"https://t.me/{ADMIN_USERNAME}"
COVER_PATH = Path(__file__).parent / "cover.png"

if not TOKEN:
    raise SystemExit("Укажи BOT_TOKEN в файле .env")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📺 О канале", callback_data="about"),
                InlineKeyboardButton(text="🧰 Стек", callback_data="stack"),
            ],
            [
                InlineKeyboardButton(text="🎮 Проекты", callback_data="projects"),
                InlineKeyboardButton(text="📋 Подробности", callback_data="details"),
            ],
            [
                InlineKeyboardButton(text="👤 Об авторе", callback_data="author"),
                InlineKeyboardButton(text="❓ FAQ", callback_data="faq"),
            ],
            [InlineKeyboardButton(text="🔗 Получить канал", callback_data="get_channel")],
            [InlineKeyboardButton(text="✉️ Написать в ЛС", url=ADMIN_URL)],
        ]
    )


def back_menu(*extra_rows: list[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    rows = list(extra_rows)
    rows.append(
        [
            InlineKeyboardButton(text="🏠 Меню", callback_data="menu"),
            InlineKeyboardButton(text="✉️ ЛС", url=ADMIN_URL),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


WELCOME_CAPTION = (
    "<b>HARDDEV</b>\n"
    "канал начинающего инди-девелопера\n\n"
    "Здесь живут игры, боты и небольшие эксперименты.\n"
    "Выбери раздел ниже — или сразу напиши в ЛС."
)

TEXTS = {
    "about": (
        "<b>О канале HardDEV</b>\n\n"
        "Это личный канал начинающего инди-девелопера.\n"
        "В основном канале публикуются проекты, обновления, сборки и заметки по разработке.\n\n"
        "Не курс и не огромное комьюнити — дневник человека, который сам собирает игры и ботов.\n\n"
        "Чтобы попасть в основной канал, напиши в ЛС: @{admin}"
    ),
    "stack": (
        "<b>Стек канала</b>\n\n"
        "<b>Языки</b>\n"
        "• JavaScript\n"
        "• Python\n"
        "• GDScript\n\n"
        "<b>Игровой движок</b>\n"
        "• Godot\n\n"
        "<b>Хостинги и код</b>\n"
        "• GitHub — хранение проектов\n"
        "• Firebase — онлайн-сервисы и база\n"
        "• Render — запуск сайтов, серверов и ботов\n\n"
        "<b>Telegram</b>\n"
        "• боты через BotFather"
    ),
    "projects": (
        "<b>Что обычно выходит в канале</b>\n\n"
        "• игры на Godot\n"
        "• веб-проекты и эксперименты\n"
        "• Telegram-боты\n"
        "• обновления, правки и новые идеи\n\n"
        "Список живых проектов лучше спрашивать в ЛС — туда скидывают актуальную ссылку на канал и свежие сборки."
    ),
    "details": (
        "<b>Подробности</b>\n\n"
        "HardDEV — закрытый канал. Ссылка не висит в открытом доступе специально.\n\n"
        "<b>Как это устроено</b>\n"
        "1. Пишешь @{admin}\n"
        "2. Получаешь ссылку на основной канал\n"
        "3. Смотришь проекты и обновления\n\n"
        "Если хочешь задать вопрос по Godot, ботам, GitHub, Firebase или Render — тоже пиши в ЛС."
    ),
    "author": (
        "<b>Автор</b>\n\n"
        "Ник: <b>HARD</b>\n"
        "ЛС: @{admin}\n\n"
        "Начинающий инди-девелопер.\n"
        "Делает игры на Godot, пишет ботов и собирает небольшие проекты на JS и Python.\n\n"
        "Канал — про процесс, а не про «готовые миллионы скачиваний»."
    ),
    "faq": (
        "<b>Частые вопросы</b>\n\n"
        "<b>Это публичный канал?</b>\n"
        "Нет, основной канал закрытый.\n\n"
        "<b>Как получить ссылку?</b>\n"
        "Написать @{admin}\n\n"
        "<b>Тут учат с нуля?</b>\n"
        "Нет. Это канал проектов, не школа.\n\n"
        "<b>Можно кинуть свой проект?</b>\n"
        "Сначала напиши в ЛС.\n\n"
        "<b>Боты и игры бесплатные?</b>\n"
        "Смотри актуальные посты в основном канале."
    ),
    "get_channel": (
        "<b>Ссылка на основной канал</b>\n\n"
        "Её выдаёт только автор.\n"
        "Напиши в личные сообщения: @{admin}\n\n"
        "Коротко напиши, что хочешь ссылку на HardDEV — и всё."
    ),
    "help": (
        "<b>Команды бота</b>\n\n"
        "/start — обложка и главное меню\n"
        "/menu — меню без обложки\n"
        "/about — о канале\n"
        "/stack — языки и сервисы\n"
        "/projects — проекты\n"
        "/details — подробности\n"
        "/author — об авторе\n"
        "/faq — вопросы\n"
        "/channel — как получить канал\n"
        "/ls — ссылка на личные сообщения\n"
        "/help — эта справка"
    ),
}


def fill(key: str) -> str:
    return TEXTS[key].format(admin=ADMIN_USERNAME)


async def send_cover(message: Message) -> None:
    if COVER_PATH.exists():
        await message.answer_photo(
            photo=FSInputFile(COVER_PATH),
            caption=WELCOME_CAPTION,
            reply_markup=main_menu(),
        )
    else:
        await message.answer(WELCOME_CAPTION, reply_markup=main_menu())


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await send_cover(message)


@dp.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer("<b>Меню HardDEV</b>\nВыбери раздел:", reply_markup=main_menu())


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(fill("help"), reply_markup=back_menu())


@dp.message(Command("about"))
async def cmd_about(message: Message) -> None:
    await message.answer(fill("about"), reply_markup=back_menu())


@dp.message(Command("stack"))
async def cmd_stack(message: Message) -> None:
    await message.answer(fill("stack"), reply_markup=back_menu())


@dp.message(Command("projects"))
async def cmd_projects(message: Message) -> None:
    await message.answer(fill("projects"), reply_markup=back_menu())


@dp.message(Command("details"))
async def cmd_details(message: Message) -> None:
    await message.answer(fill("details"), reply_markup=back_menu())


@dp.message(Command("author"))
async def cmd_author(message: Message) -> None:
    await message.answer(fill("author"), reply_markup=back_menu())


@dp.message(Command("faq"))
async def cmd_faq(message: Message) -> None:
    await message.answer(fill("faq"), reply_markup=back_menu())


@dp.message(Command("channel"))
async def cmd_channel(message: Message) -> None:
    await message.answer(
        fill("get_channel"),
        reply_markup=back_menu(
            [InlineKeyboardButton(text="✉️ Открыть ЛС", url=ADMIN_URL)]
        ),
    )


@dp.message(Command("ls"))
async def cmd_ls(message: Message) -> None:
    await message.answer(
        f"<b>Личные сообщения</b>\n\nАвтор: @{ADMIN_USERNAME}\nЖми кнопку ниже.",
        reply_markup=back_menu(
            [InlineKeyboardButton(text="✉️ Написать @the_harddev", url=ADMIN_URL)]
        ),
    )


@dp.callback_query(F.data == "menu")
async def cb_menu(call: CallbackQuery) -> None:
    await call.message.answer("<b>Меню HardDEV</b>\nВыбери раздел:", reply_markup=main_menu())
    await call.answer()


@dp.callback_query(F.data.in_(TEXTS.keys()))
async def cb_sections(call: CallbackQuery) -> None:
    key = call.data or "about"
    markup = back_menu()
    if key in {"get_channel", "details"}:
        markup = back_menu(
            [InlineKeyboardButton(text="✉️ Написать @the_harddev", url=ADMIN_URL)]
        )
    await call.message.answer(fill(key), reply_markup=markup)
    await call.answer()


@dp.message()
async def fallback(message: Message) -> None:
    await message.answer(
        "Я бот-визитка канала <b>HardDEV</b>.\n"
        "Нажми кнопку меню или напиши /start",
        reply_markup=main_menu(),
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
