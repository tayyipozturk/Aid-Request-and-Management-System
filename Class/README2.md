# Phase 2

## 1. Introduction

This is the second phase of the project. In this phase, we will be implementing the following features:

- Client: Handles user input and sends requests to the server. `python3 client.py`
- Server: Handles requests from the client and sends responses. `python3 server.py`

## test

login bob 123
open campaign1
watch 1 water 0 5 5 10 10 SOON
add_request 2 water 10 food 20 10 10 SOON help
add_request 2 limon 11 kek 2 7 7 SOON help
add_request 1 water 10 7 7 SOON help
query 1 water 0 5 5 10 10 SOON

add_request 1 water 2 6 7 SOON help

update_request 2 XXX limon 11 kek 2 6 6 SOON help
mark_available 8301ebcb-7cc4-49dd-858d-d950d93fd21f water 5 2 5 5 help
pick reqid maid water 2
82024c47-d198-450a-84b5-949

## 2. Client

The client is responsible for handling user input and sending requests to the server. The client will be able to send the following requests to the server:

- `login` <username> <password> login the user with the given username and password
- `logout` logout the current user

- `new <campaign_name> <description>`create a new campaign
- `list` list all campaigns
- `open <campaign_name>` --> open the given campaign
- `close` close the current campaign (if any)

- `add_request <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count> <latitude> <longtitude> <urgency> <description>` add a new request to the current campaign

- `get_request <request_id>` get the request with the given request id in the current campaign

- `update_request <target_request_id> <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count> <latitude> <longtitude> <urgency> <description>` update the request with the given request id in the current campaign

- `remove_request <request_id>` remove the request with the given request id in the current campaign

- `query <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <latitude2> <longtitude2> <urgency>` query the server for the requests that match the given query in a rectangular region with the given coordinates
- `query <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <radius> <urgency>` query the server for the requests that match the given query in a circular region with the given center coordinates and radius

- `watch <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <latitude2> <longtitude2> <urgency>` watch the server for the requests that match the given query in a rectangular region with the given coordinates

`watch <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <radius> <urgency>` watch the server for the requests that match the given query in a circular region with the given center coordinates and radius

- `unwatch <watch_id>` stop watching the server for the request with the given watch id

- `search_item <item_name>` search for the item with the given name

- `update_item <target_item_name> <new_name> <new_synonym1> <new_synonym2> ... <new_synonym_n>` update the item with the given item name and synonyms

- `remove_item <item_name>` remove the item with the given item name

- `mark_available <id> <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count> <expiration_time> <latitude> <longtitude> <comment>` mark the request with the given id as available

- `pick <request_id> <mark_available_id> <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count>` pick the request with the given request id and mark available id

- `arrived <request_id> <mark_available_id>` mark the request with the given request id and mark available id as arrived
