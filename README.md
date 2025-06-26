# taggle
A minimal RESTful solution to tag a search with an in memory storage

# API Design Document
## Requirements
TODO consider a better structure for requirements 
### Given requirements
- Implement a minimal REST API
  - Support `POST` at `/submit`
    - Endpoint accepts a JSON payload
      - Schema requires `value` - valid IPs or valid hash values.
      - Contains optional `tags`
      - Example query POST /submit
      - ```json
        {
          "value": "example.org",
          "tags": ["world", "hello"]
        }
        ```
    - Endpoint responses:
      - HTTP 201 with generated `id` if successful.
      - HTTP 400 if validation fails.
      - HTTP 500 if an unexpected error occurs.

  - Support queries to `GET` at `/data`
    - Query parameters:
      - `value` - valid IPs or valid hash values.
      - `tags` - optional, comma-separated list of tags.
      - `limit` - optional, integer to limit results.
    - Responses:
      - HTTP 200 with a JSON array of matching items. e.g.: GET /data?q=aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d&tags=foo,world&limit=5
        ```json
        [
          {
            "value": "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",
            "tags": ["world", "hello"],
            "type": "hash"
            }
        ]
        ```
      - Possible HTTP 404 if no items match the query.
      - HTTP 500 for unexpected errors.



### Bonus Requirements
- Data de-duplication
- Helpful error messages for user
## Implementation Details

### Endpoints
As provided in the requirements, we will implement two endpoints:
- `POST /submit` - to submit a value with optional tags.
- `GET /data` - to query for values based on tags and value.
- We will use Litestar to implement the endpoints.

### Data Storage
- We will use an in-memory store to hold the submitted values and their associated tags.
- We will create a simple DTO (Data Transfer Object) to represent the data structure.
- The data structure will include:
  - `id`: A unique identifier for the entry.
  - `value`: The submitted value (IP or hash).
  - `tags`: A list of tags associated with the value.
  - `type`: The type of the value (e.g., "ip", "hash", "domain").
- The in-memory store will be a dictionary where the key is the `value` in our DTO. 
  - I could combine it with `id` if I wanted to allow multiple entries with the same value but different tags.
  - However, I clarify in my assumptions why I think this is not necessary.

### Assumptions
- We can lower case tags and values - the input case is not significant.
- Deduplication
  - If the value exists with the same tags, we shall return the existing ID.
  - Throw an error if the value already exists with different tags
    - Starting with a simple check for the value in the in-memory store to avoid duplicates.
    - Assuming that we would extend with a `PUT` and `DELETE` endpoint later so a simple check for the value is sufficient for now.
  - Other options
    - We could do a composite key of `value` and `tags`.
      - This would allow us to have multiple entries with the same value but different tags.
    - We could change the tags on resubmission
      - This is a `PUT` so I would push back if someone wanted to do this.

- [TODO] this uncovered a misunderstanding of the requirements
  - We need to allow multiple entries with the same value but different tags.
  - Need to reconsider the data structure - a simple idea would be to use additional memory - store value to ids.
    
## NOTES 
- Need to ensure validation of IPs, hashes, and domain names.
- Need to store items in a manner that they can be efficiently queried.
- Need to consider time and space as in-memory storage is required.

### Story so far
Simple litestar template with endpoints routes and schemas defined.
added basic tests for the endpoints.

