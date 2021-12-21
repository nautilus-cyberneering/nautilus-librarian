# GPG fixtures

Export GPG key:

```shell
gpg --output private.gpg --armor --export-secret-key committer@example.com
```

Import GPG key in a temporary directory:

```shell
gpg --homedir ./tests/fixtures/.gnupg --import private.gpg
```

The GPG key we are using for testing:

```shell
gpg --list-keys --fingerprint --with-keygrip --with-subkey-fingerprints 27304EDD6079B81C
pub   rsa4096 2021-11-19 [C]
      8896 6A5B 8C01 BD04 F3DA  4404 2730 4EDD 6079 B81C
      Keygrip = 449972AC9FF11BCABEED8A7AE834C4349CC4DBFF
uid           [ultimate] A committer <committer@example.com>
sub   rsa4096 2021-11-19 [E]
      B1D4 A248 3D1D 2A02 416B  E077 5B6B DD35 BEDF BF6F
      Keygrip = 97D36F5B8F5BECDA8A1923FC00D11C7C438584F9
sub   rsa4096 2021-11-26 [S]
      BD98 B3F4 2545 FF93 EFF5  5F7F 3F39 AA14 32CA 6AD7
      Keygrip = 00CB9308AE0B6DE018C5ADBAB29BA7899D6062BE
```
