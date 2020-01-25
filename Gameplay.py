import pygame
import sys
import tkinter as tk
import paho.mqtt.client as mqtt

host = "broker.mqttdashboard.com"
port = 8000
channel1 = "TEST/MQTT"
channel2 = "TEST/MQTT2"

size = width, height = 500, 500
#Setting menu
#For setting the name of each team and the goal
class SettingWidget:
    def btn(self):
        self.name1 = self.entry1.get()
        self.name2 = self.entry2.get()
        self.goal = int(self.entrygoal.get())
        #print(self.name1, self.name2)
        self.widget.destroy()

    def __init__(self,width,height):
        self.name1 = "MCU"
        self.name2 = "LIV"
        self.goal = 5
        self.widget = tk.Tk()
        self.widget.geometry(str(width)+"x"+str(height))
        self.widget.title('Setting')
        self.create_widget()
        
    def create_widget(self):
        tk.Label(self.widget,text = 'First team\'s name').grid(row=0)
        tk.Label(self.widget,text = 'Second team\'s name').grid(row=1)
        tk.Label(self.widget,text = 'Goal').grid(row=2)
        self.v1 = tk.StringVar()
        self.entry1 = tk.Entry(self.widget,textvariable = self.v1)
        self.entry1.grid(row=0,column = 1)
        self.v1.set(self.name1)

        self.v2 = tk.StringVar()
        self.entry2 = tk.Entry(self.widget,textvariable = self.v2)
        self.entry2.grid(row=1,column = 1)
        self.v2.set(self.name2)
        
        self.vg = tk.StringVar()
        self.entrygoal = tk.Entry(self.widget,textvariable = self.vg)
        self.entrygoal.grid(row=2,column = 1)
        self.vg.set(str(self.goal))
        
        self.enter_btn = tk.Button(self.widget, text='Enter the game', width=25, command = self.btn)
        self.enter_btn.grid(row=3) 
        self.widget.mainloop()

    def getname(self):
        return (self.name1,self.name2,self.goal)
    
        

team1, team2, goal = SettingWidget(width,height).getname()
size = width, height = 1200, 500
print(team1, team2, goal)

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe(channel1)

def on_message(client, userdata,msg):
    print(msg.payload.decode("utf-8", "strict"))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host) 
client.loop_start()



black = 0, 0, 0
green = 0,255,0
blue = 0,0,255
white = 255,255,255
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Football Game')
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

ball_r = 40
ball_pos = ball_x, ball_y = width//2, 2*height//3-ball_r

score1 = 0
score2 = 0

done = False

num = 0

while not done:
    screen.fill(white)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    score = font.render(str(score1)+' - '+str(score2), True, black)
    pos = score.get_rect()
    pos.center = (width//2,30)
    screen.blit(score,pos) 

    _team1 = font.render(team1, True, black)
    pos = _team1.get_rect()
    pos.midleft = (30,30)
    screen.blit(_team1,pos) 

    _team2 = font.render(team2, True, black)
    pos = _team2.get_rect()
    pos.midright = (width-30,30)
    screen.blit(_team2,pos)



    pygame.draw.rect(screen, green, pygame.Rect(0, 2*height//3, width, height//3))
    #<a href="https://www.freepik.com/free-photos-vectors/sport">Sport vector created by titusurya - www.freepik.com</a>
    ballImg = pygame.image.load('ball.png') 
    ballImg = pygame.transform.scale(ballImg,(2*ball_r,2*ball_r))

    goalImg = pygame.image.load('goal.png') # 919*1534
    goalImg = pygame.transform.scale(goalImg,(120,int(120*1534/919)))
    goalImg2 = pygame.transform.flip(goalImg,True,False)
    pos = ballImg.get_rect()
    pos.center = (ball_pos)
    screen.blit(ballImg,pos)

    pos = goalImg.get_rect()
    pos.bottomright = (width,2*height//3)
    screen.blit(goalImg,pos)

    pos = goalImg2.get_rect()
    pos.bottomleft = (0,2*height//3)
    screen.blit(goalImg2,pos)
    
    
    
    #if ball.colliderect(goal1):
    #    print('goal1')
    #print(num)
    #num = num+1
    #pygame.time.wait(1000)
    
    #client.publish(channel2,"start")
    
    pygame.display.flip()
    clock.tick(60)
   
