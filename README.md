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
- We will use a dictionary to map the `id` to the data structure for quick access.
- We will also maintain a reverse mapping from `value` to `id` to facilitate quick lookups and deduplication.

### Assumptions
- We can lower case tags and values - the input case is not significant.
    
## NOTES 
- Need to ensure validation of IPs, hashes, and domain names.
- Need to consider time and space as in-memory storage is required.

### Story so far
Simple litestar template with endpoints routes and schemas defined.
added a simple in-memory storage for the data.
added a simple deduplication mechanism.
added validation for IPs, hashes, and domain names.
added services to add and query data.

TODO
review the code and add tests tomorrow before submitting.