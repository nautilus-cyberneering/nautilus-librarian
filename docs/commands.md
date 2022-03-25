# Commands

The Nautilus Librarian console commands.

## Gold Images Processing

`Gold` images are a type of image in terms of its purpose,  defined on the [Nautilus Filename Specification](https://github.com/Nautilus-Cyberneering/nautilus-namecodes).

It is a command to handle `Gold` image changes in an image dataset (we call it "Library").

### Description

This command allows you to process all the changes in a library repository affecting `Gold` images.

Sample usage:

```shell
nautilus-librarian gold-images-processing \
    --previous-ref PREVIOUS_REF \
    --current-ref  CURRENT_REF
```

Where `PREVIOUS_REF` and `CURRENT_REF` ar  the git first and last commit references defining the list of commits you want to process.

If you handle a dataset of images following the [Nautilus Filename Specification](https://github.com/Nautilus-Cyberneering/nautilus-namecodes), there is a special type of image called "Gold" image. That is the first artifact after the acquired media, for example via scanning.

[Chinese Ideographs](https://github.com/Nautilus-Cyberneering/chinese-ideographs) is a sample library which follows the [Nautilus Filename Specification](https://github.com/Nautilus-Cyberneering/nautilus-namecodes). It contains some Chinese drawings related to Chinese ideographs.

In the data folder you can see all the images:

```text
data
├── 000000
│   ├── 32
│   │   ├── 000000-32.600.2.tif
│   │   └── 000000-32.600.2.tif.dvc
│   └── 52
│       ├── 000000-52.600.2.tif
│       └── 000000-52.600.2.tif.dvc
...
├── 000007
│   ├── 32
│   │   ├── 000007-32.600.2.tif
│   │   └── 000007-32.600.2.tif.dvc
│   └── 52
└── 000008
    ├── 32
    │   ├── 000008-32.600.2.tif
    │   └── 000008-32.600.2.tif.dvc
    └── 52

27 directories, 32 files
```

In fact, it does not contain the image itself but the "pointer" to the file in the remote DVC storage (`.dvc` extensions). [DVC](https://dvc.org/) is a wrapper on top of Git to version and store binary files. It is an alternative to [Git LFS](https://git-lfs.github.com/). You can get (`pull`) the real images from the remote DVC storage into your local file system and they are ignored in the Git repository.

[DVC](https://dvc.org/) has a command similar to `git diff` called `dvd diff` which give you a list of the changes between two commits.

For example, if you clone that repo:

```shell
git clone https://github.com/Nautilus-Cyberneering/chinese-ideographs
cd chinese-ideographs
```

and you run this command:

```shell
dvc diff --json 420ea8d 6e9878f
```

You will obtain this `json` object (it's has been truncated here):

```json
{                                                                     
  "added": [],
  "deleted": [
    {
      "path": "data/000000/32/000000-32.600.2.tif"
    },
    {
      "path": "data/000008/32/000008-32.600.2.tif"
    }
  ],
  "modified": [
    {
      "path": "data/000001/32/000001-32.600.2.tif"
    }
  ],
  "renamed": []
}
```

This means that some images were deleted and one image was modified.

The `gold-images-processing` command helps you to handle all changes related to `Gold` images. `Gold` images are identified by their purpose code `32`. We know that the modified image is a `Gold` image because the second code in the name is `32`, following the art work ID: `000001-32.600.2.tif`.

The main goal for this command is to generate `Base` images automatically. When you add a new `Gold` image to a library that image is usually too big, and very often you do not need a very high resolution image. `Base` images are a second type of image that have a lower resolution and can be used for a lot of use cases. The `gold-images-processing` command automatically generates and keep synced the set of `Base` images.

The `gold-images-processing` command also helps to keep the library clean and tidy. This is the list of all tasks.

- Get new or modified Gold images using `dvc diff` command.
- Pull images that are going to be processed from DVC remote storage.
- Validate filenames. Make sure the filename follows the [Nautilus Filename Specification](https://github.com/Nautilus-Cyberneering/nautilus-namecodes).
- Validate filepaths. Make sure the file is in the right folder.
- Validate image size.
- Generate Base image from `Gold` (change size and [ICC profile](https://en.wikipedia.org/wiki/ICC_profile)).
- Auto-commit new or changed `Base` images.

The way you usually use this command is by invoking it on a GitHub (or other CI/CD tool) workflow. You can see an example [here](https://github.com/Nautilus-Cyberneering/chinese-ideographs/blob/main/.github/workflows/gold-drawings-processing.yml).

Example of invoking the command in a GitHub workflow:

```yaml
- name: Run librarian gold image processing command
run: |
    nautilus-librarian gold-images-processing --previous-ref ${{ env.PREVIOUS_REF }}  --current-ref ${{ env.CURRENT_REF }}
env:
    AZURE_STORAGE_ACCOUNT: ${{ secrets.AZURE_STORAGE_ACCOUNT }}
    AZURE_STORAGE_SAS_TOKEN: ${{ secrets.AZURE_STORAGE_SAS_TOKEN }}
```

### Arguments

| Name           | Description                                                                                              | Env Var           |
|----------------|----------------------------------------------------------------------------------------------------------|-------------------|
| `previous_ref` | The `a_rev` in the dvd diff command. See: [dvc diff --help](https://dvc.org/doc/command-reference/diff). | `NL_PREVIOUS_REF` |
| `current_ref`  | The `b_rev` in the dvd diff command. See: [dvc diff --help](https://dvc.org/doc/command-reference/diff). | `NL_CURRENT_REF`  |

The `previous_ref` and `current_ref` are the positional arguments passed to the [dvc diff](https://dvc.org/doc/command-reference/diff) command:

```text
a_rev  Old Git commit to compare (defaults to HEAD)
b_rev  New Git commit to compare (defaults to the current workspace)
```

### Options

| Name                  | Optional | Description                                                                                                                           | Default             | Env Var                  |
|-----------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------|---------------------|--------------------------|
| `git_user_name`       | yes      | Committer name for automatically generated git commits                                                                                | Git global config   | `NL_GIT_USER_NAME`       |
| `git_user_email`      | yes      | Committer email for automatically generated git commits                                                                               | Git global config   | `NL_GIT_USER_EMAIL`      |
| `git_user_signingkey` | yes      | GPG signing key ID to sign commits                                                                                                    | Git global config   | `NL_GIT_USER_SIGNINGKEY` |
| `git_repo_dir`        | yes      | The directory where the Git repository is located                                                                                     | Current working dir | `NL_GIT_REPO_DIR`        |
| `min_image_size`      | yes      | Minimum `Gold` image size in pixels for width and height                                                                              | `256`               | `NL_MIN_IMAGE_SIZE`      |
| `max_image_size`      | yes      | Maximum `Gold` image size in pixels for width and height                                                                              | `16384`             | `NL_MAX_IMAGE_SIZE`      |
| `base_image_size`     | yes      | Size for the longer dimension of the Base image                                                                                       | `512`               | `NL_BASE_IMAGE_SIZE`     |
| `dvc_diff`            | yes      | Alternative diff to overwrite `previous_ref` and `current_ref` arguments                                                              |                     | `NL_DVC_DIFF`            |
| `dvc_remote`          | yes      | The name of the remote DVC storage in the `.dvc\config` file. See [dvc remote command](https://dvc.org/doc/command-reference/remote). | `None`              | `NL_DVC_REMOTE`          |
| `gnupghome`           | yes      | GPG env var to overwrite default `--homedir`. [More info](https://www.gnupg.org/documentation/manuals/gnupg/GPG-Configuration.html).  | `~/.gnupg`          | `GNUPGHOME`              |

GPG is used to sign commits. Git relays on GPG to sign commits. You have to setup your GPG configuration in order to sign commits. Right now signing commits is mandatory but we [plan to make it optional](https://github.com/Nautilus-Cyberneering/nautilus-librarian/issues/90).

Default Git configuration for commits is also obtained from Git global configuration. We are also [planning to change](https://github.com/Nautilus-Cyberneering/nautilus-librarian/issues/68) that and let the user preset that configuration before calling this command.

### Extra environment variables

| Name                      | Optional | Description                                                                                                  |
|---------------------------|----------|--------------------------------------------------------------------------------------------------------------|
| `AZURE_STORAGE_ACCOUNT`   | no       | [Your Azure Storage Account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-overview) |
| `AZURE_STORAGE_SAS_TOKEN` | no       | [Your SAS token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview)                 |

You can use environment variables instead of arguments and options, but some env vars are exclusively env vars.

Some of them, like `AZURE_STORAGE_ACCOUNT` and `AZURE_STORAGE_SAS_TOKEN`, are used by DVC to access the remote storage.

You can find instructions about how to setup a storage for DVC on the [DVC documentation](https://dvc.org/doc/command-reference/remote/add).

There is also a specific tutorial for [adding remote Azure Storage for DVC](https://github.com/josecelano/data-version-control/blob/master/docs/azure-blob-storage.md).
