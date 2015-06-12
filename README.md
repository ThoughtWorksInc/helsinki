##Getting Started


###You will need

- MongoDB
- Elasticsearch

To be running on `localhost`


###Install Dependencies

`pip install -r requirements.txt`


###Running the server

`python main.py`

Run with `--reindex` to load the data from OpenAhjo into elasticsearch

Run with `--debug` for live reloading and stack traces


###Sending Notifications

To send notifications you will need to have your mailgun credentials in `mailgun.json`
(see the example file). Then run

`python main.py --mailshot`


###Running Tests

Before pushing:

`./pre_push.sh`

#####Unit tests:

`nosetests`

To include print output:

`nosetests -s`

#####Code style checks:

`pep8 .`


##Front End

Default will watch the sass:

```
gulp
```

To output minified css:

```
gulp --production true
```
