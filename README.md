# Discovery

A Web Schema Visualization App

## Run a local dev server

1. Install Elasticsearch at localhost:9200 (follow [this instruction](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html))
2. Clone this repo

    ```bash
    git clone https://github.com/biothings/discovery-app.git
    ```

3. Install system packages (on Ubuntu, for example)

    ```bash
    sudo apt install libcurl4-openssl-dev libssl-dev
    ```

4. Change directory to project folder

    ```bash
    cd discovery-app
    ```

5. Install python dependencies

    ```bash
    pip install -r requirements.txt
    ```

6. Create a *config_key.py* under project folder with

    ```bash
    COOKIE_SECRET = '<Any Random String>'
    GITHUB_CLIENT_ID = '<your Github application Client ID>'
    GITHUB_CLIENT_SECRET = '<your Github application Client Secret>'
    ```

    Follow [this instruction](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) to create your Github Client ID and Secret.
7. Run dev server

    ```bash
    python index.py --debug
    ```

You should now be able to access the homepage at <http://localhost:8000/>

## Run in Docker

First refer to step 5 above to setup the credentials required to run the program.
The following commands should be issued under the first level project folder.
Make sure you have port `8000` and `9200` not in use when starting containers.

### Build

```bash
docker-compose up --detach
```

### Stop and restart

```bash
docker-compose stop
docker-compose start
```

### Update codebase

```bash
docker-compose exec web git pull
```

### Remove containers

```bash
docker-compose down
```
