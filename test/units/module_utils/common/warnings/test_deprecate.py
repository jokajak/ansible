# -*- coding: utf-8 -*-
# (c) 2019 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

import ansible.module_utils.common.warnings as warnings

from ansible.module_utils.common.warnings import deprecate, get_deprecation_messages
from ansible.module_utils.six import PY3


@pytest.fixture
def deprecation_messages():
    return [
        {'msg': 'First deprecation', 'version': None},
        {'msg': 'Second deprecation', 'version': '2.14'},
        {'msg': 'Third deprecation', 'version': '2.9'},
    ]


def test_deprecate_message_only():
    deprecate('Deprecation message')
    assert warnings._global_deprecations == [{'msg': 'Deprecation message', 'version': None}]


def test_deprecate_with_version():
    deprecate(msg='Deprecation message', version='2.14')
    assert warnings._global_deprecations == [{'msg': 'Deprecation message', 'version': '2.14'}]


def test_multiple_deprecations(deprecation_messages):
    for d in deprecation_messages:
        deprecate(**d)

    assert deprecation_messages == warnings._global_deprecations


def test_get_deprecation_messages(deprecation_messages):
    for d in deprecation_messages:
        deprecate(**d)

    accessor_deprecations = get_deprecation_messages()
    assert isinstance(accessor_deprecations, tuple)
    assert len(accessor_deprecations) == 3


@pytest.mark.parametrize(
    'test_case',
    (
        1,
        True,
        [1],
        {'k1': 'v1'},
        (1, 2),
        6.62607004,
        b'bytestr' if PY3 else None,
        None,
    )
)
def test_deprecate_failure(test_case):
    with pytest.raises(TypeError, match='deprecate requires a string not a %s' % type(test_case)):
        deprecate(test_case)
