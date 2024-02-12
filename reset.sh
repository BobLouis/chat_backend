rm -rf db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
sudo service redis-server restart
python3 manage.py runserver