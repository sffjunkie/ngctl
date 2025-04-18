import logging
import re
from datetime import timedelta

OLDER_RE = r"([+-]?[0-9]+)([dw])"

logger = logging.getLogger(__name__)


def older_offset_unit(older: str | None) -> tuple[int, str] | None:
    if older is None:
        return None

    m = re.match(OLDER_RE, older)
    if m is None:
        return None

    offset = int(m.group(1))
    unit = m.group(2)

    if unit == "w":
        offset = offset * 7
        unit = "d"

    return (offset, unit)


def older_timedelta(offset: str, unit: str) -> timedelta | None:
    if unit == "d":
        return timedelta(days=offset)
    else:
        logger.warning("Unrecognised date unit: must be one of 'd' or 'w'")
        return None
