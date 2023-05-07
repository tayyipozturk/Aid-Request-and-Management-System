# Aid Request and Management System

## Phase 2 --- Server - Client Implementation

## Students

Mustafa Burak Akkaya
2396968

Muhammed Tayyip Öztürk
2380806

## 1. Introduction

This is the second phase of the project. In this phase, we will be implementing the following features:

- Server: Handles requests from the client and sends responses. `python3 server.py`
- Client: Handles user input and sends requests to the server. `python3 client.py`

## 2. Server

The server is responsible for handling requests from the client and sending responses. Each client will be handled in a separate thread in the server.

## 3. Client

The client is responsible for handling user input and sending requests to the server. The client will be able to send the following requests to the server:

- `login` <username> <password> login the user with the given username and password

  e.g. `login bob 123`

- `logout` logout the current user

  e.g. `logout`

- `new <campaign_name> <description>`create a new campaign

  e.g. `new campaign1 my first campaign`

- `list` list all campaigns

  e.g. `list`

- `open <campaign_name>` --> open the given campaign

  e.g. `open campaign1`

- `close` close the current campaign (if any)

  e.g. `close`

- `add_request <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count> <latitude> <longtitude> <urgency> <description>` add a new request to the current campaign

  e.g. `add_request water 10 bread 20 10 10 SOON help me`

- `get_request <request_id>` get the request with the given request id in the current campaign

  e.g. `get_request 8301ebcb-7cc4-49dd-858d-d950d93fd21f`

- `update_request <target_request_id> <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count> <latitude> <longtitude> <urgency> <description>` update the request with the given request id in the current campaign

  e.g. `update_request 8301ebcb-7cc4-49dd-858d-d950d93fd21f water 25 bread 100 10 10 SOON help me`

- `remove_request <request_id>` remove the request with the given request id in the current campaign

  e.g. `remove_request 8301ebcb-7cc4-49dd-858d-d950d93fd21f`

- `query <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <latitude2> <longtitude2> <urgency>` query the server for the requests that match the given query in a rectangular region with the given coordinates

  e.g. `query watermelon apple 0 10 10 20 20 SOON`

- `query <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <radius> <urgency>` query the server for the requests that match the given query in a circular region with the given center coordinates and radius

  e.g. `query watermelon apple 1 10 10 5 SOON`

- `watch <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <latitude2> <longtitude2> <urgency>` watch the server for the requests that match the given query in a rectangular region with the given coordinates. returns watch_id

  e.g. `watch watermelon apple 0 10 10 20 20 SOON`

- `watch <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <radius> <urgency>` watch the server for the requests that match the given query in a circular region with the given center coordinates and radius. returns watch_id

  e.g. `watch watermelon apple 1 10 10 5 SOON`

- `unwatch <watch_id>` stop watching the server for the request with the given watch id

  e.g. `unwatch 8301ebcb-7cc4-49dd-858d-a923f5312d320`

- `mark_available <id> <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count> <expiration_time__from_now_as_hours> <latitude> <longtitude> <comment>` mark the request with the given id as available. returns mark_available_id

  e.g. `mark_available 8301ebcb-7cc4-49dd-858d-d950d93fd21f water 5 bread 10 72 24.3241 26.2321 came for help`

- `pick <request_id> <mark_available_id> <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count>` pick the request with the given request id and mark available id

  e.g. `pick 8301ebcb-7cc4-49dd-858d-d950d93fd21f 8301ebcb-7cc4-49dd-858d-a023f5312d320 water 5 bread 10`

- `arrived <request_id> <mark_available_id>` mark the request with the given request id and mark available id as arrived

  e.g. `arrived 8301ebcb-7cc4-49dd-858d-d950d93fd21f 8301ebcb-7cc4-49dd-858d-a023f5312d320`

- `search_item <item_name>` search for the item with the given name

  e.g. `search_item watermelon`

- `update_item <target_item_name> <new_name> <new_synonym1> <new_synonym2> ... <new_synonym_n>` update the item with the given item name and synonyms

  e.g. `update_item watermelon melon water`

- `remove_item <item_name>` remove the item with the given item name

  e.g. `remove_item watermelon`
