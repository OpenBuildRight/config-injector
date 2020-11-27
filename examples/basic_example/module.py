from typing import Text, SupportsInt
from urllib.parse import urlsplit
from config_injector import config, Injector
from pathlib import Path
import os


class Host:
    def __init__(
        self,
        scheme,
        host,
        database,
        port = None,
        username = None,
        password = None
    ):
        self.scheme = scheme
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

    def __str__(self):
        user = self.username if self.username else ""
        user += f".{self.password}" if self.password else ""
        user += "@" if user else ""
        port = f":{self.port}" if self.port else ""
        return f"{self.scheme}://{user}{self.host}{port}/{self.database}"

    def __repr__(self):
        if self.password:
            args = {k: v for k, v in self.__dict__.items()}
            args["password"] = "*" * len(self.password)
            return str(self.__class__(**args))
        else:
            return self.__str__()


class DatabaseController:
    def __init__(self, host: Host, option_1: SupportsInt, option_2: Text):
        self.host = host
        self.option_1 = option_1
        self.option_2 = option_2

    def __str__(self):
        return f'{type(self)}({", ".join([f"{k}={v}" for k, v in vars(self)])})'

    def __repr__(self):
        return f'{type(self)}({", ".join([f"{k}={repr(v)}" for k, v in vars(self)])})'


@config(url=str, username=str, password=str, database_name=str, port=int)
def database(url, username, password, database_name, port) -> Host:
    """
    User configuration layer factory function with validation and input processing.
    """
    url_parts = urlsplit(url)
    if url_parts.scheme not in ("mysql", "sqlite", "mssql"):
        raise ValueError(f"Scheme {url_parts.scheme} not supported")
    return Host(
        url_parts.scheme,
        url_parts.netloc,
        database=database_name,
        port=port,
        username=username,
        password=password,
    )


# Notice that this is NOT the same as type hints. Specify the function you want to use
# for construction, not the resulting type.
@config(host=database, option_1=str, option_2=int)
def database_controller(host: Host, option_1: Text, option_2: SupportsInt) -> DatabaseController:
    return database_controller(host, option_1, option_2)


def create_controller() -> DatabaseController:
    injector = Injector()
    injector.load_file(Path(__file__).parent / "config.yaml")
    controller_injector = injector["app"]["controller"]
    controller_injector["host"]["username"] = os.getenv("APP_USER", "default_username")
    controller_injector["host"]["password"] = os.getenv("APP_PASSWORD", "default_password")
    return controller_injector.instantiate(database_controller)
