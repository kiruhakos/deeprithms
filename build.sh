set -o errexit

pip install -r requirements.txt
pip install django-modeltranslation

python manage.py compilemessages -l uk


python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py createsu