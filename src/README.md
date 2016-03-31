How to use:
Run twepy.py and queenBee.py
Open 127.0.0.1:8080 in your browser and wait for sometime(5 mins).

Restart twepy.py if it stops

The program takes 100 tweets and displays the average sentiment of a state.

Issues:
twepy.py breaks because of the producer consumer problem(queenBee.py is slow so the messaging queue runs out of memory)

