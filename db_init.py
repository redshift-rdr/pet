from app import db

from app.models import Engagement, Task, Tasklist, EngagementTemplate, TasklistTemplate, TaskTemplate
from datetime import datetime, timedelta

task_template = TaskTemplate(title='Test Template 1', notes='test')
tasklist_template = TasklistTemplate(title='Test tasklist template', task_templates=[task_template])
engagement_template = EngagementTemplate(client='Context', title='test engagement template', tasklist_templates=[tasklist_template])


task = Task(title='test task', notes='just a test', complete=False)
tasklist = Tasklist(title='test tasklist', tasks=[task])
test_engagement = Engagement(client='Context', title='Test web app', start=datetime.now(), end=datetime.now(), notes='test', template=engagement_template, tasklists=[tasklist])

print('[+] Adding test data to the database')

try:
    db.session.add_all([task_template, tasklist_template, engagement_template, task, tasklist, test_engagement])
    db.session.commit()
except Exception as e:
    print('[-] There was a problem adding the data')
    print(f'[-] error: {e}')
    exit(1)

print('[+] Test data added successfully')