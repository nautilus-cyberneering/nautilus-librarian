# Commands

The Nautilus Librarian console commands.

## Gold Images Processing

It a command to handle `Gold` image changes in a image dataset.

### Description

This command allows you to process all the changes in a library repository affecting Gold images.

```shell
nautilus-librarian gold-images-processing \
    --previous-ref PREVIOUS_REF \
    --current-ref  CURRENT_REF
```

If you handle a dataset of images following the [Nautilus Filename Specification](https://github.com/Nautilus-Cyberneering/nautilus-namecodes) a special type of image is called "Gold" image. That is the first artifact after the acquired media.

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

In fact, it does not contain the image itself but the "pointer" to the file in the remote DVC storage (`.dvc` extensions). It uses [DVC](https://dvc.org/) to store the images. You can get the real images from the remote storage but they are ignored in the Git repository.

[DVC](https://dvc.org/) has a command similar to Git: `dvd diff` which give you a list of the changes between two commits.

For example, if you clone that repo and you run this command:

```shell
dvc diff --json 420ea8d 6e9878f
```

You will obtain this `json` object:

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

That means some images were deleted and one image was modified.

The `gold-images-processing` command helps you to handle all changes related to `Gold images`. `Gold` images are identified by their purpose code `32`. We know that the modified image is a `Gold` image because the second code in the name is `32`, following the art work ID: `000001-32.600.2.tif`.

The main goal for this command is to automatically generated `Base` images. When you add a new `Gold` image to a library that image is usually too big, and very often you do not need a very high resolution. `Base` images are a second type of image that has a lower resolution and can be used for a lot of use cases. The `gold-images-processing` automatically generates and keep synced the set of `Base` images.

The `gold-images-processing` command also helps to keep the library clean and sorted. These is the list all all tasks.

- Get new or modified Gold images using `dvc diff` command.
- Pull images from dvc remote storage.
- Validate filenames.
- Validate filepaths.
- Validate image size.
- Generate Base image from Gold (change size and icc profile).
- Auto-commit new Base images.

They way you usually use this command is by invoking it on a GitHub (or other CI/CD tool) workflow. You can see an example [here](https://github.com/Nautilus-Cyberneering/chinese-ideographs/blob/main/.github/workflows/gold-drawings-processing.yml).

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

| Name           | Description                                                                                              | envvar            |
|----------------|----------------------------------------------------------------------------------------------------------|-------------------|
| `previous_ref` | The `a_rev` in the dvd diff command. See: [dvc diff --help](https://dvc.org/doc/command-reference/diff). | `NL_PREVIOUS_REF` |
| `current_ref`  | The `b_rev` in the dvd diff command. See: [dvc diff --help](https://dvc.org/doc/command-reference/diff). | `NL_CURRENT_REF`  |

### Options

| Name                  | Optional | Description                                            | Default |
|-----------------------|----------|--------------------------------------------------------|---------|
| `git_user_name`       | yes      | Committer name for automatically generated git commits |         |
| `git_user_email`      | yes      | TODO                                                   |         |
| `git_user_signingkey` | yes      | TODO                                                   |         |
| `git_repo_dir`        | yes      | TODO                                                   |         |
| `min_image_size`      | yes      | TODO                                                   |         |
| `max_image_size`      | yes      | TODO                                                   |         |
| `base_image_size`     | yes      | TODO                                                   |         |
| `dvc_diff`            | yes      | TODO                                                   |         |
| `dvc_remote`          | yes      | TODO                                                   |         |
| `gnupghome`           | yes      | TODO                                                   |         |

### Extra environment variables

| Name                      | Optional | Description |
|---------------------------|----------|-------------|
| `AZURE_STORAGE_ACCOUNT`   | no       | TODO        |
| `AZURE_STORAGE_SAS_TOKEN` | no       | TODO        |
