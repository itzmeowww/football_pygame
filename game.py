import pygame
import sys
import tkinter as tk
import paho.mqtt.client as mqtt
import math

host = "broker.mqttdashboard.com"
port = 8000
receive_l = "topic/l"
receive_r = "topic/r"
send = "topic/1"

size = width, height = 300, 100
#class of setting window
# Setting menu
# For setting the name of each team and the goal
class SettingWidget:
    def btn(self):
        self.name1 = self.entry1.get()
        self.name2 = self.entry2.get()
        self.goal = int(self.entrygoal.get())
        #print(self.name1, self.name2)
        self.widget.destroy()

    def __init__(self, width, height):
        self.name1 = "MCU"
        self.name2 = "LIV"
        self.goal = 5
        self.widget = tk.Tk()
        #self.widget.geometry(str(width)+"x"+str(height))
        self.widget.title('Setting')
        self.create_widget()

    def create_widget(self):
        tk.Label(self.widget, text='First team\'s name').grid(row=0)
        tk.Label(self.widget, text='Second team\'s name').grid(row=1)
        tk.Label(self.widget, text='Goal').grid(row=2)
        self.v1 = tk.StringVar()
        self.entry1 = tk.Entry(self.widget, textvariable=self.v1)
        self.entry1.grid(row=0, column=1)
        self.v1.set(self.name1)

        self.v2 = tk.StringVar()
        self.entry2 = tk.Entry(self.widget, textvariable=self.v2)
        self.entry2.grid(row=1, column=1)
        self.v2.set(self.name2)

        self.vg = tk.StringVar()
        self.entrygoal = tk.Entry(self.widget, textvariable=self.vg)
        self.entrygoal.grid(row=2, column=1)
        self.vg.set(str(self.goal))

        self.enter_btn = tk.Button(self.widget, text='Enter the game', width=25, command=self.btn)
        self.enter_btn.grid(row=3,columnspan = 2)
        self.widget.mainloop()

    def getname(self):
        return (self.name1, self.name2, self.goal)


def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe([(receive_l,0),(receive_r,1)])
    print("Subscribed")


def on_message(client, userdata, msg):
    mes = msg.payload.decode("utf-8", "strict")
    if msg.topic == receive_l:
        game.val_l = int(mes)
        game.have_l = True
    if msg.topic == receive_r:
        game.val_r = int(mes)
        game.have_r = True


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)
client.loop_start()



score1 = 0
score2 = 0

done = False

num = 0


class Text:
    def __init__(self, screen, size, color, type,):
        self.size = size
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
        self.screen = screen
        self.type = type
        self.color = color

    def update(self, text, x, y):
        self.text = self.font.render(str(text), True, self.color)
        self.rect = self.text.get_rect()
        setattr(self.rect, self.type, (x, y))
        #self.rect.midleft = (30,30)
        self.screen.blit(self.text, self.rect)


class Ball:
    def __init__(self, x, y, r, goal_width, canvas_width):
        self.speed = 5
        self.canvas_width = canvas_width
        self.goal_width = goal_width
        self.x = x
        self.y = y
        self.r = r
        self.Img = pygame.image.load('ball.png')
        self.Img = pygame.transform.scale(self.Img, (2*r, 2*r))
        self.old_Img = self.Img
        self.gl = goal_width
        self.gr = canvas_width-goal_width
        self.score = 0
        self.angle = 0
        self.all_angle = 0
        self.dir = 0

    def update(self, screen):
        #print("UP ", self.all_angle, self.angle)
        
        if self.all_angle == self.angle:
            self.angle = self.angle
            self.dir = 0 
        elif self.dir == 1 :
            self.x = self.x + self.speed
            self.angle = self.angle-5
            self.Img = pygame.transform.rotate(self.old_Img, (self.angle % 360 + 360)%360)
        elif self.dir == -1:
            self.x = self.x - self.speed
            self.angle = self.angle+5
            self.angle = (self.angle % 360 + 360)%360
            self.Img = pygame.transform.rotate(self.old_Img, (self.angle % 360 + 360)%360)

        self.screen = screen
        self.pos = self.Img.get_rect()
        self.pos.center = (self.x, self.y)
        self.screen.blit(self.Img, self.pos)

        if self.x >= self.gr:
            self.score = 1
        elif self.x <= self.gl:
            self.score = 2


class Game:
    def __init__(self, width, height, name1, name2, goal):
        pygame.init()
        #amplify angle
        self.ang_amp = 5
        #value receive from mqtt
        self.val_l = 0
        self.val_r = 0
        self.have_l = False
        self.have_r = False
        #name & score of each team
        self.name1 = name1
        self.name2 = name2
        self.score1 = 0
        self.score2 = 0

        self.width = width
        self.height = height
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Football Game')
        self.clock = pygame.time.Clock()
        #colors
        self.black = 0, 0, 0
        self.green = 0, 255, 0
        self.blue = 0, 0, 255
        self.red = 255, 0, 0
        self.white = 255, 255, 255
        #font size
        self.font_small = 32
        self.font_large = 64

        self.goal = int(goal)
        self.goal_width = 120
        self.ball = Ball(self.width//2, 2*self.height//3-40, 40, self.goal_width, self.width)
        self.ball_x = self.ball.x
        self.r_ball_x = self.ball_x
        self.phase = 1
        self.start_ticks = pygame.time.get_ticks()
        self.start = False
        self.var = 0

    def reset(self):
        self.ball_x = self.r_ball_x
        self.ball.x = self.ball_x
        self.ball.score = 0
        self.ball.all_angle = 0
        self.ball.angle = 0
        self.start_ticks = pygame.time.get_ticks()
        if self.start:
            client.publish(send, "end")
            self.start = False

    def win(self, name):
        self.screen.fill(self.white)
        winner = Text(self.screen, self.font_large, self.black, 'center')
        winner.update(name + " win!!", self.width//2, self.height//2)

    def draw_goal(self):
        self.goalImg = pygame.image.load('goal.png')  # 919*1534
        self.goalImg = pygame.transform.scale(self.goalImg, (self.goal_width, int(self.goal_width*1534/919)))
        self.goalImg2 = pygame.transform.flip(self.goalImg, True, False)
        self.pos = self.goalImg.get_rect()
        self.pos.bottomright = (self.width, 2*self.height//3)
        self.screen.blit(self.goalImg, self.pos)
        self.pos = self.goalImg2.get_rect()
        self.pos.bottomleft = (0, 2*self.height//3)
        self.screen.blit(self.goalImg2, self.pos)

    def run(self):
        self.screen.fill(self.white)
        pygame.draw.rect(self.screen, self.green, pygame.Rect(0, 2*self.height//3, self.width, self.height//3))

        self.team1 = Text(self.screen, self.font_small, self.black, 'topleft')
        self.team1.update(self.name1, 30, 30)

        self.team2 = Text(self.screen, self.font_small, self.black, 'topright')
        self.team2.update(self.name2, self.width-30, 30)

        self.score = Text(self.screen, self.font_small, self.black, 'midtop')
        self.score.update(str(self.score1) + ' - ' + str(self.score2), self.width/2, 30)

        if self.seconds < 3:
            self.cdt = Text(self.screen, self.font_large, self.black, 'center')
            self.cdt.update(str(3-self.seconds), self.width//2, self.height//3)
        elif self.seconds == 3:
            self.cdt = Text(self.screen, self.font_large, self.black, 'center')
            self.cdt.update('start!', self.width//2, self.height//3)
            if not self.start:
                print("-start")
                client.publish(send, "start")
                self.start = True
        elif self.seconds < 13:
            self.cdt = Text(self.screen, self.font_large, self.black, 'center')
            self.cdt.update('Collecting Data : ' + str(13-self.seconds), self.width//2, self.height//3)

        elif self.seconds >= 13:
            print("-end")
            client.publish(send, "end")
            self.start_ticks = pygame.time.get_ticks()
            self.start = False

        #Control ball movement
        vr = Text(self.screen, self.font_small, self.black, 'topright')
        vr.update(self.val_r, self.width-30, 60)
        vl = Text(self.screen, self.font_small, self.black, 'topleft')
        vl.update(self.val_l, 30, 60)

        if self.have_l and self.have_r:
            
            self.have_l = self.have_r = False
            self.var = self.val_r - self.val_l
            if self.var < 0:
                self.ball.dir = 1
            elif self.var > 0:
                self.ball.dir = -1
            #print(self.val_l,self.val_r)
            self.ball.all_angle = self.ball.all_angle + self.ang_amp*self.var
            
            print(self.ball.all_angle)

        self.ball.update(self.screen)

        if self.ball.score != 0:
            if self.ball.score == 1:
                self.score1 = self.score1+1
            elif self.ball.score == 2:
                self.score2 = self.score2+1
            self.reset()

        # Draw goal on both side
        self.draw_goal()

    def update(self):
        self.seconds = (pygame.time.get_ticks()-self.start_ticks)//1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        #print(self.score1, self.score2, self.goal)
        if self.score1 >= self.goal:
            self.win(self.name1)
        elif self.score2 >= self.goal:
            self.win(self.name2)
        else:
            self.run()
        pygame.display.flip()
        self.clock.tick(30)


    # <a href="https://www.freepik.com/free-photos-vectors/sport">Sport vector created by titusurya - www.freepik.com</a>
team1, team2, goal = SettingWidget(width, height).getname()
size = width, height = 1200, 500
print(team1, team2, goal)

game = Game(1200, 500, team1, team2, goal)
while 1:
    game.update()

    # if ball.colliderect(goal1):
    #    print('goal1')
    # print(num)
    #num = num+1
    # pygame.time.wait(1000)

    # client.publish(channel2,"start")
