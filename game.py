import pygame
import sys
import tkinter as tk
import paho.mqtt.client as mqtt

# This is setting for mqtt
# host = "broker.mqttdashboard.com"
# port = 8000
host = "localhost"
port = 1883
receive_l = "topic/l"
receive_r = "topic/r"
send = "topic/1"

class SettingWidget:
    def btn(self):
        self.name1 = self.input_name1.get()
        self.name2 = self.input_name2.get()
        self.score_to_win = int(self.input_score_to_win.get())
        self.game_height = int(self.input_game_height.get())
        self.game_width = int(self.input_game_width.get())
        self.game_ang_mul = int(self.input_game_ang_mul.get())
        #print(self.name1, self.name2)
        self.widget.destroy()

    def __init__(self, _width, _height):
        self.widget_width = _width
        self.widget_height = _height
        self.name1 = "MUN"
        self.name2 = "LIV"
        self.score_to_win = 5
        self.game_width = 1200
        self.game_height = 500
        self.game_ang_mul = 5
        self.widget = tk.Tk()
        # Gets both half the screen width/height and window width/height
        self.positionRight = int(self.widget.winfo_screenwidth()/2-70)
        self.positionDown = int(self.widget.winfo_screenheight()/2-70)

        # Positions the window in the center of the page.
        self.widget.geometry(
            "+{}+{}".format(self.positionRight, self.positionDown))
        # self.widget.geometry(str(width)+"x"+str(height))
        self.widget.title('Setting')
        self.create_widget()

    def add_input(self, text, val, row, column):
        tk.Label(self.widget, text=text).grid(row=row)
        sv = tk.StringVar()
        entry = tk.Entry(self.widget, textvariable=sv)
        entry.grid(row=row, column=column+1)
        sv.set(str(val))

        return entry

    def create_widget(self):

        tk.Label(self.widget, text='Goal').grid(row=2)

        self.input_name1 = self.add_input(
            'First team\'s name', self.name1, 0, 0)
        self.input_name2 = self.add_input(
            'Second team\'s name', self.name2, 1, 0)
        self.input_score_to_win = self.add_input(
            'Score to win', self.score_to_win, 2, 0)

        tk.Label(self.widget, text='').grid(row=3)

        self.input_game_width = self.add_input(
            'Game width', self.game_width, 4, 0)
        self.input_game_height = self.add_input(
            'Game height', self.game_height, 5, 0)
        self.input_game_ang_mul = self.add_input(
            'Game angle co-efficient', self.game_ang_mul, 6, 0)
        self.enter_btn = tk.Button(
            self.widget, text='Enter the game', width=25, command=self.btn)
        self.enter_btn.grid(row=7, columnspan=2)
        self.widget.mainloop()

    def getname(self):
        return self.name1, self.name2, self.score_to_win, self.game_width, self.game_height, self.game_ang_mul


def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe([(receive_l, 0), (receive_r, 1)])
    print("Subscribed")


def on_message(client, userdata, msg):
    mes = msg.payload.decode("utf-8", "strict")
    print("message received " ,str(msg.payload.decode("utf-8")))
    print("message topic=",msg.topic)
    data = int(float(str(msg.payload.decode("utf-8"))))
    print('data = ', data)

    if msg.topic == "topic/l":
        game.val_l = data
        print("in message left")
        print(game.val_l)
        game.have_l = True
    elif msg.topic == "topic/r":
        game.val_r = data
        print("in message right")
        print(game.val_r)
        game.have_r = True


Client = mqtt.Client()
Client.on_connect = on_connect
Client.on_message = on_message
Client.connect(host, port = port)
Client.loop_start()


class Text:
    def __init__(self, screen, _size, color, _type,):
        self.size = _size
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
        self.screen = screen
        self.type = _type
        self.color = color
        self.text = None
        self.rect = None

    def update(self, text, x, y):
        self.text = self.font.render(str(text), True, self.color)
        self.rect = self.text.get_rect()
        setattr(self.rect, self.type, (x, y))
        #self.rect.midleft = (30,30)
        self.screen.blit(self.text, self.rect)


class Ball:
    def __init__(self, x, y, r, goal_width, canvas_width, screen):
        self.speed = 5
        self.canvas_width = canvas_width
        self.goal_width = goal_width
        self.screen = screen
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

    def update(self):
        #print("UP ", self.all_angle, self.angle)

        if self.all_angle == self.angle:
            self.angle = self.angle
            self.dir = 0
        elif self.dir == 1:
            self.x = self.x + self.speed
            self.angle = self.angle-5
            self.Img = pygame.transform.rotate(
                self.old_Img, (self.angle % 360 + 360) % 360)
        elif self.dir == -1:
            self.x = self.x - self.speed
            self.angle = self.angle+5
            self.angle = (self.angle % 360 + 360) % 360
            self.Img = pygame.transform.rotate(
                self.old_Img, (self.angle % 360 + 360) % 360)

        
        self.pos = self.Img.get_rect()
        self.pos.center = (self.x, self.y)
        self.screen.blit(self.Img, self.pos)

        if self.x >= self.gr:
            self.score = 1
        elif self.x <= self.gl:
            self.score = 2


class Game:
    def __init__(self, name1, name2, goal, width, height, ang_mul):
        pygame.init()
        # amplify angle
        self.ang_mul = ang_mul
        # value receive from mqtt
        self.collecting_time = 10
        self.prepare_time = 3
        self.val_l = 0
        self.val_r = 0
        self.have_l = False
        self.have_r = False
        # name & score of each team
        self.name1 = name1
        self.name2 = name2
        self.score1 = 0
        self.score2 = 0

        self.width = width
        self.height = height
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Synch - Ball')
        self.clock = pygame.time.Clock()
        # colors
        self.black = 0, 0, 0
        self.green = 55, 148, 7
        self.blue = 116, 236, 242
        self.red = 255, 0, 0
        self.white = 255, 255, 255
        # font size
        self.font_small = 32
        self.font_large = 64

        self.goal = int(goal)
        self.goal_width = 120
        self.ball = Ball(self.width//2, 2*self.height//3 -
                         40, 40, self.goal_width, self.width,self.screen)
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
            Client.publish(send, "end")
            self.start = False

    def win(self, name):
        self.screen.fill(self.blue)
        winner = Text(self.screen, self.font_large, self.black, 'center')
        winner.update(name + " is the winner!!", self.width//2, self.height//2)

    def draw_goal(self):
        self.goalImg = pygame.image.load('goal.png')  # 919*1534
        self.goalImg = pygame.transform.scale(
            self.goalImg, (self.goal_width, int(self.goal_width*1534/919)))
        self.goalImg2 = pygame.transform.flip(self.goalImg, True, False)
        self.pos = self.goalImg.get_rect()
        self.pos.bottomright = (self.width, 2*self.height//3)
        self.screen.blit(self.goalImg, self.pos)
        self.pos = self.goalImg2.get_rect()
        self.pos.bottomleft = (0, 2*self.height//3)
        self.screen.blit(self.goalImg2, self.pos)

    def run(self):
        self.screen.fill(self.blue)
        pygame.draw.rect(self.screen, self.green, pygame.Rect(
            0, 2*self.height//3, self.width, self.height//3))

        self.team1 = Text(self.screen, self.font_small, self.black, 'topleft')
        self.team1.update(self.name1, 30, 30)

        self.team2 = Text(self.screen, self.font_small, self.black, 'topright')
        self.team2.update(self.name2, self.width-30, 30)

        self.score = Text(self.screen, self.font_small, self.black, 'midtop')
        self.score.update(str(self.score1) + ' - ' +
                          str(self.score2), self.width/2, 30)

        if self.seconds < self.prepare_time:
            self.cdt = Text(self.screen, self.font_large, self.black, 'center')
            self.cdt.update(str(3-self.seconds), self.width//2, self.height//3)
        elif self.seconds == self.prepare_time:
            self.cdt = Text(self.screen, self.font_large, self.black, 'center')
            self.cdt.update('start!', self.width//2, self.height//3)
            if not self.start:
                # print("-start")
                Client.publish(send, "start")
                self.start = True
        elif self.seconds < self.prepare_time + self.collecting_time:
            self.cdt = Text(self.screen, self.font_large, self.black, 'center')
            self.cdt.update('Collecting Data : ' +
                            str(13-self.seconds), self.width//2, self.height//3)

        elif self.seconds >= self.prepare_time + self.collecting_time:
            # print("-end")
            Client.publish(send, "end")
            self.start_ticks = pygame.time.get_ticks()
            self.start = False

        # Control ball movement
        vr = Text(self.screen, self.font_small, self.black, 'topright')
        vr.update("Synch Index : " + str(self.val_r),
                  self.width-80, self.height-60)

        vl = Text(self.screen, self.font_small, self.black, 'topleft')
        vl.update("Synch Index : " + str(self.val_l), 80, self.height-60)

        if self.have_l and self.have_r:

            self.have_l = self.have_r = False
            self.var = self.val_r - self.val_l
            if self.var < 0:
                self.ball.dir = 1
            elif self.var > 0:
                self.ball.dir = -1
            # print(self.val_l,self.val_r)
            self.ball.all_angle = self.ball.all_angle + self.ang_mul*self.var

            print(self.ball.all_angle)

        self.ball.update()

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

    def begin(self):
        while(1):
            self.update()

    # <a href="https://www.freepik.com/free-photos-vectors/sport">Sport vector created by titusurya - www.freepik.com</a>


size = width, height = 300, 100
team1, team2, goal, width, height, ang_mul = SettingWidget(
    width, height).getname()
size = width, height
game = Game(team1, team2, goal, width, height, ang_mul)
game.begin()
print('exit')
