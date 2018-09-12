# Python Status.io 

Python package for [Status.io](https://status.io)

[![Downloads](https://img.shields.io/pypi/v/statusio-python.svg)](https://pypi.python.org/pypi/statusio-python/)


This library provides a pure Python interface for the [Status.io API](http://developers.status.io/). It works with Python versions from 2.6+.


## Installation


    $ pip install statusio-python

## Usage

```python
import statusio
api = statusio.Api(api_id='api_id', api_key='api_key')
```


Retrieve status page summary:

```python
summary = api.StatusSummary('status_page_id')
print(summary)
```

View the full API documentation at: http://developers.status.io/
