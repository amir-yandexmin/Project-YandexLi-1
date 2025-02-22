# импортирую pygame
import pygame
# импортирую рандом
import random
import os
import sqlite3

import pygame

# Инициализация заставки
pygame.init()

# Размеры окна
screen_width = 1280
screen_height = 700

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("заставка")

# Загрузка изображения
background_image2 = pygame.image.load('i (1).webp')

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Переход к следующему экрану при нажатии любой клавиши
            running = False
    # Отображение фона
    screen.blit(background_image2, (0, 0))
    # Обновление экрана
    pygame.display.flip()

# Инициализация основной игры
pygame.init()

# кОнСтАнТы

WIDTH, HEIGHT = 800, 400
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = 10

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Класс Динозавра
class Dinosaur:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 60
        self.width = 40
        self.height = 40
        self.velocity_y = 0
        self.jumping = False
        self.image1 = pygame.image.load("dinosaur.png")  # Загрузка изображения

        # Изменяем размер изображения
        self.image1 = pygame.transform.scale(self.image1, (self.width + 20, self.height + 20))

    # Функия для отображения прыжка персонажа
    def jump(self):
        if not self.jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.jumping = True

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y >= HEIGHT - 60:
            self.y = HEIGHT - 60
            self.jumping = False
            self.velocity_y = 0

    # Отрисовка персонажа
    def draw(self, screen):
        # Отображение изображений
        screen.blit(self.image1, (self.x, self.y))

        # начинаю рисовать задний фон
        pygame.draw.ellipse(screen, 'GRAY', (640, 10, 150, 150))

        pygame.draw.rect(screen, 'GRAY', (0, 397, 800, 15))


# Класс Препятствия
class Obstacle:
    def __init__(self, x):
        self.x = x
        self.width = 20
        self.height = 40

        # Загружаю все картинки
        self.image2 = pygame.image.load("cacti---cacti2.png")
        self.image2 = pygame.transform.scale(self.image2, (self.width + 20, self.height + 20))

        self.image3 = pygame.image.load("cactus.png")
        self.image3 = pygame.transform.scale(self.image3, (self.width + 60, self.height + 25))

        self.image4 = pygame.image.load("cactus2.png")
        self.image4 = pygame.transform.scale(self.image4, (self.width + 60, self.height + 25))

        self.sp_kartinok = [self.image2, self.image3, self.image4]
        self.ran_cact = random.randint(0, 2)

        self.imagePT = pygame.image.load("3bc86bac27b48ed.png")
        self.imagePT = pygame.transform.scale(self.imagePT, (self.width + 60, self.height))

    def update(self):
        self.x -= 5

    def draw(self, screen):
        # Отображение изображения кактусов
        screen.blit(self.sp_kartinok[self.ran_cact], (self.x, HEIGHT - self.height - 20))

    def draw1(self, screen):
        # Отображение изображения птерадактеля
        screen.blit(self.imagePT, (self.x, HEIGHT - self.height - 190))


# Основная функция игры
def main():
    conn = sqlite3.connect("Dino_score.sqlite")
    cursor = conn.cursor()
    # рисую перый холст с длиной и шириной введынми раньше
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # меняю название
    pygame.display.set_caption("завр")
    clock = pygame.time.Clock()

    # Подключаю базу данных для изменнения рекордов

    # Ввожу переменные для использания их в дальнейшем
    dinosaur = Dinosaur()
    obstacles = []
    obstacles_pter = []
    score = 0
    spawn_timer = 0
    spawn_timer1 = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dinosaur.jump()

        # Обновление динозавра
        dinosaur.update()

        # Генерация препятствий
        spawn_timer1 += 1
        spawn_timer += 1
        kadri = random.randint(50, 144)
        kadri_pter = random.randint(400, 500)
        if spawn_timer > kadri:  # беру рандомное значение для разного расстояния между препятствиями
            obstacles.append(Obstacle(WIDTH))
            spawn_timer = 0

        # Обновление и отрисовка препятствий
        for obstacle in obstacles[:]:
            obstacle.update()
            if obstacle.x < 0:
                obstacles.remove(obstacle)
                score += 1
            obstacle.draw(screen)

        # отрисвока птерадактеля
        if spawn_timer1 > kadri_pter:  # беру рандомное значение для разного расстояния между препятствиями
            obstacles_pter.append(Obstacle(WIDTH))
            spawn_timer1 = 0

        for obstacle in obstacles_pter[:]:
            obstacle.update()
            if obstacle.x < 0:
                obstacles_pter.remove(obstacle)
            obstacle.draw1(screen)

        # Проверка на столкновение
        for obstacle in obstacles:
            if (dinosaur.x < obstacle.x + obstacle.width - 5 and
                    dinosaur.x + dinosaur.width > obstacle.x and
                    dinosaur.y + dinosaur.height > HEIGHT - obstacle.height - 30):
                print(f"Game Over!")

                sq = f'SELECT score from Scoress'
                cursor.execute(sq)
                sss = cursor.fetchall()[0][0]
                if int(sss) < score:
                    sqq = f'UPDATE Scoress set score = {score}'
                    cursor.execute(sqq)
                conn.commit()
                running = False

        # Отрисовка динозавра
        dinosaur.draw(screen)

        # Отображение счета

        CHET_IGROKA = pygame.font.Font(None, 40)
        text = CHET_IGROKA.render(f"Счёт: {score}", True, BLACK, 'GRAY')
        screen.blit(text, (10, 10))

        # Отображение лучшего рекорда
        sq1 = f'SELECT score from Scoress'
        cursor.execute(sq1)
        ssc = cursor.fetchall()[0][0]
        CHET_IGROKA = pygame.font.Font(None, 40)
        text = CHET_IGROKA.render(f"Лучший рекорд: {ssc}", True, BLACK, 'GRAY')

        screen.blit(text, (10, 50))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

# Иницилизация завершения игры
pygame.init()

# Размеры окна
screen_width = 1280
screen_height = 700

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Концовка")

# Загрузка изображения
background_image2 = pygame.image.load('i (2).webp')

# Основной цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # При нажатии кнопки мыши игра закрывается
        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = False
    # Отображение фона
    screen.blit(background_image2, (0, 0))

    # Обновление экрана
    pygame.display.flip()
pygame.quit()
