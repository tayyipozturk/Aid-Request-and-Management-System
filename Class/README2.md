# Phase 2

## 1. Introduction

This is the second phase of the project. In this phase, we will be implementing the following features:

- Client: Handles user input and sends requests to the server. `python3 client.py`
- Server: Handles requests from the client and sends responses. `python3 server.py`

## 2. Client

The client is responsible for handling user input and sending requests to the server. The client will be able to send the following requests to the server:

- `login` <username> <password> login the user with the given username and password
- `logout` logout the current user

- `new <campaign_name> <description>`create a new campaign
- `list` list all campaigns
- `open <campaign_name>` --> open the given campaign
- `close` close the current campaign (if any)

- `add_request <#_of_items> <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count> <latitude> <longtitude> <urgency> <description>` add a new request to the current campaign

- `get_request <request_id>` get the request with the given request id in the current campaign

- `update_request <#_of_items> <target_request_id> <item_1> <item_1_count> <item_2> <item_2_count> ... <item_n> <item_n_count> <latitude> <longtitude> <urgency> <description>` update the request with the given request id in the current campaign

- `remove_request <request_id>` remove the request with the given request id in the current campaign

- `query <#_of_items> <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <latitude2> <longtitude2> <urgency>` query the server for the requests that match the given query in a rectangular region with the given coordinates
- `query <#_of_items> <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <radius> <urgency>` query the server for the requests that match the given query in a circular region with the given center coordinates and radius

- `watch <#_of_items> <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <latitude2> <longtitude2> <urgency>` watch the server for the requests that match the given query in a rectangular region with the given coordinates

`watch <#_of_items> <item_1> <item_2> ... <item_n> 0 <latitude1> <longtitude1> <radius> <urgency>` watch the server for the requests that match the given query in a circular region with the given center coordinates and radius

- `unwatch <watch_id>` stop watching the server for the request with the given watch id

- `search_item <item_name>` search for the item with the given name

- `update_item <target_item_name> <new_name> <new_synonym1> <new_synonym2> ... <new_synonym_n>` update the item with the given item name and synonyms

- `remove_item <item_name>` remove the item with the given item name
