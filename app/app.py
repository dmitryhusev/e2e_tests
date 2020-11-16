import time
from selenium.common.exceptions import (
    TimeoutException as Toe,
    WebDriverException as Wde,
    ElementClickInterceptedException as Ecie,
    ElementNotInteractableException as Enie,
    StaleElementReferenceException as Sere,
    UnexpectedAlertPresentException as Uape
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from app.settings import TIMEOUT, BASE_URL


def get_element(browser, locator, timeout=TIMEOUT):
    """
        Function returns web element if it is in DOM and visible.
        If not found --> TimeoutException.

            -- locator: XPATH locator of element
            -- timeout: in seconds
    """

    message = f'Element not found: {locator}'
    wait = WebDriverWait(browser, timeout)
    return wait.until(lambda x: x.find_element_by_xpath(locator), message)


def get_elements(browser, locator, timeout=TIMEOUT):
    # Does the same as element() function but returns list of elements

    message = f'Elements not found, check locator: {locator}'
    wait = WebDriverWait(browser, timeout)
    return wait.until(lambda x: x.find_elements_by_xpath(locator), message)


def get_text(browser, locator, lower=False):
    # Returns text of element

    text = get_element(browser, locator).text
    return text.lower() if lower else text


def get_attribute_value(browser, locator, attr):
    return get_element(browser, locator).get_attribute(attr)


def get_text_of_elements(browser, locator):
    elems = get_elements(browser, locator)
    return [el.text for el in elems]


def is_attribute_present(browser, locator, attribute, value):
    """
        checking if value (e.g. "helloworld") is present in attribute ("src")
        like here: <img src="helloworld.jpg">
    """

    attribute_value = get_element(browser, locator).get_attribute(attribute)
    if value in attribute_value:
        return True
    else:
        raise ValueError(f'{value} is not in {attribute_value}')


def clear(browser, locator):

    counter = 0
    while counter < 5:
        value = get_attribute_value(browser, locator, 'value')
        if len(value) > 0:
            enter_text(locator, Keys.CONTROL + 'a')
            enter_text(locator, Keys.DELETE)
            get_element(locator).clear()
            break
        else:
            time.sleep(1)
            counter += 1


def make_element_visible(browser, locator):
    browser.execute_script(
        "arguments[0].setAttribute('style','display:true;');",
        get_element(locator)
    )


def refresh_to_find(browser, locator, timeout=5, times=3):

    counter = 0
    while counter < times:
        try:
            return get_element(locator, timeout=timeout)
        except Toe:
            counter += 1
            browser.refresh()
    raise Toe(msg=f'Element "{locator}" not found')


def refresh_not_to_find(browser, locator, timeout=10, times=3):

    counter = 0
    while counter < times:
        try:
            return is_element_absent(browser, locator, timeout=timeout)
        except Toe:
            counter += 1
            browser.refresh()
    raise Toe(f'Unexpected element is present: {locator}')


def is_text_in_element(browser, locator, text, timeout=TIMEOUT):

    wait = WebDriverWait(browser, timeout)
    message = f'Element "{locator}" does not have text "{text}"'
    try:
        wait.until(
            ec.text_to_be_present_in_element((By.XPATH, locator), text),
            message)
        return get_text(browser, locator)
    except Toe:
        raise


def is_text_in_value(browser, locator, text, timeout=TIMEOUT):

    wait = WebDriverWait(browser, timeout)
    message = f'Element "{locator}" does not have text in value"{text}"'
    try:
        wait.until(
            ec.text_to_be_present_in_element_value((By.XPATH, locator), text),
            message)
        return get_attribute_value(locator, 'value')
    except Toe:
        raise


def is_element_absent(browser, locator, timeout=15):
    # Returns true if element is not visible or not found

    wait = WebDriverWait(browser, timeout)
    try:
        wait.until_not(
            lambda x: x.find_element_by_xpath(locator).is_displayed())
        return True
    except Toe:
        raise Toe(f'Unexpected element is present: {locator}')


def click(browser, locator, locator_to_wait=None, timeout=10, duration=TIMEOUT):
    # tries to click on web element
    # if exception appears, wait 1 sec and try to click again
    # total waiting time = duration

    start_time = time.time()
    while True:
        try:
            if locator_to_wait:
                get_element(browser, locator, timeout).click()
                get_element(browser, locator_to_wait, timeout=timeout)
            else:
                get_element(browser, locator, timeout).click()
            break
        except (Wde, Ecie, Toe):
            if time.time() < start_time + duration:
                time.sleep(1)
            else:
                raise


def enter_text(browser, locator, keys, timeout=TIMEOUT):
    start_time = time.time()
    while True:
        try:
            return get_element(browser, locator).send_keys(keys)
        except (Enie, Wde, Sere):
            if time.time() < start_time + timeout:
                time.sleep(1)
            else:
                raise


def switch_to_iframe(browser, web_element):
    browser.switch_to.frame(web_element)


def open_page(browser, url='', full=False):
    if full:
        browser.get(url)
    else:
        browser.get(BASE_URL + url)


def current_url(browser):
    return browser.current_url


def close_browser_tab(browser):

    counter = 0
    while counter < 10:
        if len(browser.window_handles) > 1:
            browser.close()
            return browser.switch_to.window(
                browser.window_handles[-1])
        else:
            time.sleep(1)
            counter += 1
            continue
    raise Toe('Can not close browser tab')


def go_to_tab(browser, tab_index=-1):
    tabs = browser.window_handles
    browser.switch_to.window(tabs[tab_index])


def reload_page(browser):
    browser.refresh()


def page_title(browser, *titles, timeout=15):
    wait = WebDriverWait(browser, timeout)
    for title in titles:
        try:
            wait.until(lambda x: title == x.title)
            return True
        except (Toe, Uape):
            continue
    message = '{}{}{}'.format(titles, ' is/are not in ', browser.title)
    raise Toe(message)


def text_on_page(browser, text, timeout=30):
    wait = WebDriverWait(browser, timeout)

    try:
        msg = 'Text "{}" is not displayed on the page'.format(text)
        loc = '//*[contains(text(), "%s")]' % text
        wait.until(lambda x: x.find_element_by_xpath(loc), msg)
        return True
    except Toe:
        raise


def no_text_on_page(browser, text, timeout=15):
    locator = '//*[contains(text(), "%s")]' % text
    try:
        return is_element_absent(browser, locator, timeout=timeout)

    except Toe:
        msg = (
            'Not expected, text "{}" '
            'should not be displayed on the page. '
            'Check locator: {}'.format(text, locator))
        raise Toe(msg)
