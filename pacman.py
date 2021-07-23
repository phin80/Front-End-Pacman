import pygame


# it is better to have an extra variable, than an extremely long line.
img_path = "./player.png"

class Bird:  # represents the bird, not the game
	def __init__(self):
		""" The constructor of the class """
		self.image = pygame.image.load(img_path)

		# the bird's position
		
		self.x = 0
		self.y = 0
		self.speed = 1.5
		self.ckey = None
	pygame.draw.rect()
	def handle_keys(self,k=None):
		""" Handles Keys """
		if k == None:
			key = pygame.key.get_pressed()
		else:
			key = pygame.key.get_pressed()
		if self.ckey == None:
			self.ckey = key
		if self.ckey != None and self.ckey != key and 1 in tuple(key):
			self.ckey = key
		dist = 1 # distance moved in 1 frame, try changing it to 5
		if key[pygame.K_DOWN] or k=="DOWN": # down key
			self.y += dist * self.speed # move down
		elif key[pygame.K_UP] or k=="UP": # up key
			self.y -= dist * self.speed # move up
		elif key[pygame.K_RIGHT] or k=="RIGHT": # right key
			self.x += dist * self.speed # move right
		elif key[pygame.K_LEFT] or k=="LEFT": # left key
			self.x -= dist * self.speed # move left

	def draw(self, surface):
		""" Draw on surface """
		# blit yourself at your current position
		surface.blit(self.image, (self.x, self.y))

	pygame.init()
	screen = pygame.display.set_mode((1000, 1000))
	screen.fill((255,255,255)) # fill the screen with white

	pygame.draw.rect(screen, (0, 0, 0), (215, 135, 50, 50), 10)
	bird = Bird() # create an instance
	clock = pygame.time.Clock()

	running = True
	bckey=None

	while running:
		# handle every event since the last frame.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() # quit the screen
				running = False

	bird.handle_keys()
	bckey = {
		"DOWN":[False if bird.ckey[pygame.K_DOWN] == 0 else True][0],
		"UP":[False if bird.ckey[pygame.K_UP] == 0 else True][0],
		"LEFT":[False if bird.ckey[pygame.K_LEFT] == 0 else True][0],
		"RIGHT":[False if bird.ckey[pygame.K_RIGHT] == 0 else True][0],
	}
	for x in list(bckey.keys()):
		if bckey[x] == True:
			bird.handle_keys(k=x)
			break
	screen.fill((255,255,255)) # fill the screen with white
	bird.draw(screen) # draw the bird to the screen
	pygame.display.update() # update the screen

	clock.tick(60)
