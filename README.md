##Getting Started

###You will need

- MongoDB
- Elasticsearch

To be running on `localhost`

###Running the server

`python main.py`

Run with `--reindex` to load the data from OpenAhjo into elasticsearch
Run with `--debug` for live reloading and stack traces

##Front End

Default will watch the sass:

```
gulp
```

To output minified css:

```
gulp --production true
```
