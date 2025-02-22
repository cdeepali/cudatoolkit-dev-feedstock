#!/usr/bin/env python3

# Originally forked from https://github.com/conda-forge/cudatoolkit-dev-feedstock
# Distributed under the BSD-3-Clause license
# Copyright (c) 2017, Continuum Analytics, Inc. All rights reserved.

import argparse
import json
import os
import shutil
import stat
from pathlib import Path


def copy_files(src, dst):
    def set_chmod(file_name):
        # Do a simple chmod +x for a file within python
        st = os.stat(file_name)
        os.chmod(file_name, st.st_mode | stat.S_IXOTH)

    try:
        if os.path.isfile(src):
            shutil.copy(src, dst)
            set_chmod(dst)
    except FileExistsError:
        pass


def _main(args):

    prefix_dir_path = Path(os.environ["PREFIX"])
    prefix_bin_dir_path = prefix_dir_path / "bin"
    recipe_dir_path = Path(os.environ["RECIPE_DIR"])

    # Copy cudatoolkit-dev-post-install.py to $PREFIX/bin
    src = recipe_dir_path / "cudatoolkit-dev-post-install.py"
    dst = prefix_bin_dir_path
    os.makedirs(dst, exist_ok=True)
    copy_files(src, dst)
    with open(prefix_bin_dir_path / "cudatoolkit-dev-extra-args.json", "w") as f:
        f.write(json.dumps(args))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build script for cudatoolkit-dev")

    parser.add_argument("release", action="store", type=str)
    parser.add_argument("driver_version", action="store", type=str)
    results = parser.parse_args()
    args = vars(results)
    _main(args)
