"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import re
import string
import textwrap
import unicodedata as ud
from collections import Counter
from difflib import SequenceMatcher
from typing import Any, List, Sequence, Tuple

from jinja2 import Environment, Template, meta


def jinja_format(template: str, skip_validation: bool = True, **kwargs: Any) -> str:
    if not skip_validation:
        variables = meta.find_undeclared_variables(Environment().parse(template))
        if not all(k in kwargs for k in variables):
            raise ValueError(f"Expected: {variables}, got: {sorted(kwargs)}.\nTemplate:\n{template}")
        kwargs = {k: kwargs[k] for k in variables}
    return Template(template, keep_trailing_newline=True).render(**kwargs)


def promp_template_from_file(path: str) -> str:
    """Reads a prompt template from a file and returns as a string"""
    with open(path, "r", encoding="utf-8") as f:
        return textwrap.dedent(f.read().strip())


def string_format(template: str, skip_validation: bool = True, **kwargs: Any) -> str:
    if not skip_validation:
        variables = [k[1] for k in string.Formatter().parse(template) if k[1]]
        if not all(k in kwargs for k in variables):
            raise ValueError(f"Expected: {variables}, got: {sorted(kwargs)}.\nTemplate:\n{template}")
        #  `Dict[Optional[str], typing.Any]`.
        kwargs = {k: kwargs[k] for k in variables}
    return template.format(**kwargs)
