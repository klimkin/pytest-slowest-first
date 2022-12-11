# -*- coding: utf-8 -*-


def test_help_message(testdir):
    result = testdir.runpytest(
        "--help",
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "slowest-first:",
            "*--sf, --slowest-first",
            "*Run the slowest tests first",
        ]
    )


def test_consequent_run_reorders_tests(testdir):
    testdir.makepyfile(
        """
        import time
        def test_fast():
            pass
        def test_slow():
            time.sleep(0.1)
        """
    )
    testdir.runpytest("--sf")
    result = testdir.runpytest("--sf", "--collect-only")
    result.stdout.fnmatch_lines(
        [
            "*test_slow*",
            "*test_fast*",
        ]
    )


def test_running_with_xdist_loadgroup_interleaves_worker_markers(testdir):
    testdir.makepyfile(
        """
        import time
        import pytest
        @pytest.mark.parametrize("i", range(4))
        def test(i):
            time.sleep(0.1 * i)
        """
    )
    testdir.runpytest("--sf", "-n2", "--dist=loadgroup")
    result = testdir.runpytest("--sf", "-n2", "--dist=loadgroup", "-v")
    result.stdout.fnmatch_lines(
        [
            "*gw0*::test*3*",
            "*gw0*::test*1*",
        ]
    )
    result.stdout.fnmatch_lines(
        [
            "*gw1*::test*2*",
            "*gw1*::test*0*",
        ]
    )
