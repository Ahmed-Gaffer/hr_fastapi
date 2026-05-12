from pathlib import Path

from sqlmodel import Session

from app.database import engine
from app.services.imports.employees import EmployeeImporter


def import_employees_from_excel(file_path: str, commit: bool = True, allow_create_tenant: bool = True):
    """Import employee rows from an Excel file into the database."""
    source = Path(file_path)
    if not source.exists():
        raise FileNotFoundError(f"Excel file not found: {source}")

    with source.open("rb") as excel_file:
        content = excel_file.read()

    importer = EmployeeImporter()
    with Session(engine) as session:
        result = importer.run(
            session=session,
            stream=content,
            commit=commit,
            allow_create_tenant=allow_create_tenant,
        )
    return result
