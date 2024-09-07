from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

Base = declarative_base()


class UserMessage(Base):
    __tablename__ = 'user_messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    message_count = Column(Integer, default=0)
    last_message_date = Column(DateTime, default=datetime.now(timezone.utc))
    chat_id = Column(Integer, nullable=False)

engine = create_engine('sqlite:///leaderboard.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
