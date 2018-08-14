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

@pytest.fixture
def loaded_emmiter():
    """A loaded emmiter with no cooldown and a true stop cond"""
    e = artifacts.Emitter(test_object, lambda self: True, cooldown=0)
    e.load()
    return e

class test_object:
    draw = Mock()
    update = Mock()
    kill = Mock()

def test_emmiter_load(stop_cond):
    e = artifacts.Emitter(test_object, stop_cond, cooldown=0)
    assert len(e) == 0
    e.load()
    assert len(e) == 1
    e.load()
    e.load()
    assert len(e) == 3


def test_emmiter_cooldown():
    e = artifacts.Emitter(test_object, lambda obj: True, cooldown=3)
    e.load()
    e.update()
    e.load()  # This should not load due to the cooldown
    assert len(e) == 1
    e.update()
    e.update()
    e.load()
    assert len(e) == 2


def test_emmiter_remove_elemetns():
    e = artifacts.Emitter(test_object, lambda obj: False, cooldown=3)
    e.load()
    element = e.elements_instances[0]
    assert len(e) == 1
    e.update()  # Shold remove element from list
    element.kill.assert_called()
    assert len(e) == 0


def test_emmiter_calls_draw(loaded_emmiter):
    e = loaded_emmiter
    e.update()
    element = e.elements_instances[0]
    element.draw.assert_called()

def test_emmiter_calls_draw(loaded_emmiter):
    e = loaded_emmiter
    e.emit()
    element = e.elements_instances[0]
    element.update.assert_called()


#####################################
#         Test Projectiles          #
#####################################
