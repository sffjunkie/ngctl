import re
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

HM_GENERATION_LINK_RE = r"home-manager-(\d+)-link"


class HMGeneration(NamedTuple):
    generation: int
    date: str
    homeManagerVersion: str
    current: bool

    def rich_renderables(self):
        items = []
        if self.current:
            items.append(f"{self.generation} current")
        else:
            items.append(str(self.generation))
        items.append(self.date)
        items.append(self.homeManagerVersion)
        return items


def hm_generations(
    profile_dir: Path,
    older: datetime | None = None,
) -> list[HMGeneration]:
    current_system = (profile_dir / "home-manager").readlink().name
    if (m := re.match(HM_GENERATION_LINK_RE, current_system)) is None:
        return []
    current_generation_number = int(m.group(1))

    data = []
    for generation_dir in profile_dir.glob("*"):
        if (m := re.match(HM_GENERATION_LINK_RE, str(generation_dir.name))) is not None:
            build_date = datetime.fromtimestamp(
                generation_dir.stat().st_ctime, tz=timezone.utc
            )
            if older is not None and build_date >= older:
                continue

            generation_number = int(m.group(1))

            hm_version_file = generation_dir / "hm-version"
            if hm_version_file.exists():
                with open(hm_version_file) as fp:
                    hm_version = fp.read().strip("\n")
            else:
                hm_version = "Unknown"

            data.append(
                HMGeneration(
                    generation=generation_number,
                    date=build_date.isoformat(timespec="seconds"),
                    homeManagerVersion=hm_version,
                    current=current_generation_number == generation_number,
                )
            )

    return data
