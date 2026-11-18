from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str

class Survey(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    course_year: str
    preferred_study_time: str
    learning_mode: str
    daily_study_hours: float
    favorite_tool: str
    stress_level: int