import shutil


# TODO: write unittest
def check_package_existence(required_package: str) -> None:
    """
    Check if the required package is installed on the system.
    Raises an error if the specified package is not found.
    """
    if shutil.which(required_package) is None:
        raise RuntimeError(
            f"The '{required_package}' command was not found. Please install it before running this program."
        )
