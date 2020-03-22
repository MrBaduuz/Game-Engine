import sys
engine_path = sys.path[0].replace("Examples", "")
sys.path.append(engine_path)
import Engine as eng
import random

eng.createGame("Asteroids", 600 * 4/3, 600, 60)
eng.hide_mouse(True)

pos = eng.Vector(eng.gameSize()[0]/2, eng.gameSize()[1]/2)
vel = eng.Vector(0, 0)
reload_time = 0.2
last_shot = 0
bullet_speed = 10
mouseX, mouseY = eng.mouseCoords()

class Bullet(eng.Particle):
	def __init__(self, x, y, mx, my):
		super().__init__(eng.Vector(x, y))
		self.vel = eng.Vector(mx-x, my-y)
		self.vel.setMag(bullet_speed)
		global explosions
		explosions.append(Exploder(self.pos, self.vel))
		
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
		return self.ptype(pos.x, pos.y, mouseX, mouseY)

class Explosion(eng.Particle):
	def __init__(self, pos, heading):
		super().__init__(pos)
		self.angle = random.randint(0, 359)
		self.a_vel = random.randint(-10, 10)
		self.vel = eng.Vector(random.randint(heading-50, heading+50))
		self.vel.setMag(random.randint(5, 7))
		self.death_speed = 0.038
	def show(self):
		eng.drawRectRot(self.pos.x, self.pos.y, self.lifetime*15, self.lifetime*15, self.angle, (255, 255, 255))
	def update(self, dt):
		self.physics(dt)
		self.angle += self.a_vel
class Exploder(eng.ParticleSystem):
	def __init__(self, pos, vel):
		super().__init__(20, Explosion, 0, 20)
		self.pos = pos
		self.heading = int(vel.heading())
	def particle(self):
		return self.ptype(self.pos, self.heading)

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
	global pos, vel
	acc = eng.Vector(0, 0)
	if keys[eng.keys.K_LEFT] or keys[eng.keys.K_a]:
		acc -= eng.Vector(1, 0)
	if keys[eng.keys.K_RIGHT] or keys[eng.keys.K_d]:
		acc += eng.Vector(1, 0)
	if keys[eng.keys.K_UP] or keys[eng.keys.K_w]:
		acc -= eng.Vector(0, 1)
	if keys[eng.keys.K_DOWN] or keys[eng.keys.K_s]:
		acc += eng.Vector(0, 1)
	acc.setMag(0.25*dt*60)
	vel += acc
	vel.limit(5)
	pos += vel*dt*60
	vel *= 0.99

explosions = []
def update(deltaTime):
	global pos, mouseX, mouseY, vel
	eng.drawBg(50, 50, 50)
	mouseX, mouseY = eng.mouseCoords()
	keys = eng.keyPressed()
	movement(keys, deltaTime)
	bounds()
	shoot(deltaTime)
	for exp in explosions:
		exp.update(deltaTime)
		exp.show()
		if exp.isDead:
			explosions.remove(exp)
	gun.update(deltaTime)
	gun.show()
	eng.drawPolyRot(pos.x, pos.y, [10, -10, -10, -10, 0, 10], eng.atan2(mouseY-pos.y, mouseX-pos.x), (200, 200, 200))
	eng.drawLine(mouseX-5, mouseY, mouseX+5, mouseY, (255, 255, 255, 1))
	eng.drawLine(mouseX, mouseY-5, mouseX, mouseY+5, (255, 255, 255, 1))

eng.update = update
eng.run()