# Picnic Assignment: Ivan Nikiforov

_Please explain your solution in this file._

The solution is pretty straightforward:
* CLI app that accepts some arguments from user on its launch. If used docker-compose, the arguments could be specified in `docker-compose.yml` file `command` section, for example `command: ["100", "30", "-o=output_file.json", "-r=0"]` means the app settings `run at most 100 messages; or at most 30 seconds; write result to output_file.json; request the server indefinitely until one of the aforementioned conditions happens.`
* Depending on the app settings, the app will run one or more times following workflow:
    1. GET data from target URL
    2. Parse server response
    3. Process events
    4. Sort processed events data
    5. Serialize sorted events data
    6. Write result in a dedicated file.
* The app code splitted across several modules:
    1. `__main__.py` - entrypoint. Contains single `entry()` function that takes cares of getting app settings and invocation of `handle_continuous_run` function (a manager function that in loop handles all the single runs).
    2. `cli.py` - a module that handles registering CLI arguments.
    3. `constants.py` - a module that contains some constants app use (DEFAULT_SERVER_URL, etc.)
    4. `model.py` - main app module containing business logic (aforementioned `handle_continuous_run` function, and auxiliary functions for requesting, parsing, filtering and aggregating data).

### Extra: Feedback on the assignment

_If you wish to give feedback on the assignment._
