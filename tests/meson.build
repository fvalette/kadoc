# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2023 Ledger SAS
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

svd_tests_main_in = files('main.c.in')
svd_tests_peripherals = [
    'RCC',
    'GPIO',
    'USART',
    'I2C',
    'PWR',
    'SPI',
]

foreach soc, svd_json: json_dict
    irq_defs_h = custom_target('@0@_irq_defs_h'.format(soc),
        input: irq_defs_in,
        output: '@0@_@BASENAME@'.format(soc),
        depends: [ svd_json ],
        command: [ jinja_cli, '-d', svd_json, '-o', '@OUTPUT@', '@INPUT@' ],
        build_by_default: true
    )

    layout_h = custom_target('@0@_layout_defs_h'.format(soc),
        input: layout_in,
        output: '@0@_@BASENAME@'.format(soc),
        depends: [ svd_json ],
        command: [ jinja_cli, '-d', svd_json, '-o', '@OUTPUT@', '@INPUT@' ],
        build_by_default: true
    )

    peripherals_h = []
    foreach peripheral: svd_tests_peripherals
        peripherals_h += custom_target('@0@_@1@_defs_h'.format(soc, peripheral.to_lower()),
            input: peripheral_defs_in,
            output: '@0@_@1@_defs.h'.format(soc, peripheral.to_lower()),
            depends: [ svd_json ],
            command: [ jinja_cli, '-d', svd_json, '--define', 'NAME', peripheral,'-o', '@OUTPUT@', '@INPUT@' ],
            build_by_default: true
    )
    endforeach

    main_c = custom_target('@0@_main_c'.format(soc),
        input: svd_tests_main_in,
        output: '@0@_@BASENAME@'.format(soc),
        command: [ jinja_cli, '--define', 'soc', soc, '--define', 'peripherals', ','.join(svd_tests_peripherals), '-o', '@OUTPUT@', '@INPUT@' ],
        build_by_default: true
    )

    test_exe = executable('@0@_test'.format(soc),
        sources: [ main_c, irq_defs_h, irq_defs_h, layout_h, peripherals_h ],
        link_language: 'c',
        native: true,
    )

    test('@0@'.format(soc), test_exe)

endforeach
