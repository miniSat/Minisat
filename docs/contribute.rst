Contribute
==========

Minisat is an open source project that’s licensed under the GNU General Public License version 3. All contributions gladly accepted as long as they follow our programming guidelines.

**Setting up the development**

To create a development environment follow steps given for Minisat `installation <http://minisat.readthedocs.io/en/latest/installation.html>`_.

**Setting up test environment**

`Pytest <https://docs.pytest.org/en/latest/>`_ is used for testing and `Travis-ci <https://travis-ci.com/>`_ for Continuous Integration.
Pull requests are tested against testcases by `Travis-ci <https://travis-ci.org/miniSat/Minisat>`_. If your pull request didn't pass our test cases, you can visit the test job that failed and view its console output.

It is possible for you to run these same tests locally. To setup a testing environment, you need to download `Selenium <http://www.seleniumhq.org/>`_ webdriver for Mozilla Firefox at `mozilla geckodriver <https://github.com/mozilla/geckodriver/releases>`_.

Extract the driver.

Export path

.. code-block:: console

    # export PATH=$PATH/:/path/of/driver

It will set a path variable to the webdriver.

And run the test

.. code-block:: console

    # pytest

To check whether your programming style matches our, use *flake8* 

.. code-block:: console

    # flake8 --ignore=E501,E122,E722 minisat satellite

**Submit Patches**

Patches to fix bugs are always appreciated. Before introducing a new feature, create an issue first. If you are going to work on a specific issue, make a note in the issue section so that everyone knows what you’re working on. Please try to create an issue which is specific for your patch details.
- Fork the project and Clone it

On GitHub, navigate to the `Minisat repository <https://github.com/miniSat/minisat/>`_. In the top-right corner of the page, click Fork.


To clone repo

.. code-block:: console

    # git clone https://github.com/<your-user-name>/minisat.git

- Create a feature/topic branch

.. code-block:: console

    # git checkout -b <branchName>

- Make the changes required and commit the code

.. code-block:: console
    
    # git add <modifiedFile(s)>
    # git commit -m "Fixes #<bug> - <message>"

- Push topic branch to your fork

.. code-block:: console
    
    # git push origin <branchName>

- Create a pull request from *<branchName>* to *testing* branch.

To create pull request follow the `link <https://help.github.com/articles/about-pull-requests/>`_.
