from django.test import TestCase  # NOQA
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# Create your tests here.


def test_pep8():
    response = os.system("flake8 --ignore=E501,E122,E722 minisat satellite")
    assert response == 0


def test_compute_resource():
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
