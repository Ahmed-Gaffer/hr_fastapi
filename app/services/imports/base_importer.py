# File Path: E:/خاص احمد جعفر/برمجة/مشاريع/hr_fastapi/app/services\imports\base_importer.py
# File Name: base_importer.py
# -----------------------------------------



from datetime import datetime

class BaseImporter:
    def new_report(self, file_id: str, dry_run: bool):
        return {
            "status": "pending",
            "file_id": file_id,
            "dry_run": dry_run,
            "added": 0,
            "updated": 0,
            "rejected": 0,
            "errors": [],
            "warnings": [],
            "meta": {"started_at": datetime.utcnow().isoformat()}
        }

    def finalize_report(self, report: dict):
        report["meta"]["finished_at"] = datetime.utcnow().isoformat()
        return report

    def safe_rollback(self, session):
        try:
            session.rollback()
        except:
            pass