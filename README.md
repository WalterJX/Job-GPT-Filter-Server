# Job-GPT-Filter-Server
 
Before you run the server for the first time (and every time you change the structure of the table), run the following commands:

python manage.py makemigrations

python manage.py migrate

Note that currently GPT-3.5-turbo api is not acting ideally as we thought, it's answer quality is much worse than ChatGPT 3.5. Other alternative solution including Claude (or Claude2), Bard, etc.
