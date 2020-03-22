import pytest

from configDmanager import import_config

import DPipe

def test_pipe_version():
    assert DPipe.__version__ == import_config('PackageConfigs.VersionConfig').version
