"""
run.py, the main driver function for the backend, starts the flask server with all routes connected.
"""
from application import app
from flask_cors import CORS
from controllers import update_sprint
from policies import *
from flask_apscheduler import APScheduler
from services import getter
from backup_db import create_backup

CORS(app, origin='*')

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)

# # cron examples
@scheduler.task('cron', id='do_job_2', minute=0, hour=0)
def job2():
    update_sprint.update_sprint()

@scheduler.task('cron', id='do_job_3', minute=0, hour=0, day_of_week='sun')
def job3():
    create_backup()

scheduler.start()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)