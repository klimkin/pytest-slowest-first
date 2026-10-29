# -*- coding: utf-8 -*-

import json

import pytest


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
    result.assert_outcomes(passed=4)
    result.stdout.fnmatch_lines(["*::test[[]3[]]@slowest-first-w0*"])
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


def test_xdist_run_records_every_test_duration(pytester):
    pytester.makepyfile(
        """
        import pytest
        @pytest.mark.parametrize("i", range(200))
        def test(i):
            pass
        """
    )
    pytester.runpytest("-n4").assert_outcomes(passed=200)
    result = pytester.runpytest("--cache-show", "execution_times")
    assert sum("::test[" in line for line in result.outlines) == 200


@pytest.mark.parametrize("workers", [0, 2])
def test_slowest_first_without_cacheprovider(pytester, workers):
    pytester.makepyfile("def test(): pass")
    pytester.runpytest("--sf", f"-n{workers}", "-p", "no:cacheprovider").assert_outcomes(passed=1)


@pytest.mark.parametrize("workers", [0, 2])
def test_grouped_durations_reorder_serial_collection(pytester, workers):
    pytester.makepyfile(
        """
        import pytest
        @pytest.mark.xdist_group('database@primary')
        @pytest.mark.parametrize('name', ['fast@host', 'slow@host'])
        def test_duration(name):
            pass
        """
    )
    pytester.makeconftest(
        """
        import pytest
        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtest_makereport(item, call):
            outcome = yield
            report = outcome.get_result()
            report.duration = 0.0
            if call.when == 'call':
                report.duration = 10.0 if 'slow' in item.name else 1.0
        """
    )
    pytester.runpytest(f"-n{workers}", "--dist=loadgroup").assert_outcomes(passed=2)
    durations = json.loads((pytester.path / ".pytest_cache/v/execution_times").read_text())
    assert durations == {
        "test_grouped_durations_reorder_serial_collection.py::test_duration[fast@host]": 1.0,
        "test_grouped_durations_reorder_serial_collection.py::test_duration[slow@host]": 10.0,
    }
    result = pytester.runpytest("--sf", "--collect-only", "-q")
    result.stdout.fnmatch_lines(
        ["*::test_duration[[]slow@host[]]", "*::test_duration[[]fast@host[]]"]
    )


def test_slowest_first_preserves_user_groups(pytester):
    pytester.makepyfile(
        """
        from pathlib import Path
        import pytest
        pytestmark = pytest.mark.xdist_group('database')
        @pytest.mark.parametrize('i', range(4))
        def test_shared_resource(i, worker_id):
            Path(__file__).with_name(f'worker-{i}').write_text(worker_id)
        """
    )
    result = pytester.runpytest("--sf", "-n2", "--dist=loadgroup", "-v")
    result.assert_outcomes(passed=4)
    assert len({path.read_text() for path in pytester.path.glob('worker-*')}) == 1
    assert "@database_slowest-first" not in result.stdout.str()
