from transform.transform import calculate_salary
from Vehicle_Management_System.app.db.postgres import insert_salary
import datetime

def run_salary_job(employees):
    month = datetime.date.today().replace(day=1)

    for emp in employees:
        net = calculate_salary(
            emp["base_salary"],
            emp["allowances"],
            emp["deductions"]
        )

        payload = {
            "employee_id": emp["employee_id"],
            "salary_month": month,
            "base_salary": emp["base_salary"],
            "allowances": emp["allowances"],
            "deductions": emp["deductions"],
            "net_salary": net
        }

        insert_salary(payload)