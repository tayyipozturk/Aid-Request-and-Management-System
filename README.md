# Aid Request and Management System

This project is a web application that allows users to request and supply aid. It is developed using Django framework and websockets on Python.

## Students

Mustafa Burak Akkaya
2396968

Muhammed Tayyip Öztürk
2380806

## Installation

### Requirements

- Python 3.10 or higher

### Run

Run commands below on separate terminals.

- ```python3 server/server_3.py``` For backend and notification websocket server.
- ```python3 django/manage.py runserver``` For Django server.

## Usage

### Register
- User registers to the system by providing username and password.

### Login
- User logs in to the system by providing username and password that is registered before.

### Campaign Operations
#### Create
- User can create a campaign by providing title and description by clicking `New Campaign` button.
#### List
- User can see all campaigns by clicking `List Campaigns` button.
#### Open/Close
- User can open a campaign to make miscellaneous request operations by clicking `Open Campaign` button and selecting a campaign from available campaigns' list.
- User can close the current campaign if applicable, by clicking `Close Campaign` button.

### Item Operations
#### Search (Adds if not found)
- User can search an item by providing either item name or synonym. If the search is successful, user can see the item's name and synonyms and, item is automatically added to the campaign otherwise.
#### Update
- User can update an item by entering the target item name and providing item name and new synonyms.
#### Delete
- User can delete an item by entering the target item name.

### Request Operations
#### Add
- User can add a request by providing item(s) and quantity(ies) by clicking `Add Request` button with the request location selected on the map, urgency of the request and the description.
#### List
- User can see all requests by clicking `List Requests` button. Moreover, request info can be accessed via view button for each request in the list.
#### Update
- User can update a request by clicking `Update Request` button and selecting a request from the list. Then, user can update the request by providing new item(s) and quantity(ies), request location, urgency of the request and the description.
#### Delete
- User can delete a request by clicking `Remove Request` button and selecting a request from the list.

### Request Operations for Aid Suppliers
#### Search
- User can search an area for requests by clicking either Rectangular or Circular button under the `Search` tab.
- If Rectangular is selected, user can enter two points' latitude and longitude values to create a rectangular area. By entering the item name and the urgency of the request, user can see all requests in the area.
- If Circular is selected, user can enter a point's latitude and longitude values and a radius value to create a circular area. By entering the item name and the urgency of the request, user can see all requests in the area.
#### Watch
- User can watch future requests for an item by clicking either Rectangular or Circular button under the `Watch` tab.
- If Rectangular is selected, user can enter two points' latitude and longitude values to create a rectangular area. By entering the item name and the urgency of the request, user can see all requests in the area with the urgency more severe than or equal to the entered urgency.
- If Circular is selected, user can enter a point's latitude and longitude values and a radius value to create a circular area. By entering the item name and the urgency of the request, user can see all requests in the area with the urgency more severe than or equal to the entered urgency.
- After a request matching the criteria is added to the system, user is notified by a notification message.
#### Unwatch
- Unwatching a request is also possible by clicking `Unwatch` button under the `Watch` tab and selecting a request already watched by the user from the list.
#### Mark Available
- User can mark an item as available by clicking `Mark Available` button in the `Request Info` page via listing requests. Then, user can enter the item and quantity to mark as available. Availability time and location with the comments are also required.
- If a request is available, supplier location can also be seen on the map with the request location.
### Request Operations for Aid Requesters
#### Pick
- If an item is marked as available, it can be seen under the `Available Supplies` tab in the request info page. By clicking on the select button, requester can pick the supply by entering the quantity of the item. If pick quantity is more than available items, number of available items are picked.
#### Arrive
- If an item is picked, requester can click `Arrive` button in the request info page to complete the process. If all items in the request are picked and arrived, the request status is changed to `CLOSED`.