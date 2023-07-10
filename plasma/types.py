from typing import TypeAlias, Sequence

import pygame

Coordinate: TypeAlias = tuple[float, float] | list[float] | pygame.Vector2 | Sequence[float]
