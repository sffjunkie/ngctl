import re
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

from ngctl.command import command_output

SYSTEM_GENERATION_LINK_RE = r"system-(\d+)-link"


class SystemGeneration(NamedTuple):
    generation: int
    date: str
    nixosVersion: str
    kernelVersion: str
    configurationRevision: str
    specialisations: str
    current: bool

    def rich_renderables(self):
        items = []
        if self.current:
            items.append(f"{self.generation} current")
        else:
            items.append(str(self.generation))
        items.append(self.date)
        items.append(self.nixosVersion)
        items.append(self.kernelVersion)
        items.append(self.configurationRevision)
        items.append(",".join(self.specialisations))
        return items


def system_generations(
    profile_dir: Path,
    older: datetime | None = None,
) -> list[SystemGeneration]:
    current_system = (profile_dir / "system").readlink().name
    if (m := re.match(SYSTEM_GENERATION_LINK_RE, current_system)) is None:
        return []
    current_generation_number = int(m.group(1))

    data = []
    for generation_dir in profile_dir.glob("*"):
        if (
            m := re.match(SYSTEM_GENERATION_LINK_RE, str(generation_dir.name))
        ) is not None:
            build_date = datetime.fromtimestamp(
                generation_dir.stat().st_ctime, tz=timezone.utc
            )
            if older is not None and build_date >= older:
                continue

            generation_number = int(m.group(1))

            nixos_version_file = generation_dir / "nixos-version"
            if nixos_version_file.exists():
                with open(nixos_version_file) as fp:
                    nixos_version = fp.read()
            else:
                nixos_version = "Unknown"

            kernel_dir = ((generation_dir / "kernel").readlink()).parent
            kernel_module_dir = kernel_dir / "lib" / "modules"
            if kernel_module_dir.exists():
                kernel_version = tuple(kernel_module_dir.glob("*"))[0].name
            else:
                kernel_version = "Unknown"

            version_cmd = str(generation_dir / "sw" / "bin" / "nixos-version")
            args = [version_cmd, "--configuration-revision"]
            configuration_revision = command_output(args)

            args = [version_cmd]
            nixos_version_default = command_output(args)

            if configuration_revision == nixos_version_default:
                configuration_revision = ""

            specialisation_dir = generation_dir / "specialisation"
            specialisations_dirs = tuple(specialisation_dir.glob("*"))
            if len(specialisations_dirs) == 0:
                specialisations = ["*"]
            else:
                specialisations = [s for s in specialisations_dirs if s.is_dir]

            data.append(
                SystemGeneration(
                    generation=generation_number,
                    date=build_date.isoformat(timespec="seconds"),
                    nixosVersion=nixos_version,
                    kernelVersion=kernel_version,
                    configurationRevision=configuration_revision,
                    specialisations=specialisations,
                    current=current_generation_number == generation_number,
                )
            )

    return data
