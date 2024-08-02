
## Create a virtual environment
python3 -m venv venv

## Work within the virtual environment
source venv/bin/activate

## Install the required dependencies
pip3 install -r requirements.txt

## Scrape the data
python3 scrapping.py

## Scheduler that scarapes data periodically
python3 scheduling.py

## Run the search engine
cd search_engine
python3 manage.py runserver

## Run the cluser

cd search_engine
python3 manage.py runserver
Go to /cluster