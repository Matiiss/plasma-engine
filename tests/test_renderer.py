import itertools
from typing import NamedTuple

import pygame

from plasma.renderer import Renderer


def get_default_renderer() -> Renderer:
    return Renderer()


class StackItem(NamedTuple):
    surf: pygame.Surface
    rect: pygame.Rect | pygame.FRect
    z_index: int | None


def get_test_stack() -> list[StackItem]:
    return [
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), None),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), None),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), None),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(1, 0, 10, 10), None),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(2, 0, 10, 10), None),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(3, 0, 10, 10), None),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), 0),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), 0),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), 0),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(1, 0, 10, 10), 0),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(2, 0, 10, 10), 0),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(3, 0, 10, 10), 0),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), 1),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), 1),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), 1),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(0, 0, 10, 10), 2),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(1, 0, 10, 10), 2),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(2, 0, 10, 10), 2),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(-100, 0, 10, 10), 0),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(-100, 0, 10, 10), 2),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(20000, 0, 10, 10), 0),
        StackItem(pygame.Surface((10, 10)), pygame.FRect(300000, 0, 10, 10), 1),
    ]


class TestRenderer:
    def test_append_to_stack(self):
        renderer = get_default_renderer()
        items = get_test_stack()
        for item in items:
            surf, rect, z_index = item
            renderer.append_to_stack(surf, rect, z_index)

        # check the first tuple at layer 0
        assert len(renderer.stack[0][0]) == 2

        assert len(renderer.stack[0]) == len(
            [item for item in items if item.z_index in (0, None)]
        )

        for z_index in set(item.z_index for item in items):
            if z_index in (0, None):
                continue

            assert len(renderer.stack[z_index]) == len(
                [item for item in items if item.z_index == z_index]
            )

    def test_stack_filter_viewport(self):
        renderer = get_default_renderer()
        items = get_test_stack()
        for item in items:
            surf, rect, z_index = item
            renderer.append_to_stack(surf, rect, z_index)

        renderer.filter_viewport()

        left_items = [
            item for item in items if item.rect.colliderect(renderer.viewport)
        ]
        assert sum(map(len, renderer.stack.values())) == len(left_items)

    def test_stack_sort(self):
        renderer = get_default_renderer()
        items = get_test_stack()
        for item in items:
            surf, rect_, z_index = item
            renderer.append_to_stack(surf, rect_, z_index)

        renderer.stack_sort(key=lambda rect: rect.topleft)

        for z_index in set(item.z_index or 0 for item in items):
            assert renderer.stack[z_index] == sorted(
                [(item.surf, item.rect) for item in items if item.z_index == z_index],
                key=lambda tpl: tpl[1].topleft,
            )

    def test_render_stack(self):
        renderer = get_default_renderer()
        items = get_test_stack()
        colors = itertools.cycle(["red", "green", "blue"])
        for idx, item in enumerate(items):
            surf, rect_, z_index = item
            if idx % 3 == 0:
                surf.fill(next(colors))
            renderer.append_to_stack(surf, rect_, z_index)

        renderer.filter_viewport()
        filtered_items = [
            item for item in items if item.rect.colliderect(renderer.viewport)
        ]

        renderer.render_stack()
        for item in filtered_items:
            assert renderer.get_at(item.rect.topleft) == item.surf.get_at((0, 0))

