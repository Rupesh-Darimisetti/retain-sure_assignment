# Major issues you identified
- The issues that was found in the code where the data is not conveted to JSON while displaying in the web for get request and others fixed using **jsonify** module.
- the code was not separeted for SQL querring and logic which is important because once you change in sql query of a python fucntion name it can be used again without any doubt and it is quick to modify it. Logic of the code is to diplay data and status code in the way we want like JSOn or template files.


# Changes you made and why
- seperated the app.py code to its respective  SQL and Bussiness logic of python file for better coding and performance.

# Any assumptions or trade-offs
- while testing one thing that the data is created from the code where it test from its file so that it data must persist in database with id 1,2 to work 100% code coverage.

# What you would do with more time
- could have created UI in frontend language and give the code.