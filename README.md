# Install and Run taggle
## Prerequisites
- Python 3.9+
- poetry

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:nikunj92/taggle.git
   cd taggle
   # Install dependencies using poetry (creates .venv)
   poetry install
    ```
   > Note: This project uses in-project virtualenvs via .venv/ (see poetry.toml) -> Given the small size of the project, this felt a good choice. If you want to use a global virtualenv, you can run `poetry config virtualenvs.in-project false` before running `poetry install`.

2. Run the tests:
    ```bash
    poetry run pytest
    ```
   
3. Run the application:
    ```bash
    poetry run taggle
    ```
   

# taggle API Design Document
### Requirements
- Build a minimal RESTful solution to tag a search with an in-memory storage. 
  - The solution should allow users to submit a value (IP, hash, or domain) with optional tags
  - The solution should allow users to query for values based on tags and value
    - This should return a list of values that match the tags and value.
    - The size of the list should be limited if a limit is provided in the query.
  - The service should be able to infer the type of the value based on its format (IP, hash, or domain) and validate it accordingly.

### Optional Requirements
- Data de-duplication
- Helpful error messages for user

### Non-Functional Requirements
- The solution should be built using Litestar
- The solution should have a layered architecture and use DI (Dependency Injection)
- The application should be structured in a way that allows for easy testing and extension
- The solution should be easy to deploy and run.
- The time should be considered, space complexity as well (the solution will use in-memory storage).

> Normally I would consider the volume of data and expected load, but given that I am building a solution using the Litestar framework suggested, I will assume that it can handle the expected load and volume of data.

---

## Solution Overview
Litestar with Provides is used with the following endpoints:
- `POST /submit` - to submit a value with optional tags.
  - This endpoint will accept a JSON payload containing the value and optional tags.
    - See the problem document for the expected JSON structure.
  - The end point will return 200 with the ID of the submitted value.
  - If the value, tag tuple is a duplicate, it will return the existing ID.
  - If the value is invalid (not an IP, hash, or domain), it will return a 400 Bad Request with an error message.
- `GET /data` - to query for values
  - The endpoint will return a list of values that match the tags and value limited by the provided limit.
    - See the problem document for the expected query parameters and response structure.
  - If no values match the query, it will return a 404 Not Found with an error message.
  - If the query parameters are invalid, it will return a 400 Bad Request with an error message.
- Validation is basic, checking if the value is a valid IP, hash, or domain.
  - IP validation uses regex to check for valid IPv4 and IPv6 formats.
  - Hash validation checks for a valid hex string of length 32 (MD5) or 64 (SHA-256).
  - Domain validation checks for a valid domain format.
- Deduplication is handled by checking if the `value` and `tags` tuple already exists in the store before adding a new entry. See discussion on more optimization in a later section.

---

## Implementation Details

### Data Storage
- In-memory store to hold the submitted values and their associated tags.
- A simple DTO-ish (Data Transfer Object) `Item` to represent the data structure.
- The data structure will include:
  - `id`: A unique identifier for the entry.
  - `value`: The submitted value (IP or hash).
  - `tags`: A list of tags associated with the value.
  - `type`: The type of the value (e.g., "ip", "hash", "domain").
- A dictionary maps the `id` to the data structure for quick access.
- A reverse mapping from `value` to `id` to facilitate quick lookups.
- Provides a simple in-memory database with basic `Create` and `Read` operations.

### Code Structure & Responsibilities

* `src/routes.py`: Route definitions, minimal logic, DI endpoints
* `src/services/`: Encapsulates business logic, testable in isolation
* `src/domain/`: Request/response models
* `src/storage/in_memory_db.py`: Naive in-memory DB with value → item list mapping
* `src/dependencies.py`: Declarative DI setup, used in `app.py`

The app was structured to:

* Maintain *separation of concerns*
* Allow *easy test injection* of services or DB
* Stay readable and extensible, even if slightly over-engineered for the scope

--- 

## Testing Plan

### Automated Tests
| Layer          | What is tested                    | Method                                                     |
| -------------- | --------------------------------- | ---------------------------------------------------------- |
| **Routes**     | HTTP response structure & status  | `TestClient` with realistic request payloads               |
| **Service**    | Tag validation, value handling    | Unit test `SubmissionService` and `SearchService` directly |
| **Controller** | Integration of DI + service logic | Functional tests of `/submit` and `/data` endpoints        |
| **Models**     | Schema and behavior               | Implicitly tested via service and route validation         |

> This has been implemented for the most part but I missed out on the error handling tests for the routes. I tested the happy path and some edge cases, but not all error cases. I would have liked to test the error responses more thoroughly if this was a real project.

### Manual Tests
1. Bad requests to `/submit` with invalid values
```bash
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "value": "!!!not-a-valid-value###",
    "tags": ["test", "fail"]
  }'
  
2. Valid request to `/submit` with a value and tags
```bash
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "value": "127.0.0.1",
    "tags": ["local", "loopback"]
    }'
```

3. Valid request to `/submit` without a tag
```bash
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "value": "127.0.0.1",
    "tags": ["local", "loopback"]
    }'
```

4. Valid request to `/data` with a tag
```bash
curl -X GET "http://localhost:8000/data?value=127.0.0.1&tags=local&limit=1"
```

---

## Discussion Points and Some Assumptions

1. **Optimization Discussion**
   In my implementation tag searches and inserts is squared - the search for the index list by value is constant, then we iterate tag lists for the items at those indexes.
   We could make the search and insert constant with a reverse index of tags to values, and value to set of tag sets. There are a couple of ways to do this (some better than others for memory), but the general idea would be we can intersect the value and tag to have a constant search time. Similarly, we can search the tag set to see if the new tag set exists for the given value in constant time.
   However, memory is costly for an in memory db. The reverse index for value to ids takes some memory, but we get a square-ish complexity instead of a cubic-ish one. Happy middle!

2. **Structure Discussion**
   I used litestar as Drew mentioned that it was the actual stack used in the clean sheet build. (Full disclosure - ChatGPT helped me learn and scaffold the missing knowledge and provided some boilerplate to work with).
   I have used Google's guice library for DI in Java, wasn't too hard to figure out Provides in Litestar. Honestly, it's a lot simpler with python!
   Next, the storage is in memory by requirement, so I built insert and select like functionality with the dictionary. Easy to plug in a cold store, or swap out - especially with DI.
   I built two services to expose the functionality to insert and search; and a util package which is just doing validation.
   The current service + DI approach works, but if I was to spend more time, I would add another controller layer - data controller. Move the validation logic in there and expose the search and insert via data controller. Would be more layered.

3. **Early wrong assumption led to the right insight**
   Initially I assumed values should be unique and hold a single list of tags. This meant overwriting existing entries, and implied a `PUT`/`DELETE` model and simplifying the whole problem.
   But then that felt like defeating the point of the challenge, so I went with *values can be repeated* with different tags as the true intent - mainly so that I could architect a system around it.

4. **Case Normalization**
   Values and tags are stored in lowercase.
   This was assumed to be acceptable from a user perspective, but a real system might want to *preserve display case* while normalizing for search.


## The Approach (Informally Documented)
I have left my commit history intact. In a real world project, I would branch off to dev and push to main, but given this was more of a rapid prototyping approach on a greenfield, I went non-standard and pushed to main.

* *Early commits* reflect wrong assumptions — such as treating values as unique and immutable
* Some level of TDD has been followed.
* I was learning Litestar while working on this project, so there is some level of code monkey-ing (with ChatGPT, docs and stack overflow).
* Once the model solidified, I backtracked into *refactor hell* — wiring DI correctly, restructuring to reduce coupling, and getting tests to work consistently. And naming, the engineers' bane!
* DI proved especially subtle with storage state, caught that issue early this morning. I tested the code via tests, but direct testing uncovered some issues. Learnt more about Litestars' db.state.

> !! A glance at the commit history will likely show a very non-linear approach and a lot of jumping around - a reflection of my neurodivergence. I considered squashing it, but then we are who we are, no more no less!

---