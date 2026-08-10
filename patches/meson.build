# SPDX-License-Identifier: Apache-2.0
#
# SPDX-FileCopyrightText: 2026 H2Lab Development Team

fs = import('fs')

patch_series_files = files()

subdir('st')

# Create a dictionary w/ target as key, patch series file object as value
patch_series_dict = {}
foreach f: patch_series_files
    # patches layout is the following, patches/<manufacturer>/<target>/series
    target = fs.name(fs.parent(f))
    patch_series_dict += {target: f}
endforeach
