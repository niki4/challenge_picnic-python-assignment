# Picnic Recruitment Task

Please read the following instructions carefully and make sure that you fulfill all
requirements listed.

## Overview

This is a Python programming assignment we've created specifically for our recruitment
process. It's a project in a Git repository hosted on GitHub. You were given a link to
GitHub, and when you visited that link, it created a private fork of this repository.
Only you and developers at Picnic can see the code you push to this repository.

High-level instructions:

1. Read and follow the task specified below.
2. Make a local clone of this repository on your machine, and do your work on a branch
   other than `master`. Do not make any changes to the `master` branch.
3. Push your changes as frequently as you like to `origin/your-branch-name`, and create
   a pull request to merge your changes back into the `master` branch. Don't merge your
   pull request. Once you're finished with the assignment, we will do a code review of
   your pull request.
4. When you're finished, [create and add][github-labels] the label `done` to your pull
   request. This will notify us that your code is ready to be reviewed. Please do
   **NOT** publish your solution on a publicly available location (such as a public
   GitHub repository, your personal website, _et cetera_). Also, please refrain from
   tagging or assigning specific Picnic employees as reviewers of your PR; we have an
   internal round-robin system to determine who will review your code.

This process closely mimics our actual development and review cycle. We hope you enjoy
it!

## Context

In a nutshell, the assignment revolves around reading JSON events when polling a
**Server**, processing them, and writing the result to a desired output file.

The input event stream comprises "pick events"; each of these events represents the
action of a warehouse employee fulfilling a customer order ("picking" an item off a
shelf).

- No assumptions should be made about the speed at which events arrive. Multiple events
  may arrive in brief succession, but it could also be that no events arrive for
  extended periods of time.
- Each event adheres to the JSON format described below.
- Each event comprises a single line of JSON.
- Events are separated by a newline (`'\n'`).
- If no events are sent for a while, `keep-alive` messages consisting of a single `'\n'`
  may be sent.

## Provided Functionality

The provided code is structured as follows:

- The source of the implementation is in `picnic-assignment/src` and in the module
  `picnic.assignment`. A few things to be noted:
  - Function `entry` in `__main__.py` is the entry point.
  - You are provided with some example files, such as `constants.py` but you are free
    and expected to reorganize things your way.
- The tests are in `picnic-assignment/tests`. If you wish to add several types of tests,
  feel free to create new subdirectories. In `tests` you'll find a subdirectory:
  - `resources/`: Resources used for testing.
- `mount-my-scenarios/`: This will be mounted as a volume to the **Server**. You can add
  new **Scenarios**, and they will be picked up. More details can be found
  [here][scenarios].
- `picnic-assignment/pyproject.toml`: This file contains build system requirements and
  information, which are used by [pip][pip] to build the package. If you prefer to use
  some different build system, this file can even be deleted!
  - Some optional dependencies are already defined for testing. You can add more.
  - This is where you'll add your project dependencies.
- `picnic-assignment/README.md`: Use this file to explain your solution to us.
- `Dockerfile`: This file _can_ be greatly improved. Some choices are very naive and
  suboptimal. In order to make sure that we can reproduce your environment as close as
  possible, feel free to change it to suit your needs. This gives you an idea of how
  your solution will be run on our systems. If you want to make sure it runs on our
  side, you **must** have a buildable `Dockerfile`.
- `docker-compose.yml`: This runs both your **Client** and our **Server** in the same
  network. If running `docker compose up --build` works, you're on the right track!
- Under `tests/unit`, a disabled test is defined. Consider getting it to pass ;).

### Pick event type specification

|    Field    |  Type   |                                            Description                                             |
| :---------: | :-----: | :------------------------------------------------------------------------------------------------: |
|    `id`     | String  |                                        A unique identifier                                         |
| `timestamp` | String  | The time at which the event was emitted; formatted as an [ISO 8601][iso-8601] UTC date-time string |
|  `picker`   | Object  |                                      Picker object, see below                                      |
|  `article`  | Object  |                                     Article object, see below                                      |
| `quantity`  | Integer |                                   The number of articles picked                                    |

### Picker type specification

|     Field      |  Type  |                                                Description                                                 |
| :------------: | :----: | :--------------------------------------------------------------------------------------------------------: |
|      `id`      | String |                                            A unique identifier                                             |
|     `name`     | String |                                             The person's name                                              |
| `active_since` | String | The time the picker clocked in to start working; formatted as an [ISO 8601][iso-8601] UTC date-time string |

### Article type specification

|       Field        |  Type  |           Description           |
| :----------------: | :----: | :-----------------------------: |
|        `id`        | String |       A unique identifier       |
|       `name`       | String | An English, human-readable name |
| `temperature_zone` | String |  Either `ambient` or `chilled`  |

### Example input event JSON representation

The following JSON object is an example of the kind of event that may be received from
polling the **Server**. Note how it matches the specification above. There is one
difference: you may assume that the received events are comprised of a single line.
(i.e., they are not formatted.)

```json
{
  "timestamp": "2018-12-20T11:50:48Z",
  "id": "2344",
  "picker": {
    "id": "14",
    "name": "Joris",
    "active_since": "2018-12-20T08:20:15Z"
  },
  "article": {
    "id": "13473",
    "name": "ACME Bananas",
    "temperature_zone": "ambient"
  },
  "quantity": 2
}
```

## Task

We would like you to create a pull request that implements the functionality listed
below.

- A CLI `event-process` with _at least_:
  - Two positional arguments:
    - `0`: Max events (`int`), a sufficient condition to stop a run;
    - `1`: Max time (`float`), in seconds, a sufficient condition to stop a run.
  - Two options:
    - `-o/--output-file` (`str`), path to the output result. \
      Default: `picnic-assignment/output-%run_id%.json`, where `%run_id%` is the number of
      the run (0, 1, 2, ..., r-1).
    - `-r/--runs` (`int`), how many times the **Client** calls the **Server**. \
      Default: `1`. \
      Special value: `0`: Indefinitely.
- The following Environment variable:
  - `PICNIC_SERVER_URL`: The API endpoint of the Picnic Server. \
    Default: `http://localhost:80`.
- The CLI respects the given `max_events` and `max_time`. For example,
  `event-process 100 30` returns after reading at most 100 events or after 30 seconds,
  whichever condition is met first.
- Each execution should process the events it receives as follows:
  - Only pick events corresponding to picks of `ambient` articles are retained. (Picks
    of `chilled` articles do count towards the `max_events` limit but are otherwise
    ignored.)
  - Events must be grouped by `picker`.
  - Pickers must be sorted chronologically (ascending) by their `active_since`
    timestamp, breaking ties by ID.
  - The picks per picker must also be sorted chronologically, ascending. (Note that
    events may not _arrive_ in chronological order!)
  - The article names should be uppercase.
- The result of the aforementioned filter, group and sort operations must be written to
  the provided output file according to the following JSON format:
  ```json
  [
    {
      "picker_name": "Joris",
      "active_since": "2018-09-20T08:20:00Z",
      "picks": [
        {
          "article_name": "ACME BANANAS",
          "timestamp": "2018-12-20T11:50:48Z"
        },
        ... more picks here ...
      ]
    },
    ... more pickers here ...
  ]
  ```

For a complete example of expected input and corresponding output, compare the contents
of the following two provided files:

- [happy-path-input.json-stream][json-happy-input]
- [happy-path-output.json][json-happy-output]

## Notes

- Feel free to add/modify dependencies in `pyproject.toml`.
- Any file can be modified / deleted, as long as there are still the following entry
  points:
  - _Docker:_ the initial `docker-compose.yml` would still execute properly, if it were
    still there;
  - _Shell:_ the aforementioned `event-process` CLI exists and is path agnostic;
  - _Python:_ the function at `picnic.assignment.__main__:entry` executes the task with
    no arguments.
- Please state your **full name** in the title of the pull request.
- When you're done, notify the recruiter via email as mentioned in the email you 
  received.

## Tips

- We value clean, readable, modern, and idiomatic Python. Your code will be reviewed by
  other developers, so make sure it is easy to follow and well-structured.
- Avoid doing manual JSON parsing. It's prone to errors and hard to read.
- Don't feel the need to over-engineer your solution. We don't expect you to build an
  entire system that can scale to billions of events. Your solution should be tailored
  to the problem statement. We prefer concise and simple solutions over lengthy ones.
  However, it should be straightforward to let the program behave differently, such as
  have a different timeout, filter on a different temperature zone, etc...
- It should really not be necessary to write more than, say, 500 lines of non-test code.
  (And in fact, it is possible to write a "perfect" solution using much less code than
  that.)

[iso-8601]: https://en.wikipedia.org/wiki/ISO_8601
[pip]: https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/
[github-labels]: https://help.github.com/articles/about-labels
[scenarios]: picnic-assignment/mount-my-scenarios/README.md
[json-happy-input]: picnic-assignment/tests/resources/happy-path-input.json-stream
[json-happy-output]: picnic-assignment/tests/resources/happy-path-output.json
