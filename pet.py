from app import app, db
from app.models import Engagement, Task, Tasklist, EngagementTemplate, TasklistTemplate, TaskTemplate

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Engagement': Engagement, 'Task': Task, 'Tasklist': Tasklist, 'EngagementTemplate': EngagementTemplate, 'TasklistTemplate': TasklistTemplate, 'TaskTemplate': TaskTemplate}