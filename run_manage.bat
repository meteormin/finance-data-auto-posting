call conda activate x86
call %~d0
call cd %~p0
call start http://localhost:8000/manage
call python manage.py runserver

