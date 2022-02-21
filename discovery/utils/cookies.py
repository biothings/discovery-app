from collections import UserDict


class SAMLCookie(UserDict):
    """
    {
        "samlNameId": "jdoe@example.org", # email
        "samlSessionIndex": "ONELOGIN_..."
        "samlUserdata": {
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress": [
                "jdoe@example.org"
            ],
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name": [],
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname": [
                "John"
            ],
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname": [
                "Doe"
            ],
            "http://schemas.xmlsoap.org/claims/upn": [],
            "http://schemas.xmlsoap.org/claims/nameIdentifier": [],
            "http://schemas.xmlsoap.org/claims/username": [],
            "http://schemas.xmlsoap.org/claims/provider": [
                "saml2"
            ],
            "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": [
                "jdoe@example.org"
            ]
        },
    }
    """

    def standardize(self):
        FIRST_NAME_KEY = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname"
        LAST_NAME_KEY = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname"

        def _get_val(data, k):
            _val = data["samlUserdata"].get(k, [])
            return _val[0] if _val else ''

        _first_name = _get_val(self.data, FIRST_NAME_KEY)
        _last_name = _get_val(self.data, LAST_NAME_KEY)
        if _first_name or _last_name:
            _name = " ".join((_first_name, _last_name))
        else:
            # if both first name and last name are empty,
            # set name to the username ("samlNameId")
            _name = self.data["samlNameId"]
        return UserInfo({
            "login": self.data["samlNameId"],  # or retrieve from samlUserData
            "name": _name,
            "avatar_url": None
        })


class GHCookie(UserDict):
    """
    {
        "login": "user123",
        "name": "John Doe",
        "email": "jdoe@example.org" # possibly missing
        "avatar_url": "..."
    }
    """

    def standardize(self):
        return UserInfo({
            "login": self.get("email") or self.get("login"),
            "avatar_url": self.get("avatar_url"),
            "name": self.get("name")
        })


class UserInfo(UserDict):
    """
    {
        "login": "user123", # discovery-app user ID
        "name": "John Doe",
        "avatar_url": "..."
    }
    """
