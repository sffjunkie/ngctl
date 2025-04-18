import re
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

from nog.command import command_output

LINK_MATCH_RE = r"system-(\d+)-link"


class Generation(NamedTuple):
    number: int
    build_date: str
    nixos_version: str
    kernel_version: str
    configuration_revision: str
    specialisations: str
    current: bool


def generations(
    profile_dir: Path,
    before: datetime | None = None,
) -> list[Generation]:
    current_system = (profile_dir / "system").readlink().name
    m = re.match(LINK_MATCH_RE, current_system)
    current_generation_number = m.group(1)

    data = []
    for generation_dir in profile_dir.glob("*"):
        if (m := re.match(LINK_MATCH_RE, str(generation_dir.name))) is not None:
            build_date = datetime.fromtimestamp(generation_dir.stat().st_ctime)
            if before is not None and build_date >= before:
                continue

            generation_number = m.group(1)

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
                Generation(
                    number=generation_number,
                    build_date=build_date.strftime("%Y-%m-%d %H:%M:%S"),
                    nixos_version=nixos_version,
                    kernel_version=kernel_version,
                    configuration_revision=configuration_revision,
                    specialisations=",".join(specialisations),
                    current=current_generation_number == generation_number,
                )
            )

    return data
