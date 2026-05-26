"""UI configuration constants for simple-chess-python."""

# Board has 8x8 squares; each square is SQUARE_SIZE pixels.
SQUARE_SIZE: int = 80
BOARD_SIZE: int = 8

WINDOW_WIDTH: int = BOARD_SIZE * SQUARE_SIZE   # 640
WINDOW_HEIGHT: int = BOARD_SIZE * SQUARE_SIZE  # 640
WINDOW_TITLE: str = "Simple Chess"

FPS: int = 30

# Board square colors — used by board_renderer.
# Classic chess palette: cream for light squares, brown for dark squares.
LIGHT_SQUARE_COLOR: tuple[int, int, int] = (240, 217, 181)
DARK_SQUARE_COLOR: tuple[int, int, int] = (181, 136, 99)
