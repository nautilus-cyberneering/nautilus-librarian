class GitUser:
    """
    Global git user info
    """

    def __init__(self, name, email, signingkey):
        self.name = name
        self.email = email
        self.signingkey = signingkey
