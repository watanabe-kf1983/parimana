Odds Analyser

```
parimana
```

or

```
docker run -p 6379:6379 -d redis
celery -A parimana.batch.app worker -P threads --loglevel=info
parimana-web
```
