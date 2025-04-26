import logging
import re
from datetime import timedelta, datetime

BEFORE_RE = r"([+-]?[0-9]+)([dw])"

logger = logging.getLogger(__name__)


def before_offset_unit(before: str | None) -> tuple[int, str] | None:
    if before is None:
        return None

    m = re.match(BEFORE_RE, before)
    if m is None:
        return None

    offset = int(m.group(1))
    unit = m.group(2)

    if unit == "w":
        offset = offset * 7
        unit = "d"

    return (offset, unit)


def before_timedelta(offset: str, unit: str) -> timedelta | None:
    if unit == "d":
        return timedelta(days=offset)
    elif unit == "w":
        return timedelta(days=offset * 7)
    else:
        logger.warning("Unrecognised date unit: must be one of 'd' or 'w'")
        return None


def before_dt(before_spec: str) -> datetime | None:
    offset_unit = before_offset_unit(before_spec)
    if offset_unit is None:
        older_than = None
    else:
        offset, unit = offset_unit

        dt = before_timedelta(offset, unit)
        if dt is not None:
            older_than = datetime.now() - dt
        else:
            older_than = None

    return older_than
