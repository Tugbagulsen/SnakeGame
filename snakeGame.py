import pygame, sys, random

# Ekran Boyutları
screen_width = 600
screen_height = 600

# Izgara ayarları
gridsize = 20
grid_width = screen_width // gridsize
grid_height = screen_height // gridsize

# Renkler
light_green = (0, 170, 140)
dark_green = (0, 140, 120)
food_color = (250, 200, 0)
snake_color = (34, 34, 34)

# Hareket yönleri
up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)

class SNAKE:
    def __init__(self):
        self.positions = [((screen_width / 2), (screen_height / 2))]  # Yılanın başlangıç konumu
        self.length = 1  # Yılanın başlangıç uzunluğu
        self.direction = random.choice([up, down, left, right])  # Yılanın başlangıç yönu
        self.color = snake_color  # Yılanın rengi
        self.score = 0  # Oyuncunun puanı
    def draw(self, surface):
        # Yılanı çizmek için pygame kutusunu kullan
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)
    def move(self):
        # Yılanın hareketini yönet
        current = self.positions[0]  # Yılanın şu anki konumu
        x, y = self.direction  # Yön vektörünü al
        new = ((current[0] + (x * gridsize)), (current[1] + (y * gridsize)))  # Yeni konumu hesapla

        # Yılanın ekran sınırlarını aşmadığı ve kendisiyle çarpışmadığından emin ol
        if new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not new in self.positions[2:]:
            self.positions.insert(0, new)  # Yeni konumu yılanın başına ekle
            if len(self.positions) > self.length:
                self.positions.pop()  # Yılanın sonundaki konumu sil
        else:
            self.reset()  # Yılan ekran sınırlarını veya kendisiyle çarpışmayı aşarsa sıfırla
    def reset(self):
        # Yılanı başlangıç pozisyonuna ve uzunluğuna geri döndür
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0  # Puanı sıfırla
    def handle_keys(self):
        # Klavye olaylarını işle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
    def turn(self, direction):
        # Yılanın dönüşünü kontrol et
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return  # Yılan zaten tam tersine dönüyorsa hiçbir şey yapma
        else:
            self.direction = direction  # Yönü değiştir

class FOOD:
    def __init__(self):
        self.position = (0, 0)  # Yem başlangıç pozisyonu
        self.color = food_color  # Yem rengi
        self.random_position()  # Yemi rastgele bir konuma yerleştir
    def random_position(self):
        # Yemi rastgele bir konuma yerleştir
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)
    def draw(self, surface):
        # Yemi çiz
        rect = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)

# Izgarayı çizmek için fonksiyon
def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y) % 2 == 0:
                light = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, light_green, light)
            else:
                dark = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, dark_green, dark)
# Ana fonksiyon
def main():
    # Pygame'i başlat
    pygame.init()
    # Ekranı ayarla
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()  # Oyun hızını kontrol etmek için bir saat oluştur
    font = pygame.font.SysFont("arial", 20)  # Oyun skorunu göstermek için bir yazı tipi oluştur
    # Çizim yüzeyi oluştur
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = SNAKE()  # Yılan nesnesi oluştur
    food = FOOD()  # Yem nesnesi oluştur

    # Ana oyun döngüsü
    while True:
        clock.tick(5)  # Oyun hızını ayarla (saniyede 20 kare)
        snake.handle_keys()  # Klavye girişlerini işle
        snake.move()  # Yılanı hareket ettir
        if snake.positions[0] == food.position:
            snake.length += 1  # Yılan yemi yediyse uzunluğunu arttır
            snake.score += 1  # Oyuncunun puanını arttır
            food.random_position()  # Yemi rastgele bir konuma yerleştir
        # Izgarayı çiz
        drawGrid(surface)
        snake.draw(surface)
        food.draw(surface)
        score_text = font.render("Score: {0}".format(snake.score), True, (0, 0, 0))  # Puanı ekrana yazdır
        screen.blit(score_text, (10, 10))  # Puan yazısını ekrana yerleştir
        # Yüzeyi ekran yüzeyine kopyala
        screen.blit(surface, (0, 0))
        # Ekranı güncelle
        pygame.display.update()

main()
