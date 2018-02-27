from django.test import TestCase  # NOQA
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
# Create your tests here.


def test_pep8():
    response = os.system("flake8 --ignore=E501,E122,E722 minisat satellite")
    assert response == 0


def test_web_ui():
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    driver.get("http://localhost:8000")
    assert "MiniSat" in driver.title
    driver.get("http://localhost:8000/compute_resource")
    assert "MiniSat" in driver.title
    driver.get("http://localhost:8000/profile")
    assert "MiniSat" in driver.title
    driver.get("http://localhost:8000/create_host")
    assert "MiniSat" in driver.title
    driver.get("http://localhost:8000/operating_system")
    assert "MiniSat" in driver.title
    driver.get("http://localhost:8000/new_container")
    assert "MiniSat" in driver.title
    driver.get("http://localhost:8000/local_images")
    assert "MiniSat" in driver.title
    driver.close()


def test_compute_resource():
    options = Options()
    de = {}
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    driver.get("http://localhost:8000/compute_resource")
    name = driver.find_element_by_id("compute_name")
    name.send_keys("compute_testing")
    ip = driver.find_element_by_id("compute_ip")
    de["ip"] = str(os.popen("hostname -I").readlines()).split(" ")
    ip.send_keys(de["ip"][0][2:])
    root_pass = driver.find_element_by_id("compute_password")
    root_pass.send_keys("root")
    compute_submit = driver.find_element_by_id("compute_submit")
    compute_submit.send_keys(Keys.RETURN)
    time.sleep(11)
    driver.save_screenshot("compute.png")
    assert "Compute Resource Added Successfully" in driver.page_source
