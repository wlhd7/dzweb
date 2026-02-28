import pytest
from dzweb.db import get_db, get_all_apps

def test_get_all_apps(app):
    with app.app_context():
        apps = get_all_apps()
        assert len(apps) == 2
        assert apps[0]['appname'] == 'App 1'
        assert apps[1]['appname'] == 'App 2'
