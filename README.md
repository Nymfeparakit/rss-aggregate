# rss-aggregate
API for creating rss feeds from various rss sources
## Running
To run API locally, the following env variables should be specified via .env file:
* POSTGRES_DB
* POSTGRES_USER
* POSTGRES_PASSWORD
* POSTGRES_HOST
* JWT_SECRET
* RESET_PWD_SECRET
* VERIFICATION_TOKEN_SECRET
### Running with docker
After all varibles were specified, we can run api with the following command:
```
docker-compose up
```
### Stack
* `FastAPI`
* `aiohttp` for making asynchronous requests to rss sources
* `asyncpg`
### Testing
All tests are located in tests/ directory. You can run them using following command:
```
pytest tests
```
