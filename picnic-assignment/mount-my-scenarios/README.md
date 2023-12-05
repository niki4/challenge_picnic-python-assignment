# Mounted Scenarios

In this assignment, we give you the possibility to add your own **Scenarios** to help
you in testing your solution. Any file with the extension `.scenario` will count toward
a potential **Scenario** that the **Server** could respond to your **Client**.

Feel free to provide us with any extra **Scenario** that you may have written and used.

## What does the Server do?

### Server

When polled, it will play out a **Scenario**, in a stream. Several **Scenarios** can be
loaded by the **Server** and they will be played out in a [round-robin] manner. Once all
**Scenarios** have been played out, it starts a new cycle.

This gives the guarantee that every time the **Server** receives a request, it can serve
a **Scenario**.

### Scenario

A **Scenario** is represented in a `*.scenario` file and contains a series of
**Actions**. Each **Action** is played sequentially, until all **Actions** have been
played. When this happens, the **Server** closes the stream.

### Action

An action contains two parts: a **verb** and a **payload**. It is defined in a
`*.scenario` file in the following manner:

```shell
{VERB} {payload (bytes)}\n
```

#### Possible Actions

- `SLEEP {N: float}`: Sleep for `N` seconds.
- `SEND {M: bytes}`: Send the message `M`.
- `# Comment` and `// Comment`: A comment line (no operation).
- `LOG {M: bytes}`: Log (`info`) the message `M`.
- `LOG {L: str} {M: bytes}`: Log (`level L`) the message `M`.
  - The possible levels `L` are the ones from [logging][logging].

### Example Scenario

```
SLEEP 0.5
SEND message 1
SEND message 2
SLEEP 1
SEND message 3
SLEEP 1
SEND message 4
```

This **Scenario** will take about 2.5 seconds to complete and send 4 different messages
before closing the stream.

[logging]: https://docs.python.org/3.10/library/logging.html#logging-levels
[round-robin]: https://en.wikipedia.org/wiki/Round-robin_item_allocation
