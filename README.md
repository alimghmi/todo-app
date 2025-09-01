# Clean Architecture

## The Big Picture

-   **Keep the core pure.**
    Business rules live in the center (entities + use cases).
    They don't know anything about frameworks, databases, or UIs.

-   **Everything points inward.**

    -   UI depends on use cases.
    -   Use cases depend on entities.
    -   Entities depend on nothing.
        Never let it leak the other way.

-   **Frameworks are details.**
    SQLite, FastAPI, CLI, whatever → all replaceable. Don't marry your
    business logic to them.

------------------------------------------------------------------------

## Layers (how I think of them)

1.  **Entities (Domain)**
    -   The rules of my world.
    -   Example: `Task` must have a title, has a done flag, created_at
        timestamp.
    -   No DB calls, no print statements. Just data + invariants.
2.  **Use Cases (Application)**
    -   The actions the system supports.
    -   Example: "create a task", "mark done", "rename".
    -   They use entities and call repositories. They *decide what
        should happen*.
3.  **Interfaces (Contracts)**
    -   Abstract classes that define the boundaries.
    -   Example: `TaskRepository` with `add`, `get`, `list`, `save`,
        `delete`.
    -   Inner layers declare *what they need*. Outer layers implement
        it.
4.  **Adapters (Infrastructure)**
    -   Concrete details.
    -   Example: `InMemoryRepo`, `SQLiteRepo`, `CLI`, `FastAPI`.
    -   They "adapt" the outside world to the inside.

------------------------------------------------------------------------

## Golden Rules I Need to Remember

-   **Don't let details leak inward.**
    Use cases should never import `sqlite3` or `fastapi`.
    They only know about interfaces and entities.

-   **Keep use cases pure.**
    They return data or errors. No I/O, no logging, no frameworks.

-   **Repositories are dumb.**
    They just store and fetch. No business decisions inside them.

-   **Data in, data out.**
    Use simple dataclasses or DTOs. Don't pass ORM models or HTTP
    objects around.

-   **Errors matter.**
    Raise domain-specific errors like `TaskNotFoundError` instead of
    generic stuff.
    Let adapters turn those into `404` or CLI messages.

-   **Close to the user, not the core.**
    All wiring (which repo to use, which framework to run) happens at
    the edge, not inside the domain.

-   **Test the core in isolation.**
    Entities and use cases should be easy to unit test without setting
    up databases or servers.

-   **Think replaceable.**
    If I can swap SQLite for Postgres, or CLI for FastAPI, without
    touching entities/use cases → I did it right.

------------------------------------------------------------------------

## Mental Shortcuts

-   **Entities = nouns.** Tasks, Users, Orders.
-   **Use cases = verbs.** Create task, Complete task, Reopen task.
-   **Interfaces = promises.** "If you give me a repo that has
    add/get/save/delete, I don't care how it works."
-   **Adapters = hacks to reality.** SQLite, HTTP, CLI, etc.

------------------------------------------------------------------------

## Tips & Tricks

-   Use **dataclasses** for entities --- simple, readable, no
    boilerplate.
-   Store dates as **ISO strings** in DB for portability.
-   Make **delete** idempotent: deleting twice shouldn't crash.
-   Favor **immutability** (return new Task instead of mutating) ---
    fewer bugs.
-   Always have a **composition root** (the place where you decide
    "today we use SQLite + FastAPI").
-   Don't over-engineer: a TODO app is small, but practicing the
    boundaries pays off in big apps.
-   When in doubt, ask: *"Can I swap this part out easily?"* If not, the
    dependency might be wrong.

------------------------------------------------------------------------

## Visual Reminder

    [ CLI / API / UI ]  -->  [ Use Cases ]  -->  [ Entities ]
           |                        |              |
    [ Memory Repo / DB ] -----------+--------------+

Everything flows inward. Core doesn't know who is calling it.

------------------------------------------------------------------------

## Why this matters

-   Less stress when requirements change.
-   Easier to test.
-   Freedom to swap tech (databases, frameworks, UIs).
-   Code stays readable and doesn't tangle up.
