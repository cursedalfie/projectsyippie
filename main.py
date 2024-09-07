import asyncio
import logging
import sys
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import desc
from msgleaderboardcd import UserMessage, session
from datetime import datetime, timezone

TOKEN = "7256855305:AAESKMB1gYdLt3KSGL3UIs1oCiK1FDIeG6U"
dp = Dispatcher()


@dp.message(Command(commands=['leaderboard']))
async def command_start_handler(message: Message) -> None:
    top_users = session.query(UserMessage).order_by(desc(UserMessage.message_count)).limit(3).all()

    leaderboard_text = "Top 3 most messages of all time\n\n"
    for rank, user in enumerate(top_users, start=1):
        leaderboard_text += f"{rank}. {html.bold(user.username or 'Unknown')} - {user.message_count} messages\n"
    await message.answer(leaderboard_text)


@dp.message(Command(commands=['leaderboardweekly']))
async def command_start_handler(message: Message) -> None:
    one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)
    top_users = session.query(UserMessage).filter(UserMessage.last_message_date >= one_week_ago) \
        .order_by(desc(UserMessage.message_count)).limit(3).all()

    leaderboard_text = "Top 3 most messages of the week\n\n"
    for rank, user in enumerate(top_users, start=1):
        leaderboard_text += f"{rank}. {html.bold(user.username or 'Unknown')} - {user.message_count} messages\n"
    await message.answer(leaderboard_text)


@dp.message()
async def echo_handler(message: Message) -> None:
    username = message.from_user.username
    user_id = message.from_user.id
    current_message = session.query(UserMessage).filter_by(user_id=user_id).first()
    if current_message is None:
        top_msg = UserMessage(user_id=user_id, username=username, message_count=1,
                              last_message_date=datetime.now(timezone.utc))
        session.add(top_msg)
        session.commit()
    else:
        current_message.message_count += 1
        current_message.last_message_date = datetime.now(timezone.utc)
        session.add(current_message)
        session.commit()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
