import pygame

from . import types


class Camera2D:
    def __init__(
        self, pos: types.Coordinate, viewport: types.Coordinate, zoom: float = 1
    ):
        self.pos: pygame.Vector2 = pos
        self.viewport = viewport
        self.zoom: float = zoom

    @property
    def pos(self) -> pygame.Vector2:
        return self._pos

    @pos.setter
    def pos(self, value: types.Coordinate):
        self._pos = pygame.Vector2(value)

    @property
    def viewport(self) -> pygame.FRect:
        return self._viewport

    @viewport.setter
    def viewport(self, value: types.Coordinate):
        self._viewport = pygame.FRect(0, 0, *value)

    def translate(self, world_pos: types.Coordinate) -> pygame.Vector2:
        distance = world_pos - self.pos
        return distance * self.zoom

    def follow(
        self,
        target: types.Coordinate,
        lerp_speed: float = 1,
        freedom_box: pygame.Rect | pygame.FRect | None = None,
    ) -> None:
        if freedom_box is not None:
            if freedom_box.collidepoint(target - self.pos):
                return

        self.pos = round(self.pos.lerp(target, lerp_speed))
