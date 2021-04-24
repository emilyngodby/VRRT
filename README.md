# VRRT [![Build Status](https://travis-ci.com/emilyngodby/VRRT.svg?branch=master)](https://travis-ci.com/emilyngodby/VRRT)
Virtual Reality Research Tool for the VA in Reno, NV.
## To install Rasa
Install Rasa (preferably in a venv) and dependencies

Python 3.8 is NOT supported by Rasa

https://rasa.com/docs/rasa/installation/

## Command Line use
You can train the model after changing the files by running

`rasa train`

then you can see the conversation on the command line by running

`rasa shell`


## To use Chatbot with django
Run the rasa server by starting the venv and running 

`rasa run -m models --enable-api --cors "*" --debug `

Then run the django server in another terminal by doing

`python3 manage.py runserver`
