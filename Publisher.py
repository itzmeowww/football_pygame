import paho.mqtt.client as mqtt
host = "broker.mqttdashboard.com"
port = 8000
receive = "topic/1"
send_l = "topic/l"
send_r = "topic/r"    


left = 0

right = 0
def on_message(_client, userdata, msg):
    global left 
    global right
    mes = msg.payload.decode("utf-8", "strict")
    print("MES : " + mes)

    if mes == "start":
        print("START")
        left = input("l : ")
        right = input("r : ")

    elif mes == "end":
        client.publish(send_l,left)
        client.publish(send_r,right)
        print(str(left),str(right))
        


def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe(receive)
    print("Subscribed to channel " + str(receive))


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host)
client.loop_start()

while(1):
    x = 1

# client.loop_forever()
