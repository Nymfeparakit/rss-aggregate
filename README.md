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
### Usage example
Full api docs are available by endpoints `/docs`.  
In order to use the api, we first need to register a new user:
```
POST /auth/register
{
  "email": "dummy@mail.com",
  "password": "123123",
}
```
Then we can login to get authorization tokens:
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded
username=dummy@mail.com&password=123123&grant_type=password
```
Add rss sources from which the feed will be compiled:
```
POST /sources
{
    "name": "some name",
    "url": "https://example.com"
}
```
In order for the source to appear in the feed, you must also add it to a custom folder. Folders can be used to separate resources according to their topics.
First create folder:
```
POST /folders
{"name": "some folder"}
```
Then we can add this source to the folder, by creating a "folder item":
```
POST /sources/folder-items
{"folder_id": "{created folder id}", "source_id": "{created source id}"}
```
Finally, we can get news from previously created sources via /today endpoint:
```
GET /today
```
### Testing
All tests are located in tests/ directory. You can run them using following command:
```
pytest tests
```
