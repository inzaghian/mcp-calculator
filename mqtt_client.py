import paho.mqtt.client as mqtt
import threading
import logging

logger = logging.getLogger("mqtt")
class MQTTSubscriber:
    def __init__(self, broker:str, port:int, user:str="admin",pswd:str="admin"):
        self.client = mqtt.Client()
        self.client.username_pw_set(user, pswd)
        self.broker=broker
        self.port=port
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client:mqtt.Client, userdata, flags, rc:int):
        if rc == 0:
            logger.debug("Connected to broker")
        else:
            logger.error(f"Connection failed (code: {rc})")

    def on_message(self, client:mqtt.Client, userdata, msg:mqtt.MQTTMessage):
        print(f"[Thread-{threading.get_ident()}] Received: {msg.payload.decode()}")

    def start(self):
        self.client.connect(self.broker, self.port, 240)
        # 关键：启动后台线程处理网络流量（非阻塞）
        self.client.loop_start()
        logger.debug("Subscriber running in background thread...")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        logger.debug("Subscriber stopped")

    def publish(self, topic:str, msg:str, qos:int=0):
        self.client.publish(topic=topic, payload=msg,qos=qos)

    def subscribe(self, topic:str):
        self.client.subscribe(topic, qos=1)

# 使用示例
if __name__ == "__main__":
    import time
    import os
    from mqtt_client import MQTTSubscriber, mqtt

    logging.basicConfig(level=logging.DEBUG)
    BROKER = os.environ.get("mqtt_broker")
    PORT = int(os.environ.get("mqtt_port"))
    USERNAME = os.environ.get("mqtt_username")
    PASSWORD = os.environ.get("mqtt_password")
    TOPIC = os.environ.get("mqtt_up_stream_topic")
    DOWN_STREAM_TOPIC = os.environ.get("mqtt_down_stream_topic")

    def on_message(client:mqtt.Client, userdata, msg):
        logger.debug(msg.payload.decode())
        logger.debug(msg.topic)

    def on_connect(client:mqtt.Client, userdata, flags, rc):
        if rc==0:
            # subscriber.publish("test/mqtt_topic", "python sended")
            subscriber.subscribe(TOPIC)

    subscriber = MQTTSubscriber(BROKER, PORT, USERNAME, PASSWORD)
    subscriber.client.on_connect = on_connect
    subscriber.client.on_message = on_message
    
    subscriber.start()

    
    try:
        while True:  # 主线程可执行其他任务
            time.sleep(1)
    except KeyboardInterrupt:
        subscriber.stop()