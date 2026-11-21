"""Custom exceptions, so the API can turn each kind of failure into a clear HTTP answer.

    ConfigurationError -> 503  (a config is missing, e.g. no API_KEY, no index ID)
    IngestionError     -> 422  (the file could not be read or indexed)
"""


class RawRagError(Exception):
    """Base class for every error this app raises on purpose."""


class ConfigurationError(RawRagError):
    """A required setting is missing or the selected APP_MODE cannot start."""


class IngestionError(RawRagError):
    """A document could not be loaded, chunked or indexed."""