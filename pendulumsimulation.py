import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Constants
width, height = 800, 600

# Color dictionary mapping color names to RGB values
COLORS = {
    "white": (1, 1, 1),
    "red": (1, 0, 0),
    "green": (0, 1, 0),
    "blue": (0, 0, 1),
    "yellow": (1, 1, 0),
    "cyan": (0, 1, 1),
    "magenta": (1, 0, 1),
    "orange": (1, 0.5, 0),
    # Add more colors if needed
}

# Pendulum class to handle individual pendulum properties and motion
class Pendulum:
    def __init__(self, length, mass, theta0, gravity, blob_color):
        self.length = length
        self.mass = mass
        self.theta0 = theta0
        self.gravity = gravity
        self.omega = np.sqrt(self.gravity / self.length)
        self.time = 0
        self.angle = theta0
        self.blob_color = blob_color
        self.time_data = []
        self.angle_data = []

    def update(self, dt):
        self.time += dt
        self.angle = self.theta0 * np.cos(self.omega * self.time)
        self.time_data.append(self.time)
        self.angle_data.append(self.angle)

    def get_position(self):
        x = self.length * np.sin(self.angle)
        y = -self.length * np.cos(self.angle)
        return x, y

def draw_pendulum(pendulum):
    x, y = pendulum.get_position()
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(0, 0)
    glVertex2f(x, y)
    glEnd()
    
    glColor3f(*pendulum.blob_color)  # Use the pendulum's color
    glBegin(GL_POLYGON)
    for i in range(20):
        angle = 2 * np.pi * i / 20
        glVertex2f(x + 0.1 * pendulum.mass * np.cos(angle), y + 0.1 * pendulum.mass * np.sin(angle))
    glEnd()

def draw_graph(pendulums):
    for pendulum in pendulums:
        glColor3f(*pendulum.blob_color)
        glBegin(GL_LINE_STRIP)
        for t, angle in zip(pendulum.time_data, pendulum.angle_data):
            glVertex2f(t, angle)
        glEnd()

def choose_color():
    print("Choose a color for the pendulum blob:")
    for color in COLORS:
        print(f"- {color}")
    while True:
        choice = input("Enter the color name: ").lower()
        if choice in COLORS:
            return COLORS[choice]
        else:
            print("Invalid color name. Please choose from the available options.")

def pendulumsimulation():
    pygame.init()
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Pendulum Simulation')

    # Set up the orthographic projection for the simulation part
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-5, 5, -5, 5)
    glMatrixMode(GL_MODELVIEW)

    num_pendulums = int(input("Enter number of pendulums: "))
    pendulums = []

    for i in range(num_pendulums):
        length = float(input(f"Enter length of pendulum {i+1} (in meters): "))
        mass = float(input(f"Enter mass of pendulum {i+1} (in kilograms): "))
        theta0 = np.deg2rad(float(input(f"Enter initial angle (in degrees) of pendulum {i+1}: ")))
        gravity = float(input(f"Enter gravity value for pendulum {i+1} (in m/s^2): "))
        blob_color = choose_color()
        pendulums.append(Pendulum(length, mass, theta0, gravity, blob_color))

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the pendulums
        # glViewport(x, y, width, height)
        glViewport(0, height // 2, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-5, 5, -5, 5)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        dt = clock.tick(60) / 1000.0

        for pendulum in pendulums:
            pendulum.update(dt)
            draw_pendulum(pendulum)

        # Draw the graph
        glViewport(0, 0, width, height // 2)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 20, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        draw_graph(pendulums)

        pygame.display.flip()

if __name__ == "__main__":
    pendulumsimulation()
