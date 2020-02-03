# ingresse-backend-test

## Installation / Usage events API

* Ensure you have installed pipenv. If not, run this:
	```
	$ pip install pipenv
	```
*  Git clone this repo:
	```
	$ git clone https://github.com/lucaslopes0198/ingresse-backend-test.git
	```

* **Dependencies**
	* cd into eventsAPI as such:
		```
		$ cd ingresse-backend-test/eventsAPI
		```
	* Install pipfile:
		```
		$ pipenv install Pipfile
		```
	* Activate your virtual environment:
		```
		$ pipenv shell
		```

#### For the next steps, make sure you are in the virtual environment and in the eventsAPI folder.

* **Testing API**
	* To run tests:
		```
		(eventsAPI) $ coverage run -m unittest discover
		```
	* View the report in terminal:
		```
		(eventsAPI) $ coverage report
		```
	* Generate a html report:
		```
		(eventsAPI) $ coverage html
		```
	* You can find the html in the `htmlcov` folder and view it by opening `index.html` in your browser.

* **Database**
	* To create the database, run:
		```
		(eventsAPI) $ python db_create.py
		```
* **Running it**
	* Run the server using this command:
		```
		(eventsAPI) $ flask run
		```
* **Endpoints**
	* Base endpoint:
		```
		http://localhost:5000
		```
	* Request Syntax to create an event:
		```
		response = client.post(
			"/events",
			json={
				"name": "String",
				"place": "String",
				"tags": [
					"String",
				],
				"datetimes": [
					"String", # dd/mm/yy H:M:S
				]
			}
		)
		```

	* Request Syntax to get all events:
		```
		response = client.get("/events")
		```

	* Request Syntax to get filtered events:
		```
		response = client.get(
			"/events/filters",
			json={
				"name": "String",
				"tags": [
					"String",
				],
				"datetimes": [
					"String", # dd/mm/yy H:M:S
					"String", # dd/mm/yy H:M:S
				]
			}
		)
		```

	* Request Syntax to update an event:
		```
		response = client.put(
			"/events/<id>",
			json={
				"name": "String",
				"tags": [
					"String",
				]
			}
		)
		```

	* Request Syntax to update interested:
		```
		response = client.put(
			"/events/<id>",
			json={
				"interested": "bool", # True=increase, False=decrease
			}
		)
		```

	* Request Syntax to delete an event:
		```
		response = client.delete("/events/<id>")
		```

	* Response Syntax to create an event:
	```
	{
		"datetimes": [
			"String",
		],
		"id": Int,
		"interested": Int,
		"name": "String",
		"place": "String",
		"tags": [
			"String",
		]
	}
	```

	* Response Syntax to get and update events:
	```
	[
		{
			"datetimes": [
				"String",
			],
			"id": Int,
			"interested": Int,
			"name": "String",
			"place": "String",
			"tags": [
				"String",
			]
		},
	]
	```

	* Response Syntax to delete an event:
	```
	{
		"msg": "event deleted successfully",
		"id": Int
	}
	```
