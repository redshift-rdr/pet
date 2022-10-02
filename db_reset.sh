rm -rf app.db migrations/
flask db init
flask db migrate -m 'bang'
flask db upgrade
python db_init.py