import paho.mqtt.client as mqtt
host = "broker.mqttdashboard.com"
port = 8000
channel1 = "TEST/MQTT"
channel2 = "TEST/MQTT2"

client = mqtt.Client()
client.connect(host)    
    

def on_message(client, userdata,msg):
    mes = msg.payload.decode("utf-8", "strict")
    print(mes)
    if(mes == 'start'):
        x = -5
        client.publish(channel1,x)

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe(channel2)

client.on_message = on_message
client.on_connect = on_connect
client.loop_forever()
while 0:
    x = input("Send : ")
    client.publish(channel1,x)
#client.loop_forever()
    
    