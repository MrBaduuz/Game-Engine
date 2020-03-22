import sys
engine_path = sys.path[0].replace("Examples", "")
sys.path.append(engine_path)
import Engine as eng
import math

eng.createGame("Asteroids", 600 * 4/3, 600, 60)
eng.hide_mouse(True)

pos = eng.Vector(eng.gameSize()[0]/2, eng.gameSize()[1]/2)
reload_time = 0.2
last_shot = 0
bullet_speed = 10

class Bullet(eng.Particle):
	def __init__(self, x, y, mx, my):
		super().__init__(eng.Vector(x, y))
		self.vel = eng.Vector(mx-x, my-y)
		print(self.vel)
		self.vel.setMag(bullet_speed)
		
	def show(self):
		eng.drawEllipse(self.pos.x, self.pos.y, 7, 7, (170, 170, 170))
	def update(self, dt):
		self.physics(dt)
	def isDead(self):
		return self.pos.x > eng.gameSize()[0]+20 or self.pos.y > eng.gameSize()[1]+20 or self.pos.x < -20 or self.pos.y < -20
class Gun(eng.ParticleSystem):
	def __init__(self):
		super().__init__(0, Bullet, 0, 0)
	def shoot(self):
		self.ps.append(self.particle())
	def add(self):
		pass
	def particle(self):
		return self.ptype(pos.x, pos.y, eng.mouseCoords()[0], eng.mouseCoords()[1])

gun = Gun()

def bounds():
	global pos
	if pos.x > eng.gameSize()[0] + 20:
		pos.x = -20
	elif pos.x < -20:
		pos.x = eng.gameSize()[0] + 20
	if pos.y > eng.gameSize()[1] + 20:
		pos.y = -20
	elif pos.y < -20:
		pos.y = eng.gameSize()[1] + 20
def shoot(dt):
	global last_shot, reload_time
	if last_shot <= 0 and eng.mousePressed():
		gun.shoot()
		last_shot = reload_time
	last_shot -= dt

def movement(keys, dt):
	global pos
	vel = eng.Vector(0, 0)
	if keys[eng.keys.K_LEFT] or keys[eng.keys.K_a]:
		vel -= eng.Vector(1, 0)
	if keys[eng.keys.K_RIGHT] or keys[eng.keys.K_d]:
		vel += eng.Vector(1, 0)
	if keys[eng.keys.K_UP] or keys[eng.keys.K_w]:
		vel -= eng.Vector(0, 1)
	if keys[eng.keys.K_DOWN] or keys[eng.keys.K_s]:
		vel += eng.Vector(0, 1)
	vel.setMag(5*dt*60)
	pos += vel

def update(deltaTime):
	global pos
	eng.drawBg(50, 50, 50)
	mouseX, mouseY = eng.mouseCoords()
	keys = eng.keyPressed()
	movement(keys, deltaTime)
	bounds()
	shoot(deltaTime)
	gun.update(deltaTime)
	gun.show()
	eng.drawPolyRot(pos.x, pos.y, [10, -10, -10, -10, 0, 10], eng.atan2(mouseY-pos.y, mouseX-pos.x), (200, 200, 200))
	eng.drawLine(mouseX-5, mouseY, mouseX+5, mouseY, (255, 255, 255, 1))
	eng.drawLine(mouseX, mouseY-5, mouseX, mouseY+5, (255, 255, 255, 1))

eng.update = update
eng.run()