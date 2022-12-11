# -*- coding: utf-8 -*-
from __future__ import annotations

import os

import pytest

_execution_time_key = pytest.StashKey[float]()


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


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    # Load the saved execution times from the cache
    execution_times = config.cache.get("execution_times", {})

    if config.option.slowest_first:
        items.sort(key=lambda item: execution_times.get(item.nodeid, 0), reverse=True)
        xdist_workers = int(os.environ.get("PYTEST_XDIST_WORKER_COUNT", 0))
        if xdist_workers > 1:
            _assign_xdist_workers(items, xdist_workers)

    # Reset execution time
    for item in items:
        item.stash[_execution_time_key] = 0


def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """Save aggregated duration of the item calls to the cache."""
    # Aggregate setup and call phases
    item.stash[_execution_time_key] += call.duration
    # Save execution time to the cache
    execution_times = item.config.cache.get("execution_times", {})
    execution_times[item.nodeid] = item.stash[_execution_time_key]
    item.config.cache.set("execution_times", execution_times)


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
            i.add_marker(pytest.mark.xdist_group(name=f"w{w}"))
