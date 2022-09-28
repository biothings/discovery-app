""" Tornado Web Handlers """

from .base import HANDLERS as BASE_HANDLERS
from .oauth import HANDLERS as OAUTH_HANDLERS
from .saml import HANDLERS as SAML_HANDLERS

HANDLERS = [
    *BASE_HANDLERS,
    *SAML_HANDLERS,
    *OAUTH_HANDLERS,
]
