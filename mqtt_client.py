import paho.mqtt.client as mqtt
import threading



class MQTTSubscriber:
    def __init__(self, on_msg, broker:str, port:int, user:str="admin",pswd:str="admin"):
        self.client = mqtt.Client()
        self.client.username_pw_set(user, pswd)
        self.broker=broker
        self.port=port
        self.on_msg = on_msg
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            # client.subscribe(TOPIC, qos=1)
        else:
            print(f"Connection failed (code: {rc})")

    def on_message(self, client:mqtt.Client, userdata, msg):
        print(f"[Thread-{threading.get_ident()}] Received: {msg.payload.decode()}")
        if self.on_msg:
            self.on_msg(self, msg.payload.decode())

    def start(self):
        self.client.connect(self.broker, self.port, 240)
        # 关键：启动后台线程处理网络流量（非阻塞）
        self.client.loop_start()
        print("Subscriber running in background thread...")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Subscriber stopped")

    def publish(self, topic:str, msg:str, qos:int=0):
        self.client.publish(topic=topic, payload=msg,qos=qos)

    def subscribe(self, topic:str):
        self.client.subscribe(topic, qos=1)

# 使用示例
if __name__ == "__main__":
    import time
    # 配置（从环境变量或配置文件读取更安全）
    BROKER = "xxx"
    PORT = 1883
    USERNAME = "admin"  # 公共代理无需认证
    PASSWORD = "admin"
    TOPIC = "test/mqtt_topic"

    def on_message(self_:MQTTSubscriber, msg):
        print(msg)

    subscriber = MQTTSubscriber(on_message, BROKER, PORT, USERNAME, PASSWORD)
    subscriber.start()
    subscriber.publish("test/mqtt_topic", "python sended")
    subscriber.subscribe(TOPIC)
    
    try:
        while True:  # 主线程可执行其他任务
            time.sleep(1)
    except KeyboardInterrupt:
        subscriber.stop()