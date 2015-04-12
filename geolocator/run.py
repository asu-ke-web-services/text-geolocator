# -*- coding: utf-8 -*-
from flask_failsafe import failsafe


def test_run():
    from flask_script import Manager
    manager = create_app()
    assert isinstance(manager, Manager)


@failsafe
def create_app():
    from app import manager
    return manager

if __name__ == '__main__':
    create_app().run()
