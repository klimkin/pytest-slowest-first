# Welcome to pytest-slowest-first

*pytest-slowest-first* is a pytest plugin that sorts tests by their
previous execution time. When running in parallel, running slowest tests
first can help to reduce the overall execution time.

Example command line usage:

    pytest --sf -n auto --dist=loadscope
