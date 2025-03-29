"""Utility functions for shellsmith."""

import base64


def base64_encode(text: str | None) -> str | None:
    """Encodes a string into URL-safe Base64 format.

    If the input is `None`, returns `None`. Padding characters are removed
    if the input length is divisible by 3.

    Args:
        text: The input string to encode. May be `None`.

    Returns:
        The Base64-encoded string, or `None` if the input is `None`.
    """
    if text is None:
        return None
    return (
        base64.urlsafe_b64encode(text.encode("utf-8"))
        .decode("utf-8")
        .rstrip("=")  # padding character if input long multiple of 3
    )


def base64_decode(encoded_text: str | None) -> str | None:
    """Decodes a URL-safe Base64 string into its original UTF-8 format.

    Pads the string if necessary before decoding.
    If the input is `None`, returns `None`.

    Args:
        encoded_text: The Base64-encoded string to decode. May be `None`.

    Returns:
        The decoded string, or `None` if the input is `None`.

    Raises:
        ValueError: If the input is improperly formatted.
    """
    if encoded_text is None:
        return None

    missing_padding = 4 - (len(encoded_text) % 4)
    if missing_padding > 0:
        encoded_text += "=" * missing_padding

    try:
        return base64.urlsafe_b64decode(encoded_text).decode("utf-8")
    except TypeError as e:
        raise ValueError("Incorrect Base64 formatting.") from e


def base64_encoded(identifier: str, encode: bool) -> str:
    """Encodes a string using Base64 if the flag is set.

    Args:
        identifier: The unique identifier to encode.
        encode: If `True`, the identifier will be Base64-encoded.
            If `False`, the original string is returned.

    Returns:
        The encoded or original string, depending on the flag.
    """
    return base64_encode(identifier) if encode else identifier
