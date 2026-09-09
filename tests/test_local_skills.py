import importlib, os, sys
from importlib.metadata import entry_points
from pathlib import Path

import pytest
from fastcore.basics import first
from pyskills.core import enable_local_skills, list_pyskills


def test_local_skills(tmp_path):
    team = tmp_path
    project = team/'orchard'
    shared,local = team/'PYSKILLs',project/'PYSKILLs'
    shared.mkdir()
    local.mkdir(parents=True)
    (shared/'orchard_tools.py').write_text(r'''"""Team orchard tools."""
region = "team"''')
    (local/'orchard_tools.py').write_text(r'''"""Project orchard tools."""
region = "project"''')
    (shared/'orchard_checks').mkdir()
    (shared/'orchard_checks'/'__init__.py').write_text(r'''"""Shared orchard checks."""
from .helpers import answer''')
    (shared/'orchard_checks'/'helpers.py').write_text('answer = 42')
    (local/'_private.py').write_text('raise RuntimeError("Do not import private helpers during discovery")')
    cwd = Path.cwd()
    (local/'json.py').write_text('"""This name belongs to an existing module."""')
    with pytest.raises(ValueError, match='conflicts'): enable_local_skills(project)
    (local/'json.py').unlink()
    finder = enable_local_skills(project)
    try:
        assert enable_local_skills(project) is finder
        with pytest.raises(ValueError, match='already'): enable_local_skills(team)
        eps = entry_points().select(group='pyskills')
        assert list_pyskills()['orchard_tools'] == 'Project orchard tools.'
        assert 'orchard_checks' in list_pyskills() and '_private' not in list_pyskills()
        assert 'orchard_checks' not in sys.modules and 'orchard_tools' not in sys.modules
        orchard_tools = importlib.import_module('orchard_tools')
        orchard_checks = importlib.import_module('orchard_checks')
        assert orchard_tools.region == 'project'
        assert orchard_checks.answer == 42
        assert first(eps, lambda e: e.value=='orchard_tools').load() is orchard_tools
        os.chdir(team)
        assert list_pyskills()['orchard_tools'] == 'Project orchard tools.'
        (local/'orchard_season.py').write_text(r'''"""Harvest calendar."""
year = 2026''')
        assert 'orchard_season' in list_pyskills()
        orchard_season = importlib.import_module('orchard_season')
        assert orchard_season.year == 2026
    finally:
        os.chdir(cwd)
        sys.meta_path.remove(finder)
        for name in ('orchard_tools', 'orchard_checks', 'orchard_checks.helpers', 'orchard_season'): sys.modules.pop(name, None)
        importlib.invalidate_caches()
