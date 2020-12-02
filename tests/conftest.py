import os
import pytest
from selenium import webdriver
# from selenium.webdriver import Firefox


@pytest.fixture
def browser():
    ci_browser = os.getenv('BROWSER')
    if ci_browser:
        br = ci_browser
        # run selenoid container
        pass
    else:
        capabilities = {
                    'browserName': 'firefox',
                    'version': '80',
                }
        br = webdriver.Remote('http://localhost:4444/wd/hub', capabilities)
        br.maximize_window()
    yield br
    br.quit()


# Other fixtures can be added below
