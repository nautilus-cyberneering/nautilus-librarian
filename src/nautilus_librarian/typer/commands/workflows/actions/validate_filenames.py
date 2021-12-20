from nautilus_librarian.mods.dvc.domain.utils import (
    extract_modified_media_file_list_from_dvd_diff_output,
)
from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    validate_filename,
)


def validate_filenames(typer, dvc_diff):
    """
    Workflow step: it validates all the media file names.

    TODO: inject "console_printer" instead of "typer"
    so that we can test this step independently in the future.
    """
    if dvc_diff == "{}":
        typer.echo("No Gold image changes found")
        raise typer.Exit()

    filenames = extract_modified_media_file_list_from_dvd_diff_output(dvc_diff)

    for filename in filenames:
        try:
            validate_filename(filename)
            typer.echo(f"{filename} ✓")
        except ValueError as error:
            typer.echo(f"{filename} ✗ {error}", err=True)
            raise typer.Abort()
