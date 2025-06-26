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

### Assumptions
- We can lower case tags and values - the input case is not significant.

## NOTES 
- Need to ensure validation of IPs, hashes, and domain names.
- Need to store items in a manner that they can be efficiently queried.
- Need to consider time and space as in-memory storage is required.

### Story so far
Simple litestar template with endpoints routes and schemas defined.

