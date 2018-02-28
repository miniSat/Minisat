from django.test import TestCase  # NOQA
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
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


def test_profile():
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    test_case = [("test1", "1000", "2", "30"), ("test2", "500", "2", "30"), ("test3", "1000", "-2", "30")]
    result = []
    expect_results = ["Pass", "Fail", "Fail"]
    for tup in test_case:
        driver.get("http://localhost:8000/profile")
        pname = driver.find_element_by_id("id_profile_name")
        pname.send_keys(tup[0])
        pram = driver.find_element_by_id("id_ram")
        pram.send_keys(tup[1])
        pcpu = driver.find_element_by_id("id_cpus")
        pcpu.send_keys(tup[2])
        pdisk = driver.find_element_by_id("id_disk_size")
        pdisk.send_keys(tup[3])
        psubmit = driver.find_element_by_id("id_submit")
        psubmit.click()
        if "Profile Added Successfully" in driver.page_source:
            result.append("Pass")
        else:
            result.append("Fail")
    assert result == expect_results
    driver.close()


def test_operating_system():
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)
    test_case = [("fedora25", "fedora25"), ("fedora26", "fedora26"), ("fedora25", "fedora26")]
    result = []
    expected_result = ["Pass", "Pass", "Fail"]
    for tup in test_case:
        driver.get("http://localhost:8000/operating_system")
        name = driver.find_element_by_id("id_os_name")
        name.send_keys(tup[0])
        location = driver.find_element_by_id("id_os_location")
        location.send_keys(tup[1])
        submit = driver.find_element_by_id("add_os")
        submit.click()

        if "Operating System Added Successfully" in driver.page_source:
            result.append('Pass')
        else:
            result.append("Fail")
    assert result == expected_result
