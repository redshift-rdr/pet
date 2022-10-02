from app import db
import uuid

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

class Task(db.Model):
    uuid = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(128), index=True)
    notes = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False)

    tasklist_id = db.Column(db.String(36), db.ForeignKey('tasklist.uuid'))
    tasklist = db.relationship('Tasklist', back_populates='tasks')

    def __repr__(self):
        return f'Task({self.title})'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}