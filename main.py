import os

import pygame

from runner import main as astar
from tools import gen_maze_img as gmi
from tools import get_endless_difficulty as ged

global white,black,red,blue,green,aqua, decision
white,black,red,blue,green,aqua = [(255,255,255),(0,0,0),(255,0,0),(0,0,255),(0,255,0),(0,255,255)]
speed_var=5
dist = 1

def pathfix(inp):
	splitted = inp.split("/")
	return os.path.join(*splitted)

class Bird(pygame.sprite.Sprite):
	def __init__(self):
		self.x = 150
		self.y = 150
		self.speed = speed_var
		self.ckey = None
		super().__init__()
		self.imgdct = {}
		self.images = self.imgdct["RIGHT"], self.imgdct["DOWN"], self.imgdct["UP"], self.imgdct["LEFT"] = [[
				pygame.image.load(pathfix(f"images/{itm}/player_{num}.png.png"))
				for num in range(0, 4)
		] for itm in ["RIGHT", "DOWN", "UP", "LEFT"]]
		self.index = 0
		self.image = pygame.image.load(pathfix("images/RIGHT/player_0.png.png"))
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
		if self.ckey == key:
			return 0

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
screen.fill(black) # fill the screen with white
bird = Bird() # create an instance
clock = pygame.time.Clock()
playergroup = pygame.sprite.Group(bird)
yes = True

def border(cs,sc=screen,pxw=4,clr=(255,255,255)):
	pygame.draw.rect(sc,clr,cs,pxw)

def rText(fnt,txt,clr=(255,255,255),rtrn=False,sc=screen,crds=False):
	if not rtrn and crds != False:
		sc.blit(fnt.render(txt,True,clr),crds)
	if rtrn: return fnt.render(txt,True,clr)

def d_rect(crds,clr,sc=screen,brdr=True):
	pygame.draw.rect(sc,clr,crds)
	if brdr: border(crds)

def dificulty_setting():
	image1 = pygame.image.load(pathfix("images/MUW4Dh6-pacman-background.jpg"))
	screen.blit(image1, (0, 0))

	font1 = pygame.font.Font(None, 150)
	font2 = pygame.font.Font(None, 300)

	rText(font1,"ultimate",crds=(275,50))
	rText(font1,"PAC MAN",crds=(250,160))
	rText(font1,"choose a dificulty",crds=(50,275))

	for x in range(3):
		d_rect(((300 * (x + 1)) - 200, 500, 200, 200), [green,blue,red][x])
	d_rect(crds=(250,750,500,200),clr=aqua)
	rText(font1, "endless", crds=(300, 800),clr=(0,0,1))
	for itr in range(3):
		screen.blit(font2.render(str(itr + 1), True, tuple([[1 if x == itr else 0][0] for x in range(1, 4)][0:2][::-1] + [0])), (300 * (itr + 2) - 460, 500))
	pygame.display.update()

running = True


bckey = None
decision = 1
endless = False
num_wins=1
def endless_create(w):
	print(w)
	grd = astar(w=w, d=.95)
	bird_images_expanded = sum(bird.images, [])
	bafter = bird_images_expanded
	for img in range(len(bird_images_expanded)):
		bafter[img] = pygame.transform.scale(bird_images_expanded[img], (round(1000 / w / 1.5), round(1000 / w / 1.5)))
	bird.imgdct["RIGHT"], bird.imgdct["DOWN"], bird.imgdct["UP"], bird.imgdct["LEFT"] = [bafter[0:4], bafter[4:8],
																						 bafter[8:12], bafter[12:16]]
	bird.x = (1000 / w)
	bird.y = (1000 / w)
	Bird.width, bird.height = [round(1000 / w / 1.5), round(1000 / w / 1.5)]
	if grd != None:
		print(gmi(w=10, h=10, grid=grd, brdr=False))
def s_eq2_clr(crds,sc=screen,clr=white):
	return [True if pygame.Surface.get_at(sc, crds) == clr else False][0]
frames=0
w = 1
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			running = False

	if decision == 1:
		if endless == True:
			endless_nums = ged(num_wins, 3)
			w = round(endless_nums * 20)
			endless_create(w=w)
			endless = True
			decision = 2
		dificulty_setting()
		mouse_position = (0, 0)
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_position = pygame.mouse.get_pos()
			sget = pygame.Surface.get_at(screen, mouse_position)
			if sget in [green, black]:
				w=8
				grd = astar(w=w, d=1)
				decision = 2
				bird_images_expanded = sum(bird.images,[])
				bafter = bird_images_expanded
				for img in range(len(bird_images_expanded)):
					bafter[img] = pygame.transform.scale(bird_images_expanded[img],(round(1000/w/1.5), round(1000/w/1.5)))
				bird.imgdct["RIGHT"], bird.imgdct["DOWN"], bird.imgdct["UP"], bird.imgdct["LEFT"] = [bafter[0:4],bafter[4:8],bafter[8:12],bafter[12:16]]
				bird.x = (1000/w)
				bird.y = (1000/w)
				Bird.width, bird.height = [round(1000/w/1.5), round(1000/w/1.5)]
				if grd != None:
					print(gmi(grid=grd,brdr=False))
			if sget in [blue, (0,1,0)]:
				w = 14
				grd = astar(w=w, d=1)
				decision = 2
				bird_images_expanded = sum(bird.images, [])
				bafter = bird_images_expanded
				for img in range(len(bird_images_expanded)):
					bafter[img] = pygame.transform.scale(bird_images_expanded[img], (round(1000/w/1.5), round(1000/w/1.5)))
				bird.imgdct["RIGHT"], bird.imgdct["DOWN"], bird.imgdct["UP"], bird.imgdct["LEFT"] = [bafter[0:4],bafter[4:8],bafter[8:12],bafter[12:16]]
				bird.x = (1000 / w)
				bird.y = (1000 / w)
				Bird.width, bird.height = [round(1000/w/1.5),round(1000/w/1.5)]
				if grd != None:
					print(gmi(grid=grd,brdr=True))
			if sget in [red, (1,0,0)]:
				w=18
				grd = astar(w=w, d=.95)
				decision = 2
				bird_images_expanded = sum(bird.images, [])
				bafter = bird_images_expanded
				for img in range(len(bird_images_expanded)):
					bafter[img] = pygame.transform.scale(bird_images_expanded[img], (round(1000/w/1.5),round(1000/w/1.5)))
				bird.imgdct["RIGHT"], bird.imgdct["DOWN"], bird.imgdct["UP"], bird.imgdct["LEFT"] = [bafter[0:4],bafter[4:8],bafter[8:12],bafter[12:16]]
				bird.x = (1000/w)
				bird.y = (1000/w)
				Bird.width, bird.height = [round(1000/w/1.5),round(1000/w/1.5)]
				if grd != None:
					print(gmi(w=10,h=10,grid=grd,brdr=False))
			if sget in [aqua,(0,0,1)]:
				endless_nums=ged(num_wins,3)
				w=round(endless_nums*20)
				endless_create(w=w)
				endless= True
				decision = 2
	if decision == 2:
		screen.fill(black)
		image2 = pygame.image.load("lvl.png")
		screen.blit(image2, (-167, -157))
		pygame.draw.circle(screen, (0, 0, 0), ((437.5, 500.0)), 2)
		squares=[]
		dots=[]
		ytimes=1
		sqr_y_crds =1
		sqr_x_crds =1
		for itr in range(w):
			sqr_y_crds = round(1000/(w*2)*ytimes)
			ytimes = ytimes+1
			xtimes = 1
			for itr2 in range(w):
				sqr_x_crds = round(1000 / (w * 2) * xtimes)
				xtimes = xtimes + 1
				squares.append((sqr_x_crds,sqr_y_crds))
		iterate_dots=0
		pygame.display.update()

		for itr in range (w**2):
			#if pygame.Surface.get_at(screen,squares[iterate_dots]) == (0,0,0):
			#	print("pog")
			#	pygame.draw.circle(screen, (255, 0, 255), (squares[iterate_dots]), 10)
			iterate_dots= iterate_dots+1
		print(squares)
		print(squares.count(any))
		#print(iterate_dots)
		tgauge = speed_var
		bx, by, bh, bw = list(map(round, [bird.x, bird.y, bird.height, bird.width]))
		if s_eq2_clr((bx - 1, by)): bird.x += tgauge
		if s_eq2_clr((bx + bw - 1, by - 1)): bird.y += tgauge
		if s_eq2_clr((bx + bw + 1, by + bh)): bird.x -= tgauge
		if s_eq2_clr((bx, by + bh + 1)): bird.y -= tgauge
		if pygame.Surface.get_at(screen,(bx,by-1)) == (57,255,20):
			dist=0
			font3= pygame.font.Font(None, 150)
			rText(font3, "YOU WIN", crds=(275, 50),clr=(0,0,0))
			frames +=1
			if frames == 50:
				bird.x,bird.y = 0,0
				dist = 1
				frames=0
				bird.ckey = None
				num_wins= num_wins+1
				decision = 1
				print(num_wins)

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
		clock.tick(120)
		pygame.display.update()
