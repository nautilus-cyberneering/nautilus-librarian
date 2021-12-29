class GpgColonListParser:
    """
    This is a parser for the GPG colon listing format.
    Details about the format:
    https://github.com/CSNW/gnupg/blob/master/doc/DETAILS

    Sample output:

    sec:-:4096:1:27304EDD6079B81C:1637342753:::-:::cESC:::+:::23::0:
    fpr:::::::::88966A5B8C01BD04F3DA440427304EDD6079B81C:
    grp:::::::::449972AC9FF11BCABEED8A7AE834C4349CC4DBFF:
    uid:-::::1638182580::B3B0B2247600E80BAB9D4802D5CF0AFC477DE016::A committer <committer@example.com>::::::::::0:
    ssb:-:4096:1:5B6BDD35BEDFBF6F:1637342753::::::e:::+:::23:
    fpr:::::::::B1D4A2483D1D2A02416BE0775B6BDD35BEDFBF6F:
    grp:::::::::97D36F5B8F5BECDA8A1923FC00D11C7C438584F9:
    ssb:-:4096:1:3F39AA1432CA6AD7:1637931661::::::s:::+:::23:
    fpr:::::::::BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7:
    grp:::::::::00CB9308AE0B6DE018C5ADBAB29BA7899D6062BE:
    """

    def __init__(self, output: str) -> None:
        self.output = output
        self.records = self.split_records(self.output)

    def split_records(self, output):
        lines = output.splitlines()

        records = []

        for line in lines:
            record = line.strip()

            if record == "":
                continue

            records.append(line.strip())

        return records

    def get_keygrip_by_fingerprint(self, fingerprint):
        current_fingerprint = ""

        for record in self.records:
            if record.startswith("fpr"):
                fields = record.split(":")
                current_fingerprint = fields[9]
            if record.startswith("grp"):
                fields = record.split(":")
                keygrip = fields[9]
                if current_fingerprint == fingerprint:
                    return keygrip

        return None

    def get_user_id_by_fingerprint(self, fingerprint):
        current_fingerprint = ""

        for record in self.records:
            if record.startswith("fpr"):
                fields = record.split(":")
                current_fingerprint = fields[9]
            if record.startswith("uid"):
                fields = record.split(":")
                uid = fields[9]
                if current_fingerprint == fingerprint:
                    name, separator, rest = uid.partition(" <")
                    email, separator, rest = rest.partition(">")
                    return name, email

        return None, None
