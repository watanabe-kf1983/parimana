Odds Analyser

docker run -p 6379:6379 -d redis
celery -A parimana.batch.app worker -P threads --loglevel=info
python -m parimana.webapi
python -m parimana
