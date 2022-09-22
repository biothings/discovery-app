"""
    SAML based SSO using python3-saml.

    Require settings.json and advanced_settings.json under this folder.
    See configuration details: https://github.com/onelogin/python3-saml

"""
import json
import logging
import os

import tornado.httpserver
import tornado.httputil
import tornado.ioloop
import tornado.web
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from tornado.log import enable_pretty_logging


class SAMLBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        session = self.get_saml_session()
        return session.get("samlNameId")

    def get_saml_session(self):
        try:
            session_ = self.get_secure_cookie("session")
            session = json.loads(session_)
            return session
        except Exception:
            return {}


class SAMLUserHandler(SAMLBaseHandler):
    def get(self):

        resposne = {}
        if self.current_user:
            resposne["login"] = self.current_user
            resposne["session"] = self.get_saml_session()

        self.finish(resposne)


class SAMLLoginHandler(SAMLBaseHandler):
    def get(self):
        req = prepare_tornado_request(self.request)
        auth = init_saml_auth(req)
        return self.redirect(auth.login(self.get_argument("next", "/")))


class SAMLACSHandler(SAMLBaseHandler):
    def post(self):
        req = prepare_tornado_request(self.request)
        auth = init_saml_auth(req)
        auth.process_response()
        errors = auth.get_errors()

        logging.info("-acs-")

        if len(errors) == 0:
            session = {}
            session["samlUserdata"] = auth.get_attributes()
            session["samlNameId"] = auth.get_nameid()
            session["samlSessionIndex"] = auth.get_session_index()
            ###
            self.set_secure_cookie("session", json.dumps(session))
            ###
            if "RelayState" in self.request.arguments:
                redirect_url = self.request.arguments["RelayState"][0].decode("utf-8")
                if "/saml/acs" not in redirect_url:  # prevent self redirection
                    return self.redirect(redirect_url)

        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()
            self.write(error_reason)


class SAMLLogOutHandler(SAMLBaseHandler):
    def get(self):

        req = prepare_tornado_request(self.request)
        auth = init_saml_auth(req)

        name_id = None
        session_index = None
        session = self.get_saml_session()
        if "samlNameId" in session:
            name_id = session["samlNameId"]
        if "samlSessionIndex" in session:
            session_index = session["samlSessionIndex"]
        return self.redirect(
            auth.logout(
                self.get_argument("next", "/"), name_id=name_id, session_index=session_index
            )
        )


class SAMLSLSHandler(SAMLBaseHandler):
    def get(self):

        req = prepare_tornado_request(self.request)
        auth = init_saml_auth(req)
        error_reason = None
        errors = []

        logging.info("-sls-")

        def dscb():
            return self.clear_cookie("session")  # clear out the session

        url = auth.process_slo(delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return self.redirect(url)
            else:
                self.redirect(self.get_argument("next", "/"))
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()
            self.finish(error_reason)


class MetadataHandler(SAMLBaseHandler):
    def get(self):
        req = prepare_tornado_request(self.request)
        auth = init_saml_auth(req)
        saml_settings = auth.get_settings()
        metadata = saml_settings.get_sp_metadata()
        errors = saml_settings.validate_metadata(metadata)

        if len(errors) == 0:
            self.set_header("Content-Type", "text/xml")
            self.write(metadata)
        else:
            self.write(", ".join(errors))


def prepare_tornado_request(request):

    dataDict = {}
    for key in request.arguments:
        dataDict[key] = request.arguments[key][0].decode("utf-8")

    result = {
        "https": "on" if request.protocol == "https" else "off",
        "http_host": tornado.httputil.split_host_and_port(request.host)[0],
        "script_name": request.path,
        "server_port": tornado.httputil.split_host_and_port(request.host)[1],
        "get_data": dataDict,
        "post_data": dataDict,
        "query_string": request.query,
    }
    return result


SAML_PATH = os.path.dirname(__file__)


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=SAML_PATH)
    return auth
