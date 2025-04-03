from datetime import datetime
from typing import List, Optional, Union

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field

load_dotenv()

class Attendees(BaseModel):
    email: Optional[str] = None  # Field(description="email приглашенного участника")


class EventDate(BaseModel):

    dateTime: Optional[Union[str, datetime]] = None  # = Field(description="Дата и время")
    timeZone: Optional[str] = None  # = Field(default="Europe/Moscow", description="Временная зона")

class Overrides(BaseModel):
    method: Optional[str] = None  # = Field(default="email", description="Метод оповещения"),
    minutes: Optional[int] = None  # = Field(default=10, description="За какое время до события оповестить"),

class Reminders(BaseModel):  # Напоминания
    useDefault: Optional[bool] = False  # Field(description="Активно или нет")
    overrides: Optional[List[Overrides]] = None
    forceSendFields: Optional[List[str]] = None

class Creator(BaseModel):
    email: Optional[str] = Field(description="email создателя")
    self: Optional[bool] = True

class Organizer(BaseModel):
    email: Optional[str] = Field(description="email организатора")
    self: Optional[bool] = True


class Event(BaseModel):
    # creator: Optional[Creator] = None  # не работает
    # organizer: Optional[Organizer] = None  # не работает
    summary: Optional[str] = None
    location: Optional[str] = None  # = Field(description="Место события")
    description: Optional[str] = None  # Field(description="Описание события")
    start: Optional[EventDate] = None
    end: Optional[EventDate] = None

    recurrence: Optional[List[str]] = None  # = Field(description="Повторение событий")

    initiator: Optional[str] = None
    attendees: Optional[List[Attendees]] = None
    reminders: Optional[Reminders] = None


class EventAnswer(Event):
    id: str = None
    kind: str = None
    etag: str = None
    status: str = None
    htmlLink: str = None
    created: Optional[Union[str, datetime]] = None
    updated: Optional[Union[str, datetime]] = None
    organizer: Organizer = None
    creator: Creator = None
    iCalUID: str = None
    sequence: int = None
    eventType: str = None


class MiniappAnswer(BaseModel):
    result: bool = False
    status: int = 500
    message: Union[EventAnswer, Event, bool] = False


class MiniappEvent(BaseModel):  # Для записи в базу
    id: Union[str, None] = None
    user_id: int = None
    summary: Optional[Union[str, None]] = ""
    location: Optional[Union[str, None]] = ""
    description: Optional[Union[str]] = ""
    start: Union[str, datetime] = None
    end: Union[str, datetime] = None
    status: Optional[Union[str, None]] = ""
    recurrence: Optional[str] = ""
    initiator: Optional[Union[str, None]] = ""
    attendees: Union[List[str], str] = ""
    manage_type: str = None  # Field(default="", description="Тип создать/изменить")

    # class Config:
    #     from_attributes = True


if __name__ == "__main__":
    pass
