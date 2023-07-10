import pygame
import pytest

from plasma.camera import Camera2D


def get_default_camera2d():
    return Camera2D()


class TestCamera2D:
    def test_requires_arguments(self):
        with pytest.raises(TypeError):
            Camera2D()

    def test_attributes(self):
        camera = get_default_camera2d()
        assert hasattr(camera, "pos")
        assert hasattr(camera, "viewport")
        assert hasattr(camera, "zoom")

    def test_translate(self):
        camera = get_default_camera2d()
        cases = [(0, 0), (-10, -10), (10, 10)]
        for case in cases:
            assert camera.translate(case) == case

        camera.pos = (10, 10)
        for case in cases:
            x, y = case
            assert camera.translate(case) == (x - 10, y - 10)

        camera.pos = (-10, -10)
        for case in cases:
            x, y = case
            assert camera.translate(case) == (x + 10, y + 10)

    def test_translate_with_zoom(self):
        camera = get_default_camera2d()
        cases = [(0, 0), (-10, -10), (10, 10)]
        zooms = [0.25, 0.5, 2, 4]

        for zoom in zooms:
            camera.zoom = zoom
            for case in cases:
                assert camera.translate(case) == (case[0] * zoom, case[1] * zoom)

            camera.pos = (10, 10)
            for case in cases:
                x, y = case
                assert camera.translate(case) == ((x - 10) * zoom, (y - 10) * zoom)

            camera.pos = (-10, -10)
            for case in cases:
                x, y = case
                assert camera.translate(case) == ((x + 10) * zoom, (y + 10) * zoom)

    def test_center_property(self):
        camera = get_default_camera2d()
        w, h = camera.viewport.size

        camera.center = (0, 0)
        assert camera.pos == (-(w / 2), -(h / 2))

    def test_follow(self):
        camera = get_default_camera2d()
        initial_x, initial_y = 0, 0
        target_x, target_y = 640, 360
        delta_x, delta_y = target_x - initial_x, target_y - initial_y

        for lerp_speed in [0, 0.5, 1]:
            camera.pos = (initial_x, initial_y)
            camera.follow((target_x, target_y), lerp_speed)
            assert camera.pos == (
                initial_x + delta_x * lerp_speed,
                initial_y + delta_y * lerp_speed,
            )

        camera.pos = (initial_x, initial_y)
        camera.follow(
            (initial_x + camera.viewport.centerx, initial_y + camera.viewport.centery)
        )
        assert camera.pos == (initial_x, initial_y)

    def test_freedom_box(self):
        camera = get_default_camera2d()
        initial_x, initial_y = 0, 0
        center_x, center_y = (
            initial_x + camera.viewport.centerx,
            initial_y + camera.viewport.centery,
        )

        freedom_box = pygame.Rect(0, 0, 64, 36)
        freedom_box.center = camera.viewport.center

        camera.pos = (initial_x, initial_y)
        camera.follow((center_x, center_y), 1, freedom_box=freedom_box)
        assert camera.pos == (initial_x, initial_y)

        camera.pos = (initial_x, initial_y)
        camera.follow(
            (center_x + freedom_box.width / 2, center_y + freedom_box.height / 2),
            1,
            freedom_box=freedom_box,
        )
        assert camera.pos == (initial_x, initial_y)

        camera.pos = (initial_x, initial_y)
        camera.follow(
            (center_x + freedom_box.width, center_y + freedom_box.height),
            1,
            freedom_box=freedom_box,
        )
        assert camera.pos == (
            initial_x + freedom_box.width / 2,
            initial_y + freedom_box.height / 2,
        )
