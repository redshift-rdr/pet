from flask import render_template, flash, redirect, request, url_for, session, make_response, jsonify
from app import app, db
from app.models import Engagement, Task, Tasklist, EngagementTemplate, TasklistTemplate, TaskTemplate
from datetime import datetime, timedelta

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

@app.route('/')
@app.route('/index')
def index():
    #return render_template('index.html')
    return 'working'


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

@app.route('/api/<model>/add', methods=['POST'])
def add(model):
    pass