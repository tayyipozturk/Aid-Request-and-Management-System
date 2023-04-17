# Project

Aid Request and Management System

##

This project consists of a user class with authorization login functions.
A campaign consists request multiple requests.
Requesters can create requests and run queries to look for requests. They can create watchers to get notified of specific request creations.
Requesters can request delivery of items they want if they have stock.
Providers can inform requesters about their stock and provide items if they want to. The main frame of the application is Campaign, which processes requests and provides responses to them.

## Students

Mustafa Burak Akkaya
2396968

Muhammed Tayyip Öztürk
2380806

## Content of Files

- `Class.user.py`: User Class File
- `Class.item.py`: Item Class File
- `Class.request.py`: Request Class File
- `Class.campaign.py` Campaign Class File
- `Enum.urgency.py`: Urgency Enum File
- `demo.py` Command line tester

## How to Run

You can utilize `demo.py` to test the system's functionality. It contains a simple command line interface to test the application. You can run it by typing `python3 demo.py` in the terminal.

### Class.user.py

This file contains the User class. It has the following attributes:

- full name -> string
- email -> string
- username -> string
- password -> string
- collection -> static list of all users

It has the following methods:

- `__init__`: Constructor
- `get()` : Returns the user's information
- `update(username=None, email=None, fullname=None, passwd=None)` : Updates the user's information, does not return anything
- `delete()` : Deletes the user, does not return anything
- `auth(plainpass)` : Checks if the plainpass is the same as the user's hashed password. Returns True if it is, False otherwise.
- `login(username, password)`: Login function. Returns the token randomly generated for the user if the login is successful, None if already logged in.
- `checksession(token)` : Checks if the user is logged in or not
- `logout()`: Logout function

### Class.item.py

This file contains the Item class. It has the following attributes:

- name -> string
- synonyms -> list of strings
- collection -> static list of all items

It has the following methods:

- `__init__`: Constructor
- `get()` : Returns the item's information as dictionary. -> `{'name': <itemname>, 'synonyms': ['<synonym1>', '<synonym2>', ...].join(",")}`
- `update(name=None, synonyms=None)` : Updates the item's information, does not return anything
- `delete()` : Deletes the item, does not return anything
- `search(name)` : Static method. Searches for an item with the given name. Returns the item if found, None otherwise and instantiates the item.

### Class.request.py

This file contains the Request class. It has the following attributes:

- owner -> string
- items_dict -> dictionary of items and their quantities -> `{'item': <itemname>, 'availibility': <availibility>, 'onroute': <onroute>}`
- geoloc -> in the form of rectangular region `` 'type': 0, 'values`: [[long, latitude],[long, latitude]] `` or circular region `'type': 1, 'values': [[long, latitude], radius]`
- urgency -> integer from 1 to 5
- comment -> string
- status -> string `open` or `closed`
- collection -> static list of all requests

It has the following methods:

- `__init__`: Constructor
- `get()` : Returns the request's information as dictionary. -> `{'owner': <username>, 'items': [{'item': <itemname>, 'availibility': <availibility>, 'onroute': <onroute>}, ...], 'geoloc': {'type': <type>, 'values': [<value1>, <value2>, ...]}, 'urgency': <urgency>, 'comment': <comment>>}`
- `update(owner=None, items_dict=None, geoloc=None, urgency=None, comment=None)` : Updates the request's information, returns True if successful, False otherwise
- `delete()` : Deletes the request, return True if successful, False otherwise
- `markavailable(user, items, expire, geoloc, comments)` : Marks the request as available. Returns unique ma_id if successful
- `pick(itemid, items)` : Picks the item that is available, marks it as onroute. Does not return anything
- `arrived(itemid)` : Marks the item's status as closed. Does not return anything

### Class.campaign.py

This file contains the Campaign class. It has the following attributes:

- name -> string
- requests -> list of requests
- description -> string
- requests -> dictionary of requests -> `{'req_id': <requestid>, 'data': <request>}`
- watches -> dictionary of watches -> `{'watch_id': <watchid>, 'callback': <callback_function>, 'item': <item>, 'loc':<location>, 'urgency': <urgency>}`
- collection -> static list of all campaigns

It has the following methods:

- `__init__`: Constructor
- `addrequest(request)` : Adds a request to the campaign. Returns request id if successful, None otherwise
- `remove(requestid)` : Removes a request from the campaign. Returns True if successful, False otherwise
- `update(requestid, owner=None, items_dict=None, geoloc=None, urgency=None, comment=None)` : Updates the request's information, returns True if successful, False otherwise
- `getrequest(requestid)` : Returns the request `(request_dict['data'].get())` with the given id if found, None otherwise
- `query(item=None, loc=None, urgency=None)` : Returns a list of requests that match the given parameters. Item parameter is an array of Items.
- `watch(callback, item, loc, urgency)` : Adds a watch to the campaign for the items in the item array. Returns watch id if successful, None otherwise
- `unwatch(watchid)` : Removes a watch from the campaign. Returns True if successful, False otherwise

### Enum.urgency.py

This file contains the Urgency enum. It has the following attributes:

- `URGENT` -> 1
- `SOON` -> 2
- `DAYS` -> 3
- `WEEKS` -> 4
- `OPTIONAL` -> 5
