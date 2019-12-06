import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import datetime
import time
import assests
import calculator
import configurations


def prettify_now():
    return datetime.datetime.now().strftime(configurations.TIMESTAMP_FORMAT)


def initialize_chrome_instance(url):
    options = Options()
    # options.add_argument('--headless')
    driver = Chrome('assets/chromedriver', options=options)
    driver.get(url)
    return driver


def take_element_screenshot(element_path, version, timestamp):
    driver = initialize_chrome_instance(element_path)
    time.sleep(5);
    image = driver.find_element_by_tag_name(configurations.SELECTOR_TAG)
    image.screenshot('products/' + version + '_' + timestamp + configurations.SCREENSHOTS_FORMAT)
    driver.close()
    return 'products/' + version + '_' + timestamp + configurations.SCREENSHOTS_FORMAT


def compare_versions(main_version, ref_version):
    if main_version.SignalPixels == ref_version.SignalPixels and main_version.BackgroundPixels == ref_version.BackgroundPixels:
        return True
    else:
        return False


def main():
    time_stamp = prettify_now()
    main_image = take_element_screenshot(assests.MAIN_VERSION, "main", time_stamp)
    ref_image = take_element_screenshot(assests.REF_VERSION, "ref", time_stamp)
    main_values = calculator.calculate_signal_vs_background(configurations.BACKGROUND, main_image)
    ref_values = calculator.calculate_signal_vs_background(configurations.BACKGROUND, ref_image)
    if compare_versions(main_values, ref_values):
        print("passed")
    else:
        print("failed")


main()

