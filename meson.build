# SPDX-License-Identifier: Apache-2.0
#
# SPDX-FileCopyrightText: 2023 Ledger SAS
# SPDX-FileCopyrightText: 2025 - 2026 H2Lab Development Team

project(
    'kadoc', 'c',
    meson_version: '>=1.10.0',
    version : run_command('support/meson/version.sh', 'get-vcs', check: true).stdout().strip(),
    license: 'Apache-2.0',
    license_files: ['LICENSES/Apache-2.0.txt'],
)

meson.add_dist_script('support/meson/version.sh', 'set-dist', meson.project_version())

pymod = import('python')

py3 = pymod.find_installation('python3', modules: ['svd2json', 'jinja2'])

svd2json = find_program('svd2json')
jinja_cli = find_program('jinja')
patch_apply = find_program('support/meson/patch-apply.py')

targets = get_option('target')
with_test = get_option('with-test')

subdir('patches')
subdir('schema')
subdir('svd')
subdir('template')

# If targets list is empty, defaulted to all svd files
if targets.length() == 0
    targets = svd_dict.keys()
endif

patched_dict = {}
json_dict = {}

foreach t: targets
    if not svd_dict.has_key(t)
        error('target', t, 'not found')
    endif

    svd_in = svd_dict.get(t)
    # SVD install directory is '<prefix>/share/svd/<manufacturer>'
    # So, deduce here the 'svd/<manufacturer>' for each svd
    svd_install_suffix = fs.parent(fs.relative_to(svd_in, meson.current_source_dir()))

    if patch_series_dict.has_key(t)
        series = patch_series_dict.get(t)
        # If SVD is patched, install the original svd renamed <target>.svd -> <target>.orig.svd
        install_orig_svd = fs.name(fs.replace_suffix(svd_in, '.orig.svd'))
        install_data(svd_in, install_dir : get_option('datadir') / svd_install_suffix, rename: install_orig_svd)
        svd_in = custom_target(
            t + '.svd patched',
            input: svd_in,
            output: '@BASENAME@.svd',
            depfile: '@BASENAME@.d',
            depend_files: series,
            command: [patch_apply, '@INPUT@', series, '@OUTPUT@', '@DEPFILE@'],
            install: true,
            install_dir: get_option('datadir') / svd_install_suffix,
        )
        patched_dict += {t: svd_in}
    else
        install_data(svd_in, install_dir : get_option('datadir') / svd_install_suffix)
    endif

    json = custom_target(t + '.json',
        input: svd_in,
        output: '@BASENAME@.json',
        command: [ svd2json, '--svd', '@INPUT@', '@OUTPUT@' ],
    )
    json_dict += {t: json}
endforeach

alias_target('patch', patched_dict.values())
alias_target('json', json_dict.values())

if with_test
    subdir('tests')
endif

summary('target', patched_dict.keys(), section: 'Patched SVD')
summary('target', json_dict.keys(), section: 'Generated Json')
