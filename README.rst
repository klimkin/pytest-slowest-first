====================
pytest-slowest-first
====================

.. image:: https://img.shields.io/pypi/v/pytest-slowest-first.svg
    :target: https://pypi.org/project/pytest-slowest-first
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-slowest-first.svg
    :target: https://pypi.org/project/pytest-slowest-first
    :alt: Python versions

.. image:: https://ci.appveyor.com/api/projects/status/github/klimkin/pytest-slowest-first?branch=master
    :target: https://ci.appveyor.com/project/klimkin/pytest-slowest-first/branch/master
    :alt: See Build Status on AppVeyor

Sort tests by their last duration, slowest first.

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s
`cookiecutter-pytest-plugin`_ template.


Features
--------

* Sort tests on consecutive runs by their last duration, slowest first.
* Works with `pytest-xdist`_ by pre-assigning tests to workers based on their
  last duration.


Requirements
------------

* pytest
* pytest-xdist (optional)


Installation
------------

You can install "pytest-slowest-first" via `pip`_ from `PyPI`_::

    $ pip install pytest-slowest-first


Usage
-----

For best results, use this plugin with `pytest-xdist`_ to run tests in parallel.
When used together, make sure to pass ``--dist=loadgroup`` to `pytest`_ to
ensure that tests are distributed evenly across workers.

Example command line::

    $ pytest --sf -n auto --dist=loadgroup


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-slowest-first" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/klimkin/pytest-slowest-first/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`pytest-xdist`: https://github.com/pytest-dev/pytest-xdist
