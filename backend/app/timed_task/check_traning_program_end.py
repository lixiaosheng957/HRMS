from app.timed_task import scheduler
from app.models.base import db
from app.models.training_program import TrainingProgram
import datetime


@scheduler.task('cron', id='do_job_check_training_program_end', hour='06', minute='00', second='00')
def job1():
    now_date = str(datetime.date.today())
    end_program_list = TrainingProgram.query.filter(
        TrainingProgram.endDate < datetime.datetime.strptime(now_date, '%Y-%m-%d'), TrainingProgram.status == 1,
        TrainingProgram.isPublish == 1, TrainingProgram.isEnd != 1).all()
    with db.auto_commit():
        for program in end_program_list:
            program.isEnd = True
