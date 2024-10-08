<img src="https://discovery.biothings.io/dde-logo-o.png" alt="dde" width="100"/>

# Data Discovery Engine

The Data Discovery Engine (DDE) is a project designed to promote the principles of FAIR (Findable, Accessible, Interoperable, Reusable) data sharing practices. Recognizing the importance of well-structured and easily discoverable data in advancing scientific research and technological development, this initiative advocates for the widespread adoption of schema.org schemas. By leveraging schema.org’s rich vocabulary for structured data and providing tools to easily extend this vocabulary to fit your research goals, the project aims to make biomedical research easily finable by humans and machines alike. The DDE does this by providing a comprehensive set of tools for data creators to annotate their datasets effectively, extend schemas easily and share your metadata efficiently. The ultimate goal is adopting FAIR data sharing practices enables data to be easily indexed by search engines like Google. This enhances the discoverability of datasets, making it simpler for researchers, developers, and other stakeholders to find relevant data quickly.

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

First refer to step 6 above to setup the credentials required to run the program.
The following commands should be issued under the first level project folder.
Make sure you have port `8000` not in use when starting containers.

### Build

```bash
cd docker
docker compose up --detach
```

### Stop and restart

```bash
docker compose stop
docker compose start
```

### Update codebase

```bash
docker compose exec web git pull
```

### Remove containers

```bash
docker compose down
```

# Related Projects

## BioThings Schema Package

biothings_schema is a Python package for the creation, extension and exploration of the schemas defined using the schema.org standard.

https://github.com/biothings/biothings_schema.py
