# SPDX-License-Identifier: Apache-2.0
#
# SPDX-FileCopyrightText: 2023 Ledger SAS
# SPDX-FileCopyrightText: 2026 H2Lab Development Team

fs = import('fs')

svd_files = files()

# Manufacturer subdir list in alpha order
subdir('st')
# NOTE: Raspberry pi not yet being supported, it is not included as the rpi SVD file
# is not, by now, valid

# Create a dictionary w/ target as key, svd file object as value
svd_dict = {}
foreach f: svd_files
    target = fs.stem(fs.name(f))
    svd_dict += {target: f}
endforeach
