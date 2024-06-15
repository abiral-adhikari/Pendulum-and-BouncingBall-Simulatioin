import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy as np

# Set up the display
display = (800, 600)


# Ball class
class Ball:
    def __init__(self, x, y, vx, vy, radius, color, elasticity, speed_factor):
        self.x = x
        self.y = y
        self.vx = vx * speed_factor
        self.vy = vy * speed_factor
        self.radius = radius
        self.color = color
        self.elasticity = elasticity

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Check for collision with walls
        if self.x - self.radius < 0 or self.x + self.radius > display[0]:
            self.vx = -self.vx * self.elasticity
            self.x = max(self.radius, min(self.x, display[0] - self.radius))
        if self.y - self.radius < 0 or self.y + self.radius > display[1]:
            self.vy = -self.vy * self.elasticity
            self.y = max(self.radius, min(self.y, display[1] - self.radius))

    def draw(self):
        glColor3fv(self.color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(self.x, self.y)
        for i in range(361):
            angle = np.radians(i)
            glVertex2f(self.x + np.cos(angle) * self.radius, self.y + np.sin(angle) * self.radius)
        glEnd()

def check_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = np.hypot(dx, dy)
    if distance < ball1.radius + ball2.radius:
        angle = np.arctan2(dy, dx)
        total_mass = ball1.radius ** 2 + ball2.radius ** 2

        # New velocities based on 1D collision equations
        new_vx1 = ball1.vx * (ball1.radius ** 2 - ball2.radius ** 2) / total_mass + \
                  ball2.vx * (2 * ball2.radius ** 2) / total_mass
        new_vx2 = ball1.vx * (2 * ball1.radius ** 2) / total_mass + \
                  ball2.vx * (ball2.radius ** 2 - ball1.radius ** 2) / total_mass
        new_vy1 = ball1.vy * (ball1.radius ** 2 - ball2.radius ** 2) / total_mass + \
                  ball2.vy * (2 * ball2.radius ** 2) / total_mass
        new_vy2 = ball1.vy * (2 * ball1.radius ** 2) / total_mass + \
                  ball2.vy * (ball2.radius ** 2 - ball1.radius ** 2) / total_mass

        ball1.vx, ball1.vy = new_vx1 * ball1.elasticity, new_vy1 * ball1.elasticity
        ball2.vx, ball2.vy = new_vx2 * ball2.elasticity, new_vy2 * ball2.elasticity

        # Move balls so they are not overlapping
        overlap = 0.5 * (ball1.radius + ball2.radius - distance + 1)
        ball1.x -= overlap * np.cos(angle)
        ball1.y -= overlap * np.sin(angle)
        ball2.x += overlap * np.cos(angle)
        ball2.y += overlap * np.sin(angle)

def random_balls(num_balls, elasticity, speed_factor):
    balls = []
    for _ in range(num_balls):
        radius = random.randint(10, 20)
        x = random.randint(radius, display[0] - radius)
        y = random.randint(radius, display[1] - radius)
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        color = (random.random(), random.random(), random.random())
        ball = Ball(x, y, vx, vy, radius, color, elasticity, speed_factor)
        balls.append(ball)
    return balls

def manual_balls(num_balls, elasticity, speed_factor):
    balls = []
    launch_locations = [
        'top_left', 'top_right', 'bottom_left', 'bottom_right', 'left', 'right', 'top', 'bottom'
    ]
    
    for i in range(num_balls):
        radius = int(input(f"Enter radius for ball {i+1}: "))
        launch_location = input(f"Enter launch location for ball {i+1} (top_left, top_right, bottom_left, bottom_right, left, right, top, bottom): ").strip().lower()
        
        if launch_location not in launch_locations:
            print("Invalid launch location. Please choose from the available options.")
            return []
        
        if launch_location == 'top_left':
            x, y = 0, display[1]
            vx = random.uniform(0.5, 2)
            vy = random.uniform(-2, -0.5)
        elif launch_location == 'top_right':
            x, y = display[0], display[1]
            vx = random.uniform(-2, -0.5)
            vy = random.uniform(-2, -0.5)
        elif launch_location == 'bottom_left':
            x, y = 0, 0
            vx = random.uniform(0.5, 2)
            vy = random.uniform(0.5, 2)
        elif launch_location == 'bottom_right':
            x, y = display[0], 0
            vx = random.uniform(-2, -0.5)
            vy = random.uniform(0.5, 2)
        elif launch_location == 'left':
            x, y = 0, random.randint(0, display[1])
            vx = random.uniform(0.5, 2)
            vy = random.uniform(-2, 2)
        elif launch_location == 'right':
            x, y = display[0], random.randint(0, display[1])
            vx = random.uniform(-2, -0.5)
            vy = random.uniform(-2, 2)
        elif launch_location == 'top':
            x, y = random.randint(0, display[0]), display[1]
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, -0.5)
        elif launch_location == 'bottom':
            x, y = random.randint(0, display[0]), 0
            vx = random.uniform(-2, 2)
            vy=random.uniform(0.5,2)
        color = (random.random(), random.random(), random.random())
        ball = Ball(x, y, vx, vy, radius, color, elasticity, speed_factor)
        balls.append(ball)
    return balls


def ballbouncingsimulation():
        # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()


    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    gluOrtho2D(0, display[0], 0, display[1])
    while True:
        mode = input("Enter\n1 for manual collision\n2 for random collision\n3 to exit:\n").strip().lower()
        if mode == '3':
            break
        if mode not in ('1', '2'):
            print("Invalid input. Please try again.")
            continue

        num_balls = int(input("Enter the number of balls: "))
        elasticity = float(input("Enter the elasticity (0 to 1): "))
        speed_factor = float(input("Enter the speed factor (1 to 10): "))

        if mode == '1':
            balls = manual_balls(num_balls, elasticity, speed_factor)
        elif mode == '2':
            balls = random_balls(num_balls, elasticity, speed_factor)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            for i, ball in enumerate(balls):
                ball.move()
                for j in range(i + 1, len(balls)):
                    check_collision(ball, balls[j])
                ball.draw()

            pygame.display.flip()
            clock.tick(60)
            
if __name__ == "__main__":
    ballbouncingsimulation()
