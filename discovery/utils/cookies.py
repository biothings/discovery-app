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
        return UserInfo({
            "login": self.data["samlNameId"],  # or retrieve from samlUserData
            "name": " ".join((
                self.data["samlUserdata"][FIRST_NAME_KEY][0],
                self.data["samlUserdata"][LAST_NAME_KEY][0]
            )),
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
