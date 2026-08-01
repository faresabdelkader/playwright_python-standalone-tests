"""
Global pytest configuration.

Browser type, headless mode and slow motion are configured from
``config.settings``. The native pytest-playwright command-line flags still
take precedence when provided: ``--browser``, ``--headed``, ``--slowmo``.

A default page timeout from ``settings.DEFAULT_TIMEOUT`` is applied to every
test via the autouse ``_apply_default_timeout`` fixture.
"""
import pytest

from config import settings


def pytest_configure(config):
    """Default the browser type from settings unless ``--browser`` was passed."""
    if not config.option.browser:
        config.option.browser = [settings.BROWSER_TYPE]


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Apply headless mode and slow motion from settings.

    Command-line flags (``--headed`` / ``--slowmo``) override these defaults
    because the plugin's own values are merged last.
    """
    return {
        "headless": settings.HEADLESS,
        "slow_mo": settings.SLOW_MO,
        **browser_type_launch_args,
    }

