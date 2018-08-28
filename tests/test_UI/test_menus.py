import pytest
import src.UI.menus as menus
import numpy as np

def test_center_modifiers():
    size = width, height = 10, 10
    offset = 4
    handle_num = 5
    cent = menus.MenuCentered(size, offset, handle_num)
    modify = cent.modify()

    assert next(modify) == -2
    assert next(modify) == -1
    assert next(modify) == 0
    assert next(modify) == 1
    assert next(modify) == 2

## rewrite theses tests
def test_menu_centered4():
    size = width, height = 10, 10
    offset = 4
    cent = menus.MenuCentered(size, offset, 4)
    assert cent() == (width // 2, (height//2) + offset * -1.5)
    assert cent() == (width // 2, (height//2) + offset * -0.5)
    assert cent() == (width // 2, (height//2) + offset * 0.5)
    assert cent() == (width // 2, (height//2) + offset * 1.5)

def test_menu_centerd5():
    size = width, height = 10, 10
    offset = 4
    cent = menus.MenuCentered(size, offset, 5)
    assert cent() == (width // 2, (height//2) + offset * -2)
    assert cent() == (width // 2, (height//2) + offset * -1)
    assert cent() == (width // 2, (height//2) + offset * 0)
    assert cent() == (width // 2, (height//2) + offset * 1)
    assert cent() == (width // 2, (height//2) + offset * 2)