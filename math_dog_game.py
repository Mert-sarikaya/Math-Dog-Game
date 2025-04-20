import pygame
import random
import sys
import time
from PIL import Image

# Fonksiyon: Buton benzeri metin kutusu çizimi
def draw_label_box(text, font, text_color, box_color, x, y, padding=10, radius=15):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    box_rect = pygame.Rect(x, y, text_rect.width + 2*padding, text_rect.height + 2*padding)

    pygame.draw.rect(screen, box_color, box_rect, border_radius=radius)
    screen.blit(text_surface, (box_rect.x + padding, box_rect.y + padding))

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
BLUE = (0, 100, 255)
BG_COLOR = (200, 230, 255)

# Ekran ayarları
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matematik Oyunu - Köpeğe Mama!")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Görselleri yükle
dog_image_path = "/Users/mertsarikaya/Desktop/adsız klasör 4/indir.png"
food_image_paths = [
    "/Users/mertsarikaya/Desktop/adsız klasör 4/mamaKabi.png",
    "/Users/mertsarikaya/Desktop/adsız klasör 4/mamaKabi2.png",
    "/Users/mertsarikaya/Desktop/adsız klasör 4/mamaKabi3.png"
]

try:
    dog_img = pygame.image.load(dog_image_path).convert_alpha()
    food_images = [pygame.image.load(path).convert_alpha() for path in food_image_paths]
except pygame.error as e:
    print("Görsel yüklenirken hata oluştu:", e)
    sys.exit()

# Boyutlandır
dog_img = pygame.transform.scale(dog_img, (200, 100))
food_images = [pygame.transform.scale(img, (60, 60)) for img in food_images]

# Mama kabı parıltısı için yüzey (sarı daire gibi)
glow_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
pygame.draw.circle(glow_surface, (255, 255, 100, 100), (40, 40), 40)

# GIF Yükleyici
def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frame = gif.convert('RGBA')
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            pygame_image = pygame.image.fromstring(data, size, mode)
            frames.append(pygame_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

# Mutlu köpek gif karelerini yükle
gif_path = "/Users/mertsarikaya/Desktop/adsız klasör 4/happydog.gif"
gif_frames = load_gif_frames(gif_path)
gif_frame_index = 0
gif_frame_timer = 0

# Konumlar
dog_rect = dog_img.get_rect()
dog_rect.bottomleft = (600, 550)

# Başlangıç mama görseli
current_food_index = 0
food_img = food_images[current_food_index]
food_rect = food_img.get_rect()
food_rect.bottomleft = (100, 550)

# Soru üretici
def generate_question():
    operation = random.choice(["+", "-", "*", "/"])
    if operation == "/":
        b = random.randint(1, 10)
        answer = random.randint(1, 10)
        a = b * answer
        question = f"{a} / {b}"
    else:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        question = f"{a} {operation} {b}"
        answer = eval(question)
    return question, answer

# Oyunu sıfırla
def reset_game():
    global current_question, correct_answer, user_input, food_moving
    global score, start_time, oyun_bitti, flash_animation
    global current_food_index, food_img
    global gif_frame_index, gif_frame_timer
    global mama_animasyon, mama_animasyon_timer, mama_animasyon_scale

    current_question, correct_answer = generate_question()
    user_input = ""
    food_rect.x = 100
    food_moving = False
    score = 0
    start_time = time.time()
    oyun_bitti = False
    flash_animation = False

    current_food_index = 0
    food_img = food_images[current_food_index]

    gif_frame_index = 0
    gif_frame_timer = 0

    mama_animasyon = False
    mama_animasyon_timer = 0
    mama_animasyon_scale = 1.0

# Başlangıç ayarları
score = 0
best_score = 0
reset_game()
error_flash = False
error_flash_timer = 0

# Animasyon ayarları
flash_count = 0
flash_colors = [RED, WHITE, BLUE]
current_flash_index = 0

# Ana döngü
while True:
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, 60 - elapsed_time)

    if remaining_time == 0 and not flash_animation and not oyun_bitti:
        if score > best_score:
            best_score = score
            flash_animation = True
            flash_count = 15
        else:
            oyun_bitti = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not oyun_bitti and not flash_animation:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.strip() != "":
                        try:
                            if int(user_input) == correct_answer:
                                food_moving = True
                                score += 1

                                new_index = min(len(food_images) - 1, score // 3)
                                if new_index != current_food_index:
                                    current_food_index = new_index
                                    food_img = food_images[current_food_index]

                                    mama_animasyon = True
                                    mama_animasyon_timer = 20
                                    mama_animasyon_scale = 1.5
                            else:
                                error_flash = True
                                error_flash_timer = 10
                                user_input = ""
                        except ValueError:
                            user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit() or (event.unicode == '-' and user_input == ''):
                    user_input += event.unicode
        elif oyun_bitti:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

    if error_flash:
        screen.fill(RED)
        error_flash_timer -= 1
        if error_flash_timer <= 0:
            error_flash = False
    elif flash_animation:
        screen.fill(flash_colors[current_flash_index])
        current_flash_index = (current_flash_index + 1) % len(flash_colors)
        flash_count -= 1
        if flash_count <= 0:
            flash_animation = False
            oyun_bitti = True
    elif not oyun_bitti:
        screen.fill(BG_COLOR)

    if not oyun_bitti and not flash_animation and not error_flash:
        if food_moving:
            if food_rect.x < dog_rect.x:
                food_rect.x += 10
            else:
                food_moving = False
                user_input = ""
                food_rect.x = 100
                current_question, correct_answer = generate_question()

        draw_label_box(f"Soru: {current_question}", font, BLACK, (255, 255, 255), 50, 50)
        draw_label_box(f"Cevap: {user_input}", font, RED, (255, 255, 255), 50, 120)
        draw_label_box(f"Puan: {score}", font, BLACK, (230, 255, 230), 50, 200)
        draw_label_box(f"En İyi Skor: {best_score}", font, BLUE, (230, 230, 255), 50, 260)
        draw_label_box(f"Kalan Süre: {remaining_time}s", font, BLACK, (255, 240, 200), 50, 320)

        screen.blit(dog_img, dog_rect)

        if mama_animasyon:
            mama_animasyon_scale -= 0.025
            if mama_animasyon_scale < 1.0:
                mama_animasyon_scale = 1.0
            mama_animasyon_timer -= 1
            if mama_animasyon_timer <= 0:
                mama_animasyon = False

            glow_pos = (food_rect.x - 10, food_rect.y - 10)
            screen.blit(glow_surface, glow_pos)

        scaled_food = pygame.transform.scale(food_img, (
            int(60 * mama_animasyon_scale),
            int(60 * mama_animasyon_scale)
        ))
        scaled_rect = scaled_food.get_rect(center=food_rect.center)
        screen.blit(scaled_food, scaled_rect)

    elif oyun_bitti:
        screen.fill(BG_COLOR)
        result_text = font.render(f"Zaman doldu! Skorun: {score}", True, BLACK)
        best_text = font.render(f"En İyi Skor: {best_score}", True, BLUE)
        retry_text = font.render("Tekrar oynamak için 'R' tuşuna bas", True, RED)

        screen.blit(result_text, (200, 180))
        screen.blit(best_text, (200, 260))
        screen.blit(retry_text, (100, 340))

        # Alt kısımda GIF döngüsü
        if gif_frames:
            gif_frame_timer += 1
            if gif_frame_timer >= 5:
                gif_frame_index = (gif_frame_index + 1) % len(gif_frames)
                gif_frame_timer = 0

            gif_image = gif_frames[gif_frame_index]
            scaled_gif = pygame.transform.scale(gif_image, (gif_image.get_width() // 2, gif_image.get_height() // 2))
            scaled_rect = scaled_gif.get_rect(center=(WIDTH // 2, 500))
            screen.blit(scaled_gif, scaled_rect)

    pygame.display.flip()
    clock.tick(30)