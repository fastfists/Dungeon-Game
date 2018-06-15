""" Dungeon Object Testing """

import src
from unittest.mock import Mock
import src.artifacts as artifacts
import pytest
from src.classydungeon import Dungeon


#####################################
#          Test Emmiter             #
#####################################
@pytest.fixture(params=[lambda obj: False, lambda obj: True])
def stop_cond(request):
    return request.param


class thing:
    def draw(self):
        pass

    def update(self):
        pass


def test_emmiter_load(stop_cond):
    e = artifacts.Emitter(thing, stop_cond, cooldown=0)
    assert len(e) == 0
    e.load()
    assert len(e) == 1
    e.load()
    e.load()
    assert len(e) == 3


def test_emmiter_cooldown():
    e = artifacts.Emitter(thing, lambda obj: True, cooldown=3)
    e.load()
    e.update()
    e.load()  # This should not execute due to the cooldown
    assert len(e) == 1
    e.update()
    e.update()
    e.load()
    assert len(e) == 2


def test_emmiter_remove():
    e = artifacts.Emitter(thing, lambda obj: False, cooldown=3)
    e.load()
    assert len(e) == 1
    e.update()  # Shold remove element from list
    assert len(e) == 0


def test_emmiter_call_update(stop_cond):
    pass


def test_emmiter_call_draw(stop_cond):
    pass

#####################################
#         Test Projectiles          #
#####################################
