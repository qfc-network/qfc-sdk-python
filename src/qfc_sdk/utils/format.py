"""Formatting utilities."""

from datetime import datetime


def shorten_address(address: str, start: int = 4, end: int = 4) -> str:
    """Shorten an address for display.

    Args:
        address: The address to shorten
        start: Number of characters to show at start (after 0x)
        end: Number of characters to show at end

    Returns:
        Shortened address string

    Examples:
        >>> shorten_address("0x742d35Cc6634C0532925a3b844Bc9e7595f12345")
        '0x742d...2345'
        >>> shorten_address("0x742d35Cc6634C0532925a3b844Bc9e7595f12345", 6, 6)
        '0x742d35...f12345'
    """
    if not address or len(address) < (start + end + 6):
        return address

    return f"{address[:start + 2]}...{address[-end:]}"


def shorten_hash(tx_hash: str, start: int = 4, end: int = 4) -> str:
    """Shorten a transaction hash for display.

    Args:
        tx_hash: The transaction hash to shorten
        start: Number of characters to show at start (after 0x)
        end: Number of characters to show at end

    Returns:
        Shortened hash string

    Examples:
        >>> shorten_hash("0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
        '0xabcd...7890'
    """
    return shorten_address(tx_hash, start, end)


def format_timestamp(timestamp: int, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a Unix timestamp.

    Args:
        timestamp: Unix timestamp in seconds
        format_str: strftime format string

    Returns:
        Formatted datetime string

    Examples:
        >>> format_timestamp(1704067200)
        '2024-01-01 00:00:00'
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime(format_str)


def format_relative_time(timestamp: int) -> str:
    """Format a timestamp as relative time.

    Args:
        timestamp: Unix timestamp in milliseconds

    Returns:
        Relative time string (e.g., "5 minutes ago")

    Examples:
        >>> format_relative_time(time.time() * 1000 - 60000)
        '1 minute ago'
    """
    # Convert to seconds if in milliseconds
    if timestamp > 1e12:
        timestamp = timestamp // 1000

    now = datetime.now().timestamp()
    diff = int(now - timestamp)

    if diff < 0:
        return "in the future"

    if diff < 60:
        return f"{diff} second{'s' if diff != 1 else ''} ago"

    if diff < 3600:
        minutes = diff // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    if diff < 86400:
        hours = diff // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    if diff < 2592000:  # 30 days
        days = diff // 86400
        return f"{days} day{'s' if days != 1 else ''} ago"

    if diff < 31536000:  # 365 days
        months = diff // 2592000
        return f"{months} month{'s' if months != 1 else ''} ago"

    years = diff // 31536000
    return f"{years} year{'s' if years != 1 else ''} ago"
