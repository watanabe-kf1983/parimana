Odds Analyser

celery -A parimana.batch.app worker -P threads --loglevel=info
python -m parimana.webapi
python -m parimana
