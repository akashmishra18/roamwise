from datetime import date, datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field, model_validator

class Preferences(BaseModel):
    destination: str = Field(min_length=2, max_length=120)
    start_date: date
    end_date: date
    budget: float = Field(ge=50, le=1000000, allow_inf_nan=False)
    currency: Literal['USD', 'EUR', 'GBP', 'INR', 'JPY'] = 'USD'
    group_size: int = Field(ge=1, le=20)
    style: Literal['Relaxed', 'Balanced', 'Adventure', 'Luxury']
    interests: list[str] = Field(min_length=1, max_length=8)
    notes: str = Field(default='', max_length=1000)

    @model_validator(mode='after')
    def dates(self):
        if not 1 <= self.day_count <= 14:
            raise ValueError('Trips must last 1 to 14 days')
        allowed = {'Culture', 'Food', 'Nature', 'Adventure', 'Art', 'Shopping', 'Romance', 'Wellness'}
        if not set(self.interests) <= allowed:
            raise ValueError('Unsupported interest')
        return self

    @property
    def day_count(self):
        return (self.end_date - self.start_date).days + 1

class Activity(BaseModel):
    time: str = Field(pattern=r'^([01]\d|2[0-3]):[0-5]\d$')
    title: str = Field(min_length=1, max_length=180)
    category: Literal['Dining', 'Attraction', 'Transport', 'Experience']
    description: str = Field(min_length=1, max_length=1500)
    duration: int = Field(ge=1, le=720)
    cost: float = Field(ge=0, le=1000000, allow_inf_nan=False)
    location: str = Field(min_length=1, max_length=300)

class Accommodation(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    cost: float = Field(ge=0, le=1000000, allow_inf_nan=False)

class Transport(BaseModel):
    description: str = Field(min_length=1, max_length=1000)
    cost: float = Field(ge=0, le=1000000, allow_inf_nan=False)

class Day(BaseModel):
    day: int = Field(ge=1, le=14)
    title: str = Field(min_length=1, max_length=180)
    activities: list[Activity] = Field(min_length=1, max_length=10)
    accommodation: Accommodation
    transport: Transport

    @model_validator(mode='after')
    def scheduling(self):
        previous_end = 0
        for activity in self.activities:
            hour, minute = map(int, activity.time.split(':'))
            start = hour * 60 + minute
            if start < previous_end or start + activity.duration > 1440:
                raise ValueError('Activities overlap or extend past midnight')
            previous_end = start + activity.duration
        return self

class Plan(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    summary: str = Field(min_length=1, max_length=1500)
    source: Literal['ai', 'demo'] = 'ai'
    days: list[Day] = Field(min_length=1, max_length=14)

class Trip(Plan):
    id: UUID
    preferences: Preferences
    created_at: datetime
    favorite: bool = False

    @model_validator(mode='after')
    def consistent_days(self):
        if [d.day for d in self.days] != list(range(1, self.preferences.day_count + 1)):
            raise ValueError('Trip days must match the requested dates')
        return self

class RegenerateRequest(BaseModel):
    preferences: Preferences
    day: int = Field(ge=1, le=14)
    current_day: Day

    @model_validator(mode='after')
    def valid_day(self):
        if self.day > self.preferences.day_count or self.current_day.day != self.day:
            raise ValueError('Day must match an existing trip day')
        return self
