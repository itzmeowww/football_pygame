import paho.mqtt.client as mqtt
host = "localhost"
port = 1883
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
    send = False
    if mes == "start" and not send:
        send = True
        print("START")
        left = input("l : ")
        right = input("r : ")
        client.publish(send_l,left)
        client.publish(send_r,right)
        print(str(left),str(right))
        send = False
        


def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe(receive)
    print("Subscribed to channel " + str(receive))


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host,port=port)
client.loop_start()

while(1):
    x = 1

# client.loop_forever()
