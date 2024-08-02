python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 scrapping.py
python3 scheduling.py
cd search_engine
python3 manage.py runserver
