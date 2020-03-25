import pytest

from configDmanager import import_config

import DemPipe


def test_pipe_version():
    assert DemPipe.__version__ == import_config('PackageConfigs.VersionConfig').version
