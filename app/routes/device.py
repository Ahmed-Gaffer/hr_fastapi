from sqlmodel import SQLModel, Field

class Employee(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    salary: float

from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///employees.db")

SQLModel.metadata.create_all(engine)

from sqlmodel import Session

new_emp = Employee(name="وخاشوثي", salary=15000)

with Session(engine) as session:
    session.add(new_emp)
    session.commit()
    session.refresh(new_emp)
