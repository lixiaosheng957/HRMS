from app.timed_task import scheduler
from app.models.base import db
from app.models.employee import Employee
import datetime


@scheduler.task('cron', id='do_job_check_training_program_end', hour='23', minute='03', second='00')
def change_work_age():
    today = datetime.date.today()
    employee_list = Employee.query.filter_by(workState="在职").all()
    for employee in employee_list:
        create_date = datetime.datetime.fromtimestamp(employee.create_time).date()
        difference = (today - create_date).days
        if difference % 182 >= 1:
            with db.auto_commit():
                employee.workAge = employee.workAge + (difference % 182) * 0.5

