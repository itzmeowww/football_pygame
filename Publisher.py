import paho.mqtt.client as mqtt
host = "broker.mqttdashboard.com"
port = 8000
channel1 = "TEST/MQTT"
channel2 = "TEST/MQTT2"


   
x = 5
def send():
    x = input('x : ')
    client.publish(channel1,x)
    print("Sent => " + str(x))

def on_message(client, userdata,msg):
    mes = msg.payload.decode("utf-8", "strict")
    #print(mes)
    
    if mes == "start":
        print("START")
        send()
        
    elif mes == "end":
        print("END")

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe(channel2)
    print("Subscribed to channel " + str(channel2))
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host) 
client.loop_start()
while(1):
    x = 1

#client.loop_forever()
    
    