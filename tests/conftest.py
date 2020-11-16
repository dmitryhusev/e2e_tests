import os
import pytest
from selenium.webdriver import Firefox


@pytest.fixture
def browser():
    ci_browser = os.getenv('BROWSER')
    if ci_browser:
        br = ci_browser
        # run selenoid container
        pass
    else:
        br = Firefox()
        br.maximize_window()
    yield br
    br.quit()


# Other fixtures can be added below
