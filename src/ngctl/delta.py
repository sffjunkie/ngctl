import logging
import re
from datetime import timedelta, datetime, timezone

BEFORE_RE = r"([+-]?[0-9]+)([dw])"

logger = logging.getLogger(__name__)


def older_offset_unit(older: str | None) -> tuple[int, str] | None:
    if older is None:
        return None

    m = re.match(BEFORE_RE, older)
    if m is None:
        return None

    offset = int(m.group(1))
    unit = m.group(2)

    if unit == "w":
        offset = offset * 7
        unit = "d"

    return (offset, unit)


def older_timedelta(offset: float, unit: str) -> timedelta | None:
    if unit == "d":
        return timedelta(days=offset)
    elif unit == "w":
        return timedelta(days=offset * 7)
    else:
        logger.warning("Unrecognised date unit: must be one of 'd' or 'w'")
        return None


def older_dt(older_spec: str) -> datetime | None:
    offset_unit = older_offset_unit(older_spec)
    if offset_unit is None:
        older_than = None
    else:
        offset, unit = offset_unit

        dt = older_timedelta(float(offset), unit)
        if dt is not None:
            older_than = datetime.now(tz=timezone.utc) - dt
            print(older_than)
        else:
            older_than = None

    return older_than
