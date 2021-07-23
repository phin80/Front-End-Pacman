import pygame


# it is better to have an extra variable, than an extremely long line.
img_path = "./player.png"


class Bird(pygame.sprite.Sprite):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.speed = 3
		self.ckey = None
		super().__init__()
		self.imgdct = {}
		self.images = self.imgdct["RIGHT"], self.imgdct["DOWN"], self.imgdct["UP"], self.imgdct["LEFT"] = [[
				pygame.image.load(f"images/{itm}/player_{num}.png")
				for num in range(0, 4)
		] for itm in ["RIGHT", "DOWN", "UP", "LEFT"]]
		self.index = 0
		self.image = pygame.image.load("images/RIGHT/player_0.png")
		self.slowdown = 6
		self.actualslow = 0

	def handle_keys(self, k=None):
		if k == None:
			key = pygame.key.get_pressed()
		else:
			key = pygame.key.get_pressed()
		if self.ckey == None:
			self.ckey = key
		if self.ckey != None and self.ckey != key and 1 in tuple(key):
			self.ckey = key
		dist = 1
		if key[pygame.K_DOWN] or k == "DOWN":
			self.y += dist * self.speed
		elif key[pygame.K_UP] or k == "UP":
			self.y -= dist * self.speed
		elif key[pygame.K_RIGHT] or k == "RIGHT":
			self.x += dist * self.speed
		elif key[pygame.K_LEFT] or k == "LEFT":
			self.x -= dist * self.speed

	def draw(self, surface, direction="RIGHT"):
		if self.actualslow == self.slowdown:
			self.actualslow = 0
			self.index += 1
			cont = True
		else:
			self.actualslow += 1
			cont = False
		if not cont:
			surface.blit(self.image, (self.x, self.y))
			return 0
		if self.index >= len(self.imgdct[direction]):
			self.index = 0
		self.image = self.imgdct[direction][self.index]
		self.index += 1
		surface.blit(self.image, (self.x, self.y))


pygame.init()
screen = pygame.display.set_mode((640, 400))

bird = Bird()
clock = pygame.time.Clock()
playergroup = pygame.sprite.Group(bird)
running = True
bckey = None

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			running = False

	bird.handle_keys()
	bckey = {
		"DOWN": [False if bird.ckey[pygame.K_DOWN] == 0 else True][0],
		"UP": [False if bird.ckey[pygame.K_UP] == 0 else True][0],
		"LEFT": [False if bird.ckey[pygame.K_LEFT] == 0 else True][0],
		"RIGHT": [False if bird.ckey[pygame.K_RIGHT] == 0 else True][0],
	}
	kk = "RIGHT"
	for x in list(bckey.keys()):
		if bckey[x] == True:
			bird.handle_keys(k=x)
			kk = x
			break
	screen.fill((0, 0, 0))
	bird.draw(screen, direction=kk)
	pygame.display.update()
	clock.tick(40)
