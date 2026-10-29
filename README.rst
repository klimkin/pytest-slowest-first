====================
pytest-slowest-first
====================

.. image:: https://img.shields.io/pypi/v/pytest-slowest-first.svg
    :target: https://pypi.org/project/pytest-slowest-first
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-slowest-first.svg
    :target: https://pypi.org/project/pytest-slowest-first
    :alt: Python versions

.. image:: https://github.com/klimkin/pytest-slowest-first/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/klimkin/pytest-slowest-first/actions/workflows/ci.yml
    :alt: CI status

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

* Python >= 3.10
* pytest >= 7.0, < 9.2
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

Other xdist schedulers keep their own distribution policy. Existing
``xdist_group`` markers keep their worker affinity with ``loadgroup``.
Durations recorded in parallel also apply to later serial runs.

pytest 9.2 changed test node IDs in a way that breaks grouping in
pytest-xdist 3.8. Use pytest below 9.2 until pytest-xdist supports that change.

Example command line::

    $ pytest --sf -n auto --dist=loadgroup


Contributing
------------
Install `uv`_, then sync the development environment from the lockfile::

    $ uv sync --locked

Run tests, lint, and build distributions::

    $ uv run --locked pytest tests
    $ uv run --locked flake8 --max-line-length 100 pytest_slowest_first.py tests
    $ uv build

Dependencies and package metadata live in ``pyproject.toml``. Commit
``uv.lock`` after changing dependencies with ``uv add`` or ``uv lock``.
GitHub Actions runs on pull requests and pushes to ``main``. Tests and lint
use the locked environment on Linux and Windows with Python 3.10 through 3.14.

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
.. _`uv`: https://docs.astral.sh/uv/getting-started/installation/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`pytest-xdist`: https://github.com/pytest-dev/pytest-xdist
