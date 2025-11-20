from app.database import create_db_and_tables, engine
from app.models.employee import Employee
from sqlmodel import Session, select

create_db_and_tables()
with Session(engine) as session:
    rows = session.exec(select(Employee)).all()
    print("عدد الموظفين في DB:", len(rows))
    for r in rows:
        print(r.id, getattr(r, "name", None), getattr(r, "email", None))