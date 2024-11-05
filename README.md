# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a
> VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter).
> Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies.
To prepare your system, ensure you have an official distribution of Python version 3.8+
and install Poetry using one of the following commands
(as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before
poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies.
To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options.
This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`.
This enables things like development mode (which also enables features like hot reloading when you make a file change).

### MongoDB

The `.env` file also includes environment variables required to connect to a mongodb instance.
This variable has deliberately been left blank in the `.env.template` file.

## Running the App

Once all the dependencies have been installed, start the Flask app in development mode within the Poetry environment by
running:

```bash
$ poetry run flask run
```

You should see output similar to the following:

```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the Tests

The project uses pytest to run tests. To run the tests, run the following from your preferred shell:

```bash
$ poetry run pytest
```

## Provisioning a VM from an Ansible Control Node

1. SSH into the control node
2. Copy the `ansible` directory to the control node
3. Replace the IP address in the `inventory` file with the IP address(es) of the managed VM(s)
4. Create a file `ansible-pw.txt` containing the vault password
5. Run the following command in the `ansible` directory, to provision the VM:
   ```bash
   $ ansible-playbook playbook.yml -i inventory --vault-password-file ansible-pw.txt
   ```

### Note on env variables

The ansible configs contained in this repo contain the encrypted env values required to run the app.
These values can be seen in the `ansible/vars/env.yml` file.

The values are individually encrypted using ansible-vault and added to the file.

To generate a new encrypted value or to replace one of the provided values:

```bash
$ ansible-vault encrypt_string --vault-password-file your_password_file --name '<key_name>'
```

then enter the value you want to encrypt when prompted.

## Docker

Run the project with mounting:

```bash
docker build --target development --tag todo-app:dev .
docker run -dit \
    --name todo-app-dev \
    -p 8000:8000 \
    --env-file .env \
    --mount type=bind,source="$(pwd)/todo_app",target=/app/todo_app,readonly \
    todo-app:dev
```

Run tests:

```bash
docker build --target test --tag todo-app:test .
docker run -it \
    --env-file .env.test \
    todo-app:test
```

Run the project in production environment:

```bash
docker build --target production --tag todo-app:prod .
docker run -dit \
    --name todo-app-prod \
    -p 8000:8000 \
    --env-file .env \
    todo-app:prod
```

## Deployment

### Building the Docker image

1. Logging into DockerHub locally, with `docker login`
2. Building the image, with `docker build --target production --tag <user_name>/todo-app:prod .`
3. Pushing the image, with `docker push <user_name>/todo_app:prod`

### Deploying to Azure App Services

1. First create an App Service Plan:
   `az appservice plan create --resource-group <resource_group_name> -n <appservice_plan_name> --sku B1 --is-linux`
2. Then create the Web App:
   `az webapp create --resource-group <resource_group_name> --plan <appservice_plan_name> --name <webapp_name> --deployment-container-image-name docker.io/<user_name>/todo-app:prod`
3. Set up environment variables individually via
   `az webapp config appsettings set -g <resource_group_name> -n <webapp_name> --settings FLASK_APP=todo_app/app`
4. The app should now be deployed to `http://<webapp_name>.azurewebsites.net/`

### Update the image

When the image is updated and pushed to DockerHub, run `curl -x POST '<webhook>'`.
The webhook URL can be found under Deployment Center on the app service's page in the Azure portal

## Security

### Encryption in transit

We are enforcing HTTPS with Azure App service.

### Encryption at rest

Azure Cosmos DB is encrypted at rest and in transport.
See https://learn.microsoft.com/en-us/azure/cosmos-db/database-encryption-at-rest for more details.
