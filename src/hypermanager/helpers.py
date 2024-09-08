def byte_to_string(hex_string: str) -> str:
    """
    Converts a hex string into a human-readable UTF-8 or Latin-1 string.

    This function is primarily used to convert extra data (in hex format)
    into readable text for identifying builders.

    Args:
        hex_string (str): The hex string to be converted (prefixed with '0x').

    Returns:
        str: The decoded human-readable string. Returns an empty string if the input is "0x".
    """
    if hex_string == "0x":
        return ""
    # Remove the "0x" prefix and decode the hex string
    bytes_object = bytes.fromhex(hex_string[2:])
    try:
        human_readable_string = bytes_object.decode("utf-8")
    except UnicodeDecodeError:
        human_readable_string = bytes_object.decode("latin-1")
    return human_readable_string


def address_to_topic(address: str) -> str:
    """
    Converts an Ethereum address into a topic for filtering logs/events.

    This function pads the address with leading zeros, as required in Ethereum
    for filtering logs based on addresses in the logs/topics.

    Args:
        address (str): The Ethereum address to be converted (prefixed with '0x').

    Returns:
        str: The padded address in the format suitable for log filtering.
    """
    return "0x000000000000000000000000" + address[2:]
