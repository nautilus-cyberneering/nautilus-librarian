class Filename:
    """A library media file name"""

    def __init__(self, filename):
        self.filename = filename
        self.parse(filename)

    def parse(self, filename):
        self.artwork_id, char, rest = filename.partition("-")
        self.purpose_code, char, rest = rest.partition(".")
        self.transformation_code, char, rest = rest.partition(".")
        self.type_code, char, rest = rest.partition(".")
        self.extension, char, rest = rest.partition(".")

    def parts(self):
        return (
            self.artwork_id,
            self.purpose_code,
            self.transformation_code,
            self.type_code,
            self.extension,
        )

    def __str__(self):
        return self.filename
