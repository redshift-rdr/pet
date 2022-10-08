from flask import render_template, flash, redirect, request, url_for, session, make_response, jsonify
from app import app, db
from app.models import Engagement, Task, Tasklist, EngagementTemplate, TasklistTemplate, TaskTemplate
from app.forms import AddEngagementForm
from datetime import date, datetime, timedelta

def get_model(model_name : str):
    model_map = {
        'Engagement': Engagement, 
        'Task': Task, 
        'Tasklist': Tasklist, 
        'EngagementTemplate': EngagementTemplate, 
        'TasklistTemplate': TasklistTemplate, 
        'TaskTemplate': TaskTemplate
    }

    try:
        return model_map[model_name]
    except KeyError:
        return None

## Web GUI routes
@app.route('/')
@app.route('/index')
def index():
    engagements = db.session.query(Engagement).all()

    return render_template('index.html', engagements=engagements)

@app.route('/add_engagement', methods=['GET', 'POST'])
def add_engagement():
    form = AddEngagementForm()

    if form.validate_on_submit():
        template = db.session.query(EngagementTemplate).filter_by(uuid=form.engagement_template.data).first()

        new_engagement = Engagement(title=form.title.data, client=form.client.data, category=form.category.data, start=form.start.data, end=form.end.data, notes=form.notes.data, template=template)
        tasklist_templates = template.tasklist_templates
        tasklists = []
        for tasklist_template in tasklist_templates:
            new_tasklist = Tasklist(title=tasklist_template.title)
            tasks = []
            for task_template in tasklist_template.task_templates:
                new_task = Task(title=task_template.title, notes=task_template.notes, deadline=date.today()+timedelta(days=int(task_template.days_to_complete)))
                tasks.append(new_task)
                db.session.add(new_task)
            new_tasklist.tasks = tasks
            tasklists.append(new_tasklist)
            db.session.add(new_tasklist)
        new_engagement.tasklists = tasklists

        db.session.add(new_engagement)
        db.session.commit()

    return render_template('addengagement.html', form=form)

## API routes
# get all instances in model
@app.route('/api/<model>')
def get_all(model):
    model = get_model(model)

    items = db.session.query(model).all()
    json_items = [item.as_dict() for item in items]
    
    return jsonify(json_items)

# get a specific instance of model
@app.route('/api/<model>/<uuid>')
def get_one(model, uuid):
    model = get_model(model)

    item = db.session.query(model).filter_by(uuid=uuid).first()
    if not item:
        return jsonify({})

    return jsonify(item.as_dict())

# add an new instance of a model
@app.route('/api/<model>/add', methods=['POST'])
def add(model):
    model = get_model(model)
    data = request.get_json()

    try:
        model_instance = model(**data)
    except Exception as e:
        return jsonify({'error': f'{e}'})

    db.session.add(model_instance)
    db.session.commit()

    return jsonify(model_instance.as_dict())    

# update an instance of a model
@app.route('/api/<model>/<uuid>/update', methods=['POST'])
def update(model, uuid):
    model = get_model(model)
    data = request.get_json()

    model_instance = db.session.query(model).filter_by(uuid=uuid).first()
    if not model_instance:
        return jsonify({"error": "could not find a model with that uuid"})

    try:
        for k,v in data.items():
            if hasattr(model_instance, k):
                setattr(model_instance, k, v)

        db.session.add(model_instance)
        db.session.commit()    
    except Exception as e:
        return jsonify({"error" : f"{e}"})

    return jsonify(model_instance.as_dict())

# delete an instance of a model
@app.route('/api/<model>/<uuid>/remove', methods=['POST'])
def remove(model, uuid):
    model = get_model(model)
    data = request.get_json()

    try:
        db.session.query(model).filter_by(uuid=uuid).delete()
        db.session.commit()
    except Exception as e:
        return jsonify({"error" : f"{e}"})

    return jsonify({"status": "success", "message": "model deleted successfully"})

# create a relationship between models
@app.route('/api/<model>/<uuid>/link', methods=['POST'])
def link(model, uuid):
    model = get_model(model)
    data = request.get_json()

    link_model = get_model(data["model"])

    to_link = db.session.query(link_model).filter_by(uuid=data["uuid"]).first()
    model_instance = db.session.query(model).filter_by(uuid=uuid).first()

    setattr(model_instance, data["linked_attribute"], to_link)

    db.session.add_all([to_link, model_instance])
    db.session.commit()

    return jsonify(model_instance.as_dict())