class TrainingProject(SQLModel, table=True):
    """جدول وسيط يربط التدريب بالمشروعات (Many-to-Many)"""

    id: Optional[int] = Field(default=None, primary_key=True)
    training_id: int = Field(foreign_key="employeetraining.id", index=True)
    project_id: int = Field(foreign_key="project.id", index=True)

    mandatory: bool = False  # هل التدريب إلزامي للمشروع؟
