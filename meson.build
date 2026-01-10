# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2023 Ledger SAS
# Copyright 2025 H2Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

project(
    'kadoc', 'c',
    meson_version: '>=1.4.0',
    version : run_command('support/meson/version.sh', 'get-vcs', check: true).stdout().strip(),
    license: 'Apache-2.0',
    license_files: ['LICENSES/Apache-2.0.txt'],
)

meson.add_dist_script('support/meson/version.sh', 'set-dist', meson.project_version())

pymod = import('python')
fs = import('fs')
py3 = pymod.find_installation('python3', modules: ['svd2json', 'jinja2'])

svd2json = find_program('svd2json')
jinja_cli = find_program('jinja')

svd_opt = get_option('svd')

subdir('template')
subdir('svd')
subdir('schema')

if not get_option('with-tests-only')
    foreach f : svd_files
        if svd_opt == fs.stem(fs.name(f))
            svd_input = f
            break
        endif
    endforeach

    svd_json = custom_target('System View Description in json',
        input: svd_input,
        output: '@BASENAME@.json',
        command: [ svd2json, '--svd', '@INPUT@', '@OUTPUT@' ],
    )
else
    subdir('tests')
endif
