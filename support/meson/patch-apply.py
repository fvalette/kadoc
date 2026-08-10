#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 H2Lab Development Team
# SPDX-License-Identifier: Apache-2.0

"""
Apply a quilt-compatible patch series to an SVD file and emit a Ninja depfile.

Usage:
    patch-apply.py <orig_svd> <series> <output_svd> <depfile>

Arguments:
    orig_svd     Path to the original (unmodified) manufacturer SVD file.
    series       Path to the patch series directory containing a 'series' file
                 and the individual .patch files listed in it.
    output_svd   Path where the patched SVD will be written (in builddir).
    depfile      Path where the Ninja depfile will be written.  Meson passes
                 this as @DEPFILE@ from the calling custom_target.

The script uses the standard POSIX `patch` utility - no quilt dependency is
required at build time. quilt is only needed for authoring new patches.

Depfile format (Ninja make-style):
    <output_svd>: <patch1> <patch2> ...

Orig svd and and patch series file are already mark as dependencies by meson as
they are (implicit) inputs.
"""

import shutil
import subprocess
import sys

from pathlib import Path


PATCH_CMD = shutil.which("patch")


def read_series(series: Path) -> list[Path]:
    """Return list of patch filenames from a quilt series file (comments stripped)."""
    parent_dir = series.parent
    patches = []
    with series.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # quilt series entries may have options after the filename; take first token
                patches.append(Path(parent_dir / line.split()[0]))
    return patches


def apply_patch(patch: Path, workdir: Path) -> None:
    result = subprocess.run(
        [
            PATCH_CMD,
            '--no-backup-if-mismatch',
            '--reject-file=-',
            '--binary',
            '-p1',
            '--input', str(patch),
        ],
        cwd=workdir,
    )
    if result.returncode != 0:
        print(f'error: patch failed: {patch}', file=sys.stderr)
        sys.exit(result.returncode)


def write_depfile(depfile: Path, output: Path, deps: list[Path]) -> None:
    with depfile.open('w', encoding="utf-8") as f:
        f.write(f"{str(output)}: ")
        f.writelines([f"{str(d)} \\" for d in deps])


def main() -> int:
    if not PATCH_CMD:
        print('error: patch command not found', file=sys.stderr)
        return 1

    if len(sys.argv) != 5:
        print(
            f'usage: {sys.argv[0]} <orig_svd> <series> <output_svd> <depfile>',
            file=sys.stderr,
        )
        return 1

    orig_svd   = Path(sys.argv[1]).absolute()
    series     = Path(sys.argv[2]).absolute()
    output_svd = Path(sys.argv[3]).absolute()
    depfile    = Path(sys.argv[4]).absolute()

    patches = read_series(series)

    # Verify all patches exist before starting
    for p in patches:
        if not p.is_file():
            print(f'error: patch not found: {p}', file=sys.stderr)
            return 1

    shutil.copy2(orig_svd, output_svd)
    for patch in patches:
        apply_patch(patch, output_svd.parent)

    write_depfile(depfile, output_svd, patches)
    return 0


if __name__ == '__main__':
    sys.exit(main())
