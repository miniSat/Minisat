from django.test import TestCase  # NOQA
import os
# Create your tests here.


def test_pep8():
    response = os.system("flake8 --ignore=E501,E122 mini main_app")
    assert response == 0
