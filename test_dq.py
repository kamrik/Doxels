import os

import dq


REPO_PATH = os.path.join(os.path.dirname(__file__), '..', 'doxels')


def test_dummy():
    assert 1 == 1


def test_repo_and_query():
    repo = dq.Repo(REPO_PATH)
    assert len(repo) > 0
    assert len(repo.query('todo easy')) > 0


def test_parse_props():
    props = dq.parse_props(['.zetag .foo = bar'])
    assert props['foo'] == 'bar'
    assert props['zetag']
