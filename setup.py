#!/usr/bin/env python

"""
Setup versions_service.

Note: Read RELEASE.md for notes on the release process
"""

from pathlib import Path
from setuptools import setup
from shutil import which


# Only use the SCM version if we have a functional git environment.
use_scm_version = Path('.git').exists() and which('git')

if use_scm_version:
    setup(use_scm_version=True)
else:
    setup()
