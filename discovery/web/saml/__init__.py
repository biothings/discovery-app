"""
    SAML based SSO.

    Require settings.json and advanced_settings.json under this folder.
    See configuration details: https://github.com/onelogin/python3-saml

"""
import os

SAML_PATH = os.path.dirname(__file__)

try:
    from .handlers import *
except ImportError:
    SAML_HANDLERS = []
else:
    SAML_HANDLERS = [
        (r"/saml/", SAMLUserHandler),
        (r"/saml/login/?", SAMLLoginHandler),
        (r"/saml/acs/?", SAMLACSHandler),
        (r"/saml/logout/?", SAMLLogOutHandler),
        (r"/saml/sls/?", SAMLSLSHandler),
        (r"/saml/metadata/?", MetadataHandler),
    ]
