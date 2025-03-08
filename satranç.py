import pygame
import chess
import chess.engine
import time

# Stockfish'in yolu
STOCKFISH_PATH = ""

# Pygame başlat
pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess_2.0_")

# Font ayarları
FONT = pygame.font.SysFont("Arial", 14, bold=True)
FONT_LARGE = pygame.font.SysFont("Arial", 24, bold=True)

# Renkler
LIGHT = (238, 238, 210)
DARK = (118, 150, 86)
RED = (200, 0, 0)  # Şah çekildiğinde kırmızı renk
YELLOW = (255, 255, 0)  # Seçilen taşın etrafı için sarı
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)  # Gidebilecek kareler için gri

# Satranç tahtası ve motor başlat
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
# Satranç tahtası ve motor başlat

# Skill Level'ı 10 olarak ayarla
engine.configure({"Skill Level": 0})

# Satranç taşlarını yükle
piece_images = {}
piece_conversion = {
    "P": "wP", "R": "wR", "N": "wN", "B": "wB", "Q": "wQ", "K": "wK",
    "p": "bP", "r": "bR", "n": "bN", "b": "bB", "q": "bQ", "k": "bK"
}

for piece in piece_conversion.values():
    piece_images[piece] = pygame.transform.scale(
        pygame.image.load(f"pieces/{piece}.png"), (SQ_SIZE, SQ_SIZE)
    )



def draw_board():
    """ Satranç tahtasını çizer. """
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Harf ve rakam etiketleri ekleyelim
    for i in range(8):
        text = FONT.render(str(8 - i), True, BLACK)
        screen.blit(text, (5, i * SQ_SIZE + 5))  # Satır numaraları

        text = FONT.render(chr(ord('a') + i), True, BLACK)
        screen.blit(text, (i * SQ_SIZE + SQ_SIZE - 14, HEIGHT - 18))  # Sütun harfleri

    if board.is_check():
        king_square = board.king(chess.WHITE) if board.turn else board.king(chess.BLACK)
        row, col = 7 - chess.square_rank(king_square), chess.square_file(king_square)
        pygame.draw.rect(screen, RED, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces():
    """ Satranç taşlarını tahtaya çizer. """
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                piece_key = piece_conversion[piece.symbol()]
                screen.blit(piece_images[piece_key], (col * SQ_SIZE, row * SQ_SIZE))


def highlight_square(square):
    """ Seçilen taşın etrafını sarı bir çerçeveyle vurgular. """
    if square is not None:
        col, row = chess.square_file(square), 7 - chess.square_rank(square)
        pygame.draw.rect(screen, YELLOW, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 5)


def draw_legal_moves(square):
    """ Seçili taşın gidebileceği kareleri işaretler. """
    if square is not None:
        for move in board.legal_moves:
            if move.from_square == square:
                col, row = chess.square_file(move.to_square), 7 - chess.square_rank(move.to_square)
                pygame.draw.circle(screen, GRAY, (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2), 10)


def get_square_from_mouse(pos):
    """ Fare tıklanınca hangi kareye tıkladığımızı hesaplar. """
    x, y = pos
    col = x // SQ_SIZE
    row = 7 - (y // SQ_SIZE)
    return chess.square(col, row)


def animate_move(move):
    """ Taşların kayarak hareket etmesini sağlar. """
    start_col, start_row = chess.square_file(move.from_square), 7 - chess.square_rank(move.from_square)
    end_col, end_row = chess.square_file(move.to_square), 7 - chess.square_rank(move.to_square)
    piece = board.piece_at(move.from_square)

    if not piece:
        return

    piece_key = piece_conversion[piece.symbol()]
    frames = 20
    clock = pygame.time.Clock()

    for frame in range(frames):
        t = frame / frames
        x = start_col * SQ_SIZE * (1 - t) + end_col * SQ_SIZE * t
        y = start_row * SQ_SIZE * (1 - t) + end_row * SQ_SIZE * t

        draw_board()
        draw_pieces()
        screen.blit(piece_images[piece_key], (x, y))

        pygame.display.flip()
        clock.tick(60)

    draw_board()
    draw_pieces()
    pygame.display.flip()

def show_promotion_screen(square):
    """ Piyon promosyonu için seçim ekranını gösterir. """
    promotion_pieces = ["wQ", "wR", "wB", "wN"] if board.turn == chess.WHITE else ["bQ", "bR", "bB", "bN"]
    piece_names = ["Vezir", "Kale", "Fil", "At"]
    buttons = []

    # Seçim ekranını çiz
    screen.fill(LIGHT)
    text = FONT_LARGE.render("Taş Seçin", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

    for i, piece in enumerate(promotion_pieces):
        button = pygame.Rect(WIDTH // 2 - 100 + (i % 2) * 120, HEIGHT // 2 - 50 + (i // 2) * 120, 100, 100)
        buttons.append((button, piece))
        pygame.draw.rect(screen, DARK, button)
        screen.blit(piece_images[piece], (button.x + 10, button.y + 10))
        text = FONT.render(piece_names[i], True, WHITE)
        screen.blit(text, (button.centerx - text.get_width() // 2, button.centery + 40))

    pygame.display.flip()

    # Kullanıcı seçim yapana kadar bekle
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button, piece in buttons:
                    if button.collidepoint(mouse_pos):
                        return piece  # Seçilen taşı döndür


def handle_promotion(move):
    """ Piyon promosyonunu işler. """
    if move.promotion is None and board.piece_at(move.from_square).piece_type == chess.PAWN:
        if (chess.square_rank(move.to_square) == 7 and board.turn == chess.WHITE) or \
           (chess.square_rank(move.to_square) == 0 and board.turn == chess.BLACK):
            # Promosyon taşını seç
            promotion_piece = show_promotion_screen(move.to_square)
            move.promotion = chess.Piece.from_symbol(promotion_piece).piece_type
    return move


def show_checkmate_screen():
    """ Şah mat olduğunda ekrana 'Şah Mat' yazan bir ekran gösterir ve 'Yeniden Oyna' butonu ekler. """
    screen.fill(LIGHT)

    # Şah Mat yazısı
    text = FONT_LARGE.render("Şah Mat!", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

    # Yeniden Oyna butonu
    replay_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, DARK, replay_button)
    replay_text = FONT_LARGE.render("Yeniden Oyna", True, WHITE)
    screen.blit(replay_text, (
    replay_button.centerx - replay_text.get_width() // 2, replay_button.centery - replay_text.get_height() // 2))

    pygame.display.flip()

    # Butona tıklanana kadar bekle
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Oyunu kapat
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if replay_button.collidepoint(mouse_pos):
                    return True  # Yeniden oyna


def show_start_screen():
    """ Başlangıç ekranını gösterir. """
    screen.fill(LIGHT)
    text = FONT_LARGE.render("Beyaz mı Siyah mı?", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

    white_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    black_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)

    pygame.draw.rect(screen, DARK, white_button)
    pygame.draw.rect(screen, DARK, black_button)

    text_white = FONT_LARGE.render("Beyaz", True, WHITE)
    text_black = FONT_LARGE.render("Siyah", True, WHITE)

    screen.blit(text_white, (white_button.centerx - text_white.get_width() // 2, white_button.centery - text_white.get_height() // 2))
    screen.blit(text_black, (black_button.centerx - text_black.get_width() // 2, black_button.centery - text_black.get_height() // 2))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                engine.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if white_button.collidepoint(mouse_pos):
                    return chess.WHITE
                elif black_button.collidepoint(mouse_pos):
                    return chess.BLACK


# Başlangıç ekranını göster ve kullanıcının seçimini al
player_color = show_start_screen()

if player_color is None:
    exit()

# Eğer kullanıcı siyahı seçerse, AI ilk hamleyi yapar
if player_color == chess.BLACK:
    result = engine.play(board, chess.engine.Limit(time=0.5))
    board.push(result.move)

selected_square = None
running = True
while running:
    draw_board()
    highlight_square(selected_square)
    draw_legal_moves(selected_square)
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square_from_mouse(pygame.mouse.get_pos())

            if selected_square is None or selected_square == square:
                if board.piece_at(square) and board.piece_at(square).color == player_color:
                    selected_square = square
                else:
                    selected_square = None
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    move = handle_promotion(move)  # Promosyon kontrolü
                    animate_move(move)
                    board.push(move)
                    pygame.time.delay(800)
                    if not board.is_game_over():
                        result = engine.play(board, chess.engine.Limit(time=0.5))
                        animate_move(result.move)
                        board.push(result.move)
                selected_square = None
        # Şah mat kontrolü
    if board.is_checkmate():
        replay = show_checkmate_screen()
        if replay:
            # Yeniden oyna butonuna tıklandıysa, oyunu sıfırla ve başlangıç ekranına dön
            board.reset()  # Tahtayı sıfırla
            player_color = show_start_screen()  # Başlangıç ekranını göster
            if player_color is None:
                running = False  # Kullanıcı oyunu kapattıysa
            elif player_color == chess.BLACK:
                # Eğer kullanıcı siyahı seçerse, AI ilk hamleyi yapar
                result = engine.play(board, chess.engine.Limit(time=0.5))
                board.push(result.move)
        else:
            running = False  # Oyunu kapat

pygame.quit()
engine.quit()

