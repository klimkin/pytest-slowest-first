from __future__ import annotations

import os

import pytest

_CACHE_KEY = "execution_times"
_NODEID_PROPERTY = "slowest_first_nodeid"


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("slowest_first", "slowest-first")
    group.addoption(
        "--sf",
        "--slowest-first",
        dest="slowest_first",
        action="store_true",
        default=False,
        help="Run the slowest tests first",
    )


class DurationRecorder:
    """Sum setup, call and teardown durations, then merge them into the cache once.

    Under pytest-xdist only the controller records: it receives every worker
    report, so workers never race on the shared cache file.
    """

    def __init__(self, cache: pytest.Cache) -> None:
        self.cache = cache
        self.durations: dict[str, float] = {}

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        nodeid = next(
            (
                value
                for name, value in report.user_properties
                if name == _NODEID_PROPERTY
            ),
            report.nodeid,
        )
        self.durations[nodeid] = self.durations.get(nodeid, 0.0) + report.duration

    def pytest_sessionfinish(self) -> None:
        if self.durations:
            self.cache.set(
                _CACHE_KEY, {**self.cache.get(_CACHE_KEY, {}), **self.durations}
            )


def pytest_configure(config: pytest.Config) -> None:
    # `config.cache` is absent under `-p no:cacheprovider`.
    cache = getattr(config, "cache", None)
    if cache is not None and not hasattr(config, "workerinput"):
        config.pluginmanager.register(DurationRecorder(cache), "slowest-first-recorder")


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    for item in items:
        item.user_properties.append((_NODEID_PROPERTY, item.nodeid))
    cache = getattr(config, "cache", None)
    if not config.option.slowest_first or cache is None:
        return
    execution_times = cache.get(_CACHE_KEY, {})
    items.sort(key=lambda item: execution_times.get(item.nodeid, 0), reverse=True)
    xdist_workers = int(os.environ.get("PYTEST_XDIST_WORKER_COUNT", "0"))
    if xdist_workers > 1 and config.getoption("loadgroup", False):
        _assign_xdist_workers(items, xdist_workers)


def _assign_xdist_workers(items: list[pytest.Item], xdist_workers: int) -> None:
    """Assign xdist groups to schedule slowest jobs first using `loadgroup`
    distribution mode.

    Default xdist policy assigns jobs sequentially to every worker without
    a round-robin. The scheduling order example for `load` mode is
    `[0, 1], [2, 3]`. After assigning markers and using `loadgroup` mode, the
    scheduling order is `[0, 2], [1, 3]`.
    """
    for w in range(xdist_workers):
        for i in items[w::xdist_workers]:
            if i.get_closest_marker("xdist_group") is None:
                i.add_marker(pytest.mark.xdist_group(name=f"slowest-first-w{w}"))
