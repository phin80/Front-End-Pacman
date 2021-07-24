import pygame

from runner import main as astar

#grd = astar(w=20,d=15)
#if grd != None:
#	print(grd)

# it is better to have an extra variable, than an extremely long line.
img_path = "./player.png"


class Bird(pygame.sprite.Sprite):
	def __init__(self):
		self.x = 50
		self.y = 50
		self.speed = 1.5
		self.ckey = None
		super().__init__()
		self.imgdct = {}
		self.images = self.imgdct["RIGHT"], self.imgdct["DOWN"], self.imgdct["UP"], self.imgdct["LEFT"] = [[
				pygame.image.load(f"images/{itm}/player_{num}.png")
				for num in range(0, 4)
		] for itm in ["RIGHT", "DOWN", "UP", "LEFT"]]
		self.index = 0
		self.image = pygame.image.load("images/RIGHT/player_0.png")
		self.width, self.height = [self.image.get_width(), self.image.get_height()]
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
screen = pygame.display.set_mode((1000, 1000))
screen.fill((0,0,0)) # fill the screen with white
bird = Bird() # create an instance
clock = pygame.time.Clock()
#pygame.draw.r
playergroup = pygame.sprite.Group(bird)
yes = True


def dificulty_setting():
	image1 = pygame.image.load("images/MUW4Dh6-pacman-background.jpg")
	screen.blit(image1, (0, 0))
	font1 = pygame.font.Font(None, 150)
	font2 = pygame.font.Font(None, 300)
	caption6 = font1.render("ultimate", True, (255, 255, 255))
	screen.blit(caption6, (275, 50))
	caption7 = font1.render("PAC MAN", True, (255, 255, 255))
	screen.blit(caption7, (250, 160))
	caption1 = font1.render("choose a dificulty", True, (255, 255, 255))
	screen.blit(caption1, (50, 275))

	pygame.draw.rect(screen, (0, 255, 0), (100, 500, 200, 200))
	pygame.draw.rect(screen, (255, 255, 255), (100, 500, 200, 200), 4)
	pygame.draw.rect(screen, (0, 0, 255), (400, 500, 200, 200))
	pygame.draw.rect(screen, (255, 255, 255), (400, 500, 200, 200), 4)
	pygame.draw.rect(screen, (255, 0, 0), (700, 500, 200, 200))
	pygame.draw.rect(screen, (255, 255, 255), (700, 500, 200, 200), 4)
	pygame.draw.rect(screen, (0, 255, 255), (250, 750, 500, 200))
	pygame.draw.rect(screen, (255, 255, 255), (250, 750, 500, 200), 4)
	caption2 = font2.render("1", True, (0, 0, 0))
	screen.blit(caption2, (140, 500))
	caption3 = font2.render("2", True, (0, 1, 0))
	screen.blit(caption3, (440, 500))
	caption4 = font2.render("3", True, (1, 0, 0))
	screen.blit(caption4, (740, 500))
	caption5 = font1.render("campaign", True, (0, 0, 1))
	screen.blit(caption5, (250, 800))
	pygame.display.update()


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			yes = False
	dificulty_setting()
	mouse_position = (0,0)
	if event.type == pygame.MOUSEBUTTONDOWN:
		mouse_position= pygame.mouse.get_pos()
		if pygame.Surface.get_at(screen,mouse_position) == (0,255,0) or pygame.Surface.get_at(screen, mouse_position) == (0,0,0):

running = False
bckey = None

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			running = False
	screen.fill((0, 0, 0))  # fill the screen with white
	pygame.draw.rect(screen, (255,255,255), (5,5,990,990), 20)
	if pygame.Surface.get_at(screen, (round(bird.x-1),round(bird.y)))==(255,255,255):
		bird.x = bird.x+3
	if pygame.Surface.get_at(screen, (round(bird.x+bird.width-1),round(bird.y-1)))==(255,255,255):
		bird.y = bird.y+3
	if pygame.Surface.get_at(screen, (round(bird.x+bird.width+1),round(bird.y+bird.height)))==(255,255,255):
		bird.x = bird.x-3
	if pygame.Surface.get_at(screen, (round(bird.x),round(bird.y+bird.height+1)))==(255,255,255):
		bird.y = bird.y-3
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
	bird.draw(screen, direction=kk)
	pygame.display.update()
	clock.tick(40)