# Initialize Development Environment

## 1. Prerequisites

- Docker
- Docker Compose

## 2. Steps

1. Folk this repository

2. Clone your folked repository

    ```bash
    git clone {Your repository URL}
    ```

3. Move to the `docker/python-env/` directory of the repository

    ```bash
    cd parapara-anime/docker/python-env/
    ```

4. Copy the `.env.sample` file to `.env`

    ```bash
    cp .env.sample .env
    ```

    Then, edit the `.env` file to set the environment variables.

5. Prepare the Docker container

    ```bash
    docker compose build
    docker compose up -d
    ```

    - Then, you can access the Jupyter Notebook server at `http://localhost:{JUPYTER_PORT}`.
    - `JUPYTER_PORT` is specified in the `.env` file.
    - The default **password** of the Jupyter Notebook server is `demo` which is also specified in the `.env` file.

6. Import `parapara`

- You can load this library like this.

    ```bash
    docker compose exec python-env bash
    # python

    >>> import parapara
    >>>
    ```

- Of course, you can also use it in Jupyter Notebook.

    ```
    # In Jupyter Notebook, this is OK !
    import parapara
    ```
