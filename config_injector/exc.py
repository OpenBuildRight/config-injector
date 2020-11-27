class ConfigError(Exception):
    ...


class ComponentNotFound(ConfigError):
    ...


class KeyNotInConfig(ConfigError):
    ...


class InvalidConfigKey(ConfigError):
    ...


class TypeNotDefined(ConfigError):
    ...


class AppMergeCollisions(ConfigError):
    ...


class InvalidConfigValue(ConfigError):
    ...


class DoesNotSupportBuild(ConfigError):
    ...


class FileTypeNotRecognized(ConfigError):
    ...
