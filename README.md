# Discovery
A Web Schema Visualization App 

## Run a local dev server
1. Install Elasticsearch at localhost:9200 (follow [this instruction](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html))
2. Clone this repo
    ```
    git clone https://github.com/biothings/discovery-app.git
    ````
3. Install system packages (on Ubuntu, for example)
    ```
    sudo apt install libcurl4-openssl-dev libssl-dev
    ```
4. Change directory to project folder
    ```
    cd discovery-app
    ```
3. Install python dependencies
    ```
    pip install -r requirements.txt
    ```
4. Change directory to python source folder
    ```
    cd discovery
    ```
5. Create a *config_key.py* under *discovery* folder with
    ```
    COOKIE_SECRET = '<Any Random String>'
    GITHUB_CLIENT_ID = '<your Github application Client ID>'
    GITHUB_CLIENT_SECRET = '<your Github application Client Secret>'
    ```
    Follow [this instruction](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) to create your Github Client ID and Secret.
8. Run dev server
    ```
    python index.py --debug
    ```
You should now be able to access the homepage at http://localhost:8000/
