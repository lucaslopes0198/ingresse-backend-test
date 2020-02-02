# ingresse-backend-test

## Installation / Usage events API

* Ensure you have installed pipenv. If not, run this:
	```sh
	$ pip install pipenv
	```
*  Git clone this repo:
	```sh
	$ git clone https://github.com/lucaslopes0198/ingresse-backend-test.git
	```

* **Dependencies**
	* cd into eventsAPI as such:
		```sh
		$ cd ingresse-backend-test/eventsAPI
		```
	* Install pipfile:
		```sh
		$ pipenv install Pipfile
		```
	* Activate your virtual environment:
		```sh
		$ pipenv shell
		```

#### For the next steps, make sure you are in the virtual environment.

* **Testing API**
	* To run tests, ensure you are in the eventsAPI folder and run:
		```sh
		(eventsAPI) $ coverage run -m unittest discover
		```
	* View the report in terminal:
		```sh
		(eventsAPI) $ coverage report
		```
	* Generate a html report:
		```sh
		(eventsAPI) $ coverage html
		```
	* You can find the html in the `htmlcov` folder and view it by opening `index.html` in your browser.

* **Database**
	* To create the database, ensure you are in the eventsAPI folder and run:
		```sh
		(eventsAPI) $ python db_create.py
		```
* **Running it**
	* Run the server using this command:
		```sh
		(eventsAPI) $ flask run
		```
* **Endpoints**
	* You can create an event using POST method:
		```sh
		http://localhost:5000/events
		```
	* Payload example to create an event:
		```json
		{
			"name": "Test1 event",
			"place": "Test1 place",
			"tags": [
				"Test1 t1",
				"Test1 t2"
			],
			"datetimes": [
				"01/01/19 20:30:00",
				"02/01/19 22:00:00"
			]
		}
		```

	* You can get all events using GET method:
		```sh
		http://localhost:5000/events
		```

	* You can get filtered events using GET method:
		```sh
		http://localhost:5000/events/filters
		```
	* Payload example to get filtered events:
		```json
		{
			"name": "Test1 event",
			"tags": [
				"Test1 t1",
			],
			"datetimes": [
				"01/01/19 20:30:00",
				"02/01/19 22:00:00"
			]
		}
		```

	* You can update an event using PUT method:
		```sh
		http://localhost:5000/events
		```
	* Payload example to update an event:
		```json
		{
			"name": "Name updated",
			"tags": [
				"Tag1 updated",
				"Tag2 updated"
			]
		}
		```

	* You can delete an event using DELETE method by ID:
		```sh
		http://localhost:5000/events/<id>
		```
