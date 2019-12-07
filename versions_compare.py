from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import datetime
import assests
import calculator
import configurations
import argparse


# document timestamp for image mark and debug abilities
def prettify_now():
    return datetime.datetime.now().strftime(configurations.TIMESTAMP_FORMAT)


# Initializing chrome instance, returns driver object
def initialize_chrome_instance(url):
    options = Options()
    mobile_emulation = {"deviceName": "iPhone X"}
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = Chrome('assets/chromedriver', options=options)
    driver.get(url)
    return driver


# Navigate to proper endpoint, retrieve the element, take its screenshot and store it in products directory.
# Function returns screenshot file path
def take_element_screenshot(element_path, version, tag, timestamp):
    driver = initialize_chrome_instance(element_path)
    wait = WebDriverWait(driver, configurations.WAIT_TIMEOUT)
    image = wait.until(EC.presence_of_element_located((By.TAG_NAME, configurations.SELECTOR_TAG)))
    image.screenshot('products/' + version + '_' + timestamp + configurations.SCREENSHOTS_FORMAT)
    driver.close()
    return 'products/' + version + '_' + timestamp + configurations.SCREENSHOTS_FORMAT


# Compare image_value objects (pixels count for background and signal)
def compare_versions(main_version, ref_version):
    if main_version.SignalPixels == ref_version.SignalPixels and \
            main_version.BackgroundPixels == ref_version.BackgroundPixels:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-main', action="store", dest="main_version", default=assests.MAIN_VERSION,
                        help="main web page")
    parser.add_argument('-ref', action="store", dest="ref_version", default=assests.REF_VERSION,
                        help="ref web page")
    parser.add_argument('-tag', action="store", dest="tag", default=configurations.SELECTOR_TAG,
                        help="selector attribute")
    arguments = parser.parse_args()
    time_stamp = prettify_now()
    main_image = take_element_screenshot(arguments.main_version, "main", arguments.tag, time_stamp)
    ref_image = take_element_screenshot(arguments.ref_version, "ref", arguments.tag, time_stamp)
    main_values = calculator.calculate_signal_vs_background(configurations.BACKGROUND, main_image)
    ref_values = calculator.calculate_signal_vs_background(configurations.BACKGROUND, ref_image)
    if compare_versions(main_values, ref_values):
        print("passed")
    else:
        print("failed")


main()

