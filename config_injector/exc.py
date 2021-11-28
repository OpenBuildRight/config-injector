class ConfigError(Exception):
    ...


class ComponentNotFound(ConfigError):
    ...


class KeyNotInConfig(ConfigError, ValueError):
    ...


class InvalidConfigKey(ConfigError, ValueError):
    ...


class TypeNotDefined(ConfigError):
    ...


class AppMergeCollisions(ConfigError):
    ...


class InvalidConfigValue(ConfigError, ValueError):
    ...


class DoesNotSupportFill(ConfigError):
    ...


class FileTypeNotRecognized(ConfigError):
    ...


class EnvironmentVariableNotFound(ConfigError, ValueError):
    def __init__(self, *args, variable_name=None):
        super().__init__(*args)
        self.variable_name = variable_name
