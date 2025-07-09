<!--
SPDX-FileCopyrightText: 2024 Ledger SAS
SPDX-License-Identifier: Apache-2.0
-->

# sentry-svd
Collection of SVD files with meson recipe to handle them

[![REUSE status](https://api.reuse.software/badge/github.com/camelot-os/kadoc)](https://api.reuse.software/badge/github.com/camelot-os/kadoc)

## Prerequisits

Python3 is required for this meson project with the following packages:
 - [Jinja2](https://pypi.org/project/Jinja2/)
 - [svd2json](https://pypi.org/project/svd2json/)

## Project options
 - `svd`: string, svd filename to use (without `.svd` extension)
 The given file must be present under the `<project root>/svd` directory. The meson.build recipe will walk through the `svds` list.

 e.g.:
  ```console
  meson setup -Dstm32u5xx <builddir>
 ```

## Usage
This project defines a custom target that convert the manufacturer provided svd to a custom json format to ease header generation with `Jinja2`, that target is named `<svd_basename>.json`

```console
cd <builddir>
ninja stm32u5xx.json
```

### As a subproject
While use as a meson subproject, this project provides useful variables.
 - `svd_json`: targets that generates json file.
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
     depends: [ svd_json ],
     command: [ jinja_cli, '-d', svd_json, '-o', '@OUTPUT@', '@INPUT@' ],
 )

 layout_h = custom_target('gen_layout',
     input: layout_in,
     output: '@BASENAME@',
     depends: [ svd_json ],
     command: [ jinja_cli, '-d', svd_json, '-o', '@OUTPUT@', '@INPUT@' ],
 )
```
 ##### with generator
```
jinja_gen = generator(jinja_cli,
       output: '@BASENAME@',
       arguments: ['-d', '@0@'.format(svd_json),
                   '-o', '@OUTPUT@',
                   '@EXTRA_ARGS@',
                   '@INPUT@'],
       depends: [ svd_json ])

 irq_def_h = jinja_gen.process(irq_defs_in)
 layout_h = jinja_gen.process(layout_in)
 gpio_h = jinja_gen.process(peripheral_defs_in, extra_args: ['--define', 'NAME', 'GPIO'])
```
> **NOTE:**  `NAME` value must be either a peripheral `name` **or** peripherals `groupName`

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
