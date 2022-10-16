from app import db
import uuid
from datetime import date, timedelta

def generate_uuid():
    return str(uuid.uuid4())

class EngagementTemplate(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    client = db.Column(db.String(36))
    title = db.Column(db.String(64), index=True, unique=True)

    tasklist_templates = db.relationship('TasklistTemplate', back_populates='template')
    engagement_id = db.Column(db.String(36), db.ForeignKey('engagement.uuid'))
    engagement = db.relationship('Engagement', back_populates='template')

    def __repr__(self):
        return f'EngagementTemplate({self.title})'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TasklistTemplate(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(64), index=True, unique=True)

    task_templates = db.relationship('TaskTemplate', back_populates='template')
    engagementtemplate_id = db.Column(db.String(36), db.ForeignKey('engagement_template.uuid'))
    template = db.relationship('EngagementTemplate', back_populates='tasklist_templates')

    def __repr__(self):
        return f'TasklistTemplate({self.title})'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TaskTemplate(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(64), index=True, unique=True)
    notes = db.Column(db.Text)
    days_to_complete = db.Column(db.Integer)
    offset = db.Column(db.String(10))

    tasklisttemplate_id = db.Column(db.String(36), db.ForeignKey('tasklist_template.uuid'))
    template = db.relationship('TasklistTemplate', back_populates='task_templates')

    def __repr__(self):
        return f'TaskTemplate({self.title})'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Engagement(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    client = db.Column(db.String(36))
    title = db.Column(db.String(128), index=True)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    notes = db.Column(db.Text)
    category = db.Column(db.String(36))

    template = db.relationship('EngagementTemplate', back_populates='engagement', uselist=False)
    tasklists = db.relationship('Tasklist', back_populates='engagement')

    def __repr__(self):
        return f'Engagement({self.title})'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def completed_count(self):
        complete_count = 0
        total = 0

        for tasklist in self.tasklists:
            data = tasklist.completed_count()

            complete_count += data[0]
            total += data[1]

        return (complete_count, total)

    def completed_percentage(self):
        data = self.completed_count()

        return data[0] / data[1] * 100

class Tasklist(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(128), index=True)
    notes = db.Column(db.Text)

    engagement_id = db.Column(db.String(36), db.ForeignKey('engagement.uuid'))
    engagement = db.relationship('Engagement', back_populates='tasklists')
    tasks = db.relationship('Task', back_populates='tasklist')

    def __repr__(self):
        return f'Tasklist({self.title})'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def completed_count(self):
        return (sum([1 for task in self.tasks if task.complete]), len(self.tasks))

class Task(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(128), index=True)
    notes = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.Date)

    tasklist_id = db.Column(db.String(36), db.ForeignKey('tasklist.uuid'))
    tasklist = db.relationship('Tasklist', back_populates='tasks')

    def __repr__(self):
        return f'Task({self.title})'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def is_overdue(self):
        return date.today() >= self.deadline