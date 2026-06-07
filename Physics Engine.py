import pygame
import matplotlib.pyplot as plt

plt.ion()
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1)

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Particle class
class Particle:
    def __init__(self, x, y, vx, vy, e, m, radius=10, color=(255,255,255), ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.e = e
        self.mass = m
        self.history_vx = []
        self.history_vy = []
        self.history_time = []
        

    def update(self, time):
        self.x += self.vx
        self.y += self.vy
        self.history_vx.append(self.vx)
        self.history_vy.append(self.vy)
        self.history_time.append(time)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def check_walls(self):
        #left wall
        if self.x-self.radius <= 0:
            self.vx = -self.vx * self.e
            self.x = self.radius
        #right wall
        if self.x+self.radius >= WIDTH:
            self.vx = -self.vx * self.e
            self.x = WIDTH - self.radius
        #top wall
        if self.y - self.radius <= 0:
            self.vy = -self.vy *self.e
            self.y = self.radius
        #bottom wall
        if self.y + self.radius >= HEIGHT:
            self.vy = -self.vy * self.e
            self.y = HEIGHT - self.radius

def collision(p1, p2):
    distance_between = ((p2.y-p1.y)**2 + (p2.x-p1.x)**2)**0.5
    if distance_between <= p1.radius+p2.radius:
        print("Colliding")
        



def plot_data(particle):
    # calculate KE
    ke_x = [0.5*particle.mass * vx**2 for vx in particle.history_vx]
    ke_y = [0.5 * particle.mass * vy**2 for vy in particle.history_vy]
    ke_total = [kx + ky for kx, ky in zip(ke_x, ke_y)]
    # clear axes
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    ax5.cla()
    # plot
    ax1.plot(particle.history_time, particle.history_vx)
    ax2.plot(particle.history_time, particle.history_vy)
    ax3.plot(particle.history_time, ke_x)
    ax4.plot(particle.history_time, ke_y)
    ax5.plot(particle.history_time, ke_total)
    #Labels
    ax1.set_ylabel("vx")
    ax2.set_ylabel("vy")
    ax3.set_ylabel("KE_x")
    ax4.set_ylabel("KE_y")
    ax5.set_ylabel("KE_total")
    ax5.set_xlabel("time (ms)")
    # pause        
    plt.pause(0.001)    
# Setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
frame = 0

# Two particles
p1 = Particle(200, 300, 2, 1, 1, 10, color=(255, 100, 100))
p2 = Particle(600, 300, -2, 1, 1, 10, color=(100, 100, 255))


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    current_time = pygame.time.get_ticks()
    p1.update(current_time)
    p1.check_walls()
    p2.update(current_time)
    p2.check_walls()
    collision(p1, p2)
    p1.draw(screen)
    p2.draw(screen)
    if frame%30 == 0:
        plot_data(p1)
        #plot_data(p2)
        pass
    frame += 1    
    

    

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()