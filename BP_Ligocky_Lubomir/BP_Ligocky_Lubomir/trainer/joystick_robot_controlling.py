import pygame

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

robotPosture.goToPosture("StandInit", 0.5f);

x  = 0.2
y  = 0.2
# pi/2 anti-clockwise (90 degrees)
theta = 1.5709
motion.moveTo(x, y, theta)

if joysticks:
    while True:
        choice = input("> ")

        if choice == 'b' :
            input("yay")
            break
pygame.joystick.quit()