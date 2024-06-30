# parapara-anime
This is a helper for creating a movie of a series of images... Like this!

<!-- The sample image for a behavior of this tool -->
<img src="docs/images/240630_parapara_anime_demo.gif" width="50%" alt="This image show how this tool works!">

## Install

- You can install this package by:
    ```bash
    $ pip install parapara-anime
    ```


## Dependency

- `Xvfb`  
The package `xvfb` is required to use this tool. So please install it like this.
    ```bash
    # Linux
    $ apt -y install --no-install-recommends xvfb
    ```
    Otherwise, you will see the following error...
    ```python
    >>> import parapara
    Traceback (most recent call last):

    ...

    FileNotFoundError: [Errno 2] No such file or directory: 'Xvfb'
    ```


## Contributing

### How to contribute

1. Initialize your development environment by following [the instructions](/docs/DEV_ENVIRONMENT.md).
