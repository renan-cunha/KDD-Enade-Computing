import pytest
from unittest.mock import MagicMock, Mock
from verify_environment import verify_environment


def test_correct_environment():
    mock = Mock()
    mock.version_info.major = 3
    mock.version_info.minor = 6

    assert verify_environment(mock) == 1


def test_wrong_major_environment():
    mock = Mock()
    mock.version_info.major = 2
    mock.version_info.minor = 6

    with pytest.raises(TypeError):
        verify_environment(mock)


def test_wrong_minor_environment():
    mock = Mock()
    mock.version_info.major = 3
    mock.version_info.minor = 7

    with pytest.raises(TypeError):
        verify_environment(mock)