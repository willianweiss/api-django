import re
import unicodedata


def slugify_file(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )
    value = re.sub("[^\w\s-]", "", value).strip().lower()  # noqa w605
    value = re.sub("[-\s]+", "_", value)  # noqa w605
    return value
