<!--
SPDX-FileCopyrightText: 2024 Ledger SAS
SPDX-FileCopyrightText: 2026 H2Lab Development Team
SPDX-License-Identifier: Apache-2.0
-->

# KADOC, a SVD handling recipe for sentry kernel in meson
Collection of SVD files with meson recipe to handle them

[![REUSE status](https://github.com/camelot-os/kadoc/actions/workflows/reuse.yml/badge.svg?branch=main&event=push)](https://github.com/camelot-os/kadoc/actions/workflows/reuse.yml)

## Overview

Kadoc is Meson recipe that helps users to integrate SVD based code generation in their projects.
It wraps the conversion from SVD to JSon using the python tools `svd2json` and provides a
meson target for use as a meson subproject.
SVD files are store under `svd/<manufacturer>/<soc>.svd`.

Manufacturer SVD files under `svd/` are **immutable originals**, i.e. they must not
be modified directly in source control.  Normalization and enrichment (fixing
register-name prefixes, adding missing field enumerations, correcting widths,
etc.) is tracked as a **quilt patch series** under `patches/<manufacturer>/<soc>/`.

At build time Meson applies the series automatically using `support/meson/patch-apply.py`,
which uses the standard POSIX `patch` utility, i.e. **no quilt dependency is required
at build time**.  The patched SVD is produced in the build directory and never
committed.  Ninja dependency tracking is handled through a generated depfile, so
any change to the series file or any individual patch file triggers an incremental
rebuild automatically.

## Prerequisits

Python3 is required for this meson project with the following packages:
 - [Jinja2](https://pypi.org/project/Jinja2/)
 - [svd2json](https://pypi.org/project/svd2json/)
 - [xmlschema](https://pypi.org/project/xmlschema/)

## Meson options
 - <s>`svd`: string, svd filename to use (without `.svd` extension)
 The given file must be present under the `<project root>/svd` directory. The meson.build recipe will walk through the `svds` list.</s> [DEPRECATED]
 - <s>`with-tests-only`: boolean, with unittests, this disables the regular targets, use for test purpose
 only </s> [DEPRECATED]
 - `target`: target(s) list, comma separated, leave empty for all targets (default empty)
 - `with-test`: boolean, if true, enable test build for each selected target (default false)
 - `schema-validation`: feature, Add svd schema validation ninja target if enable (default auto)

 e.g.:
  ```console
  meson setup -Dwith-test=true <builddir>
 ```

## Usage
This project defines a custom target that convert the manufacturer provided svd to a custom json format to ease header generation with `Jinja2`, that target is named `<soc>.json`

```console
cd <builddir>
ninja stm32u5a5.json
```

### As a subproject
While use as a meson subproject, this project provides useful variables.
 - `json_dict`: dictionary of targets that generates json file w/ soc name as key.
 - `jinja_cli`: program (found by `find_program`) to use with `custom_target` or `generator`.
 - `irq_defs_in`: template to generate soc irqs definition header.
 - `layout_in`: template to generate soc peripherals layout (IP base address) header.
 - `peripheral_defs_in`: template to generate a peripheral (or peripheral group) registers and fields description.

 #### example

 ##### with custom target
 ```
 irq_def_h = custom_target('gen_irq_defs',
    input: irq_defs_in,
     output: '@BASENAME@',
     depends: [ json_dict['<soc>'] ],
     command: [ jinja_cli, '-d', json_dict['<soc>'], '-o', '@OUTPUT@', '@INPUT@' ],
 )

 layout_h = custom_target('gen_layout',
     input: layout_in,
     output: '@BASENAME@',
     depends: [ json_dict['<soc>'] ],
     command: [ jinja_cli, '-d', json_dict['<soc>'], '-o', '@OUTPUT@', '@INPUT@' ],
 )
```
 ##### with generator
```
jinja_gen = generator(jinja_cli,
       output: '@BASENAME@',
       arguments: ['-d', '@0@'.format(json_dict['<soc>']),
                   '-o', '@OUTPUT@',
                   '@EXTRA_ARGS@',
                   '@INPUT@'],
       depends: [ json_dict['<soc>'] ])

 irq_def_h = jinja_gen.process(irq_defs_in)
 layout_h = jinja_gen.process(layout_in)
 gpio_h = jinja_gen.process(peripheral_defs_in, extra_args: ['--define', 'NAME', 'GPIO'])
```
> [!NOTE]
> `NAME` value must be either a peripheral `name` **or** peripherals `groupName`

## LICENSE
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
