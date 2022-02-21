""" Tornado Web Handlers """

from .base import HANDLERS as BASE_HANDLERS
from .oauth import HANDLERS as OAUTH_HANDLERS
from .saml import HANDLERS as SAML_HANDLERS
from .templates import HANDLERS as TPL_HANDLERS
from .templates import TemplateHandler

HANDLERS = [
    *BASE_HANDLERS,
    *SAML_HANDLERS,
    *OAUTH_HANDLERS,
    *TPL_HANDLERS
]
