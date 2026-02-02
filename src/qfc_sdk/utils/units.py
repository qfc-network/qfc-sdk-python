"""Unit conversion utilities."""

from decimal import Decimal, InvalidOperation

WEI_PER_QFC = 10**18
WEI_PER_GWEI = 10**9


def parse_qfc(value: str | int | float) -> int:
    """Convert QFC to wei.

    Args:
        value: Amount in QFC (string, int, or float)

    Returns:
        Amount in wei as integer

    Examples:
        >>> parse_qfc("1.5")
        1500000000000000000
        >>> parse_qfc(10)
        10000000000000000000
    """
    if isinstance(value, (int, float)):
        value = str(value)

    try:
        decimal_value = Decimal(value)
        wei_value = decimal_value * WEI_PER_QFC
        return int(wei_value)
    except InvalidOperation as e:
        raise ValueError(f"Invalid QFC value: {value}") from e


def format_qfc(wei: int, decimals: int = 4) -> str:
    """Convert wei to QFC string.

    Args:
        wei: Amount in wei
        decimals: Number of decimal places (default: 4)

    Returns:
        Formatted QFC string

    Examples:
        >>> format_qfc(1500000000000000000)
        '1.5000'
        >>> format_qfc(1500000000000000000, 2)
        '1.50'
    """
    decimal_value = Decimal(wei) / WEI_PER_QFC
    format_str = f"{{:.{decimals}f}}"
    return format_str.format(decimal_value)


def parse_gwei(value: str | int | float) -> int:
    """Convert gwei to wei.

    Args:
        value: Amount in gwei

    Returns:
        Amount in wei as integer

    Examples:
        >>> parse_gwei("10")
        10000000000
    """
    if isinstance(value, (int, float)):
        value = str(value)

    try:
        decimal_value = Decimal(value)
        wei_value = decimal_value * WEI_PER_GWEI
        return int(wei_value)
    except InvalidOperation as e:
        raise ValueError(f"Invalid gwei value: {value}") from e


def format_gwei(wei: int, decimals: int = 1) -> str:
    """Convert wei to gwei string.

    Args:
        wei: Amount in wei
        decimals: Number of decimal places (default: 1)

    Returns:
        Formatted gwei string

    Examples:
        >>> format_gwei(10000000000)
        '10.0'
    """
    decimal_value = Decimal(wei) / WEI_PER_GWEI
    format_str = f"{{:.{decimals}f}}"
    return format_str.format(decimal_value)


def format_qfc_with_commas(wei: int, decimals: int = 4) -> str:
    """Format wei as QFC with thousand separators.

    Args:
        wei: Amount in wei
        decimals: Number of decimal places

    Returns:
        Formatted string with commas

    Examples:
        >>> format_qfc_with_commas(1234567890000000000000)
        '1,234.5679'
    """
    qfc_str = format_qfc(wei, decimals)
    parts = qfc_str.split(".")
    integer_part = parts[0]

    # Add commas
    formatted_int = ""
    for i, char in enumerate(reversed(integer_part)):
        if i > 0 and i % 3 == 0:
            formatted_int = "," + formatted_int
        formatted_int = char + formatted_int

    if len(parts) > 1:
        return f"{formatted_int}.{parts[1]}"
    return formatted_int
