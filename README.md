<img src="https://discovery.biothings.io/dde-logo-o.png" alt="dde" width="100"/>

# Data Discovery Engine

The Data Discovery Engine (DDE) is a project designed to promote the principles of FAIR (Findable, Accessible, Interoperable, Reusable) data sharing practices. Recognizing the importance of well-structured and easily discoverable data in advancing scientific research and technological development, this initiative advocates for the widespread adoption of schema.org schemas. By leveraging schema.org’s rich vocabulary for structured data and providing tools to easily extend this vocabulary to fit your research goals, the project aims to make biomedical research easily finable by humans and machines alike. The DDE does this by providing a comprehensive set of tools for data creators to annotate their datasets effectively, extend schemas easily and share your metadata efficiently. The ultimate goal is adopting FAIR data sharing practices enables data to be easily indexed by search engines like Google. This enhances the discoverability of datasets, making it simpler for researchers, developers, and other stakeholders to find relevant data quickly.

## Getting started

To run the DDE API you will need to create some credentials, this file is not included and must be created by you.
Once that's complete you can choose to run the API with Docker or run the DDE code locally.

At the top level of the repository create a file *config_key.py* with:

    ```bash
    COOKIE_SECRET = '<Any Random String>'
    GITHUB_CLIENT_ID = '<your Github application Client ID>'
    GITHUB_CLIENT_SECRET = '<your Github application Client Secret>'
    ```
    
Follow [this instruction](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) to create your Github Client ID and Secret.

## (Option 1) Run the DDE API in Docker

The following commands should be issued under the first level project folder.
Make sure port `8000` is not in use when starting the containers.

**Note: You can build the complete application with Docker and choose to run the frontend in either development mode or production mode (default). The main difference is that in production mode, the frontend code is not editable, and what you see in the browser reflects a compiled build.**

### Build and start with webapp in production mode. (not editable frontend)

```bash
cd docker
 WEB_APP_MODE=production docker compose up --detach
```

### Build and start with webapp in development mode. (editable frontend)

```bash
cd docker
WEB_APP_MODE=development docker compose -f docker-compose.yml -f docker-compose.override.yml up --detach
```

**NOTE: If at some point you wish to switch from one version to another you must stop the container and remove all images associated and rebuild the project to avoid issues.**

To remove the container and its images run this command:

```bash
docker compose down --rmi all
```


## Additional useful docker compose commands

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


## (Option 2) Run the DDE API locally

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
 
    It's recommended to set up a Python virtual environment first. <add link>

    ```bash
    pip install -r requirements.txt
    ```

 6. Run dev server

    ```bash
    python index.py --debug
    ```

You should now be able to access the homepage at <http://localhost:8000/>



# Running the DDE web application

The web frontend is a server side rendered application built using Nuxt3. 

## Understading how the web application works

A Nuxt3 Web SSR (Server-Side Rendering) application works by running its own Node.js server to handle requests and render pages on the server side. When a user requests a page, the Nuxt3 Node server processes the Vue components, fetches any required data, and generates fully rendered HTML, which is sent to the client. 
Look at the [nuxt 3 documentation](https://v3.nuxtjs.org) to learn more.

## Setup

Go to project folder

note Node version needed.

Make sure to install the dependencies with your preferred method:

```bash
# yarn
yarn install

OR

# npm
npm install

OR

# pnpm
pnpm install --shamefully-hoist
```

## Development Server

Start the development server on http://localhost:3000

```bash
npm run dev
```

## Production

Build the application for production:

```bash
npm run build
```

Locally preview production build:

```bash
npm run preview
```

Checkout the [deployment documentation](https://v3.nuxtjs.org/guide/deploy/presets) for more information.


# Develop with both a dev backend and dev frontend services running together (local setup only)

To test some functionality in the web app the frontend requires authentication and we need the API to handle this without any CORS issues, to do so we need a proxy server to delegate requests to our two running services.

In the production environment, this setup functions as follows: an Nginx server is required to manage incoming HTTP requests and route them appropriately to their respective services. The application architecture consists of two separate servers: one for the backend API, built with Python, typically running on port 8000, and another for the frontend, built with Node.js, running on port 3000. Nginx acts as a reverse proxy, directing requests to the correct service based on the URL path or other routing rules. This setup ensures efficient request handling, load balancing, and secure communication between the frontend and backend services.

## Step 1. Run the API and web app

Run both services locally as described above. If you chose to run all services through Docker: Docker will run all the services needed. Please refer to the instructions above for that configuration.

## Step 2. Run Nginx

Run Nginx with the configuration file [here](https://github.com/biothings/discovery-app/blob/main/docker/nginx_conf.d/discovery-app.conf).

## Step 3. Ready to dev

You should now be able to access both services at <http://localhost/>


# Related Projects

## BioThings Schema Package

```biothings_schema``` is a Python package for the creation, extension and exploration of the schemas defined using the schema.org standard.

https://github.com/biothings/biothings_schema.py