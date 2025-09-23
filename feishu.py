# SDK 使用说明 SDK user guide：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# import lark_oapi as lark

import json    
import threading
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
import logging

logger = logging.getLogger("feishu")
class feishu_client:

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

        self.client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    def listen(self, event_handle):
        self.event_handler = lark.EventDispatcherHandler.builder("", "") \
            .register_p2_im_message_receive_v1(self._do_p2_im_message_receive_v1) \
            .build()
        self.cli = lark.ws.Client(self.app_id, self.app_secret,
                    event_handler=self.event_handler, log_level=lark.LogLevel.INFO)
        self.thread = threading.Thread(target=self.cli.start, daemon=True)
        self.event_handle = event_handle
        self.thread.start()


    def _do_p2_im_message_receive_v1(self, data: lark.im.v1.P2ImMessageReceiveV1) -> None:
        if self.event_handle:
            self.event_handle(self, lark.JSON.marshal(data, indent=4))


    def send_msg_to_user(self, user_id, content)->bool:
            # 构造请求对象
        request: CreateMessageRequest = CreateMessageRequest.builder() \
            .receive_id_type("user_id") \
            .request_body(CreateMessageRequestBody.builder()
                .receive_id(f"{user_id}")
                .msg_type("text")
                .content(f"{{\"text\":\"{content}\"}}")
                .build()) \
            .build()

        # 发起请求
        response: CreateMessageResponse = self.client.im.v1.message.create(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return False
        return True
        # 处理业务结果
        # lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    def send_msg_to_chat(self, chat_id, msg)->bool:
         # 构造请求对象
        request: CreateMessageRequest = CreateMessageRequest.builder() \
            .receive_id_type("chat_id") \
            .request_body(CreateMessageRequestBody.builder()
                .receive_id(f"{chat_id}")
                .msg_type("text")
                .content(f"{{\"text\":\"{msg}\"}}")
                .build()) \
            .build()

        # 发起请求
        response: CreateMessageResponse = self.client.im.v1.message.create(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return False
        return True

        # 处理业务结果
        # lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    import time
    import os
    import sys
    import signal
    from mqtt_client import MQTTSubscriber, mqtt
    logging.basicConfig(level=logging.INFO)

    class application:
        def __init__(self):
            signal.signal(signal.SIGINT, self.signal_handler)
            self.BROKER = os.environ.get('mqtt_broker')
            self.PORT = int(os.environ.get('mqtt_port'))
            self.USERNAME = os.environ.get('mqtt_username')
            self.PASSWORD = os.environ.get('mqtt_password')
            self.UP_STREAM_TOPIC = os.environ.get('mqtt_up_stream_topic')
            self.DOWN_STREAM_TOPIC = os.environ.get('mqtt_down_stream_topic')
            self.APP_ID = os.environ.get('feishu_app_id')
            self.APP_SECRET = os.environ.get('feishu_app_secret')
            self.mqtt = MQTTSubscriber(self.BROKER, self.PORT, self.USERNAME, self.PASSWORD)
            self.mqtt.client.on_connect = self.on_mqtt_connect
            self.mqtt.client.on_message = self.on_mqtt_message
            self.mqtt.start()
            self.cli = feishu_client(self.APP_ID, self.APP_SECRET)
            self.cli.listen(self.on_feishu_message)
            
        def on_mqtt_connect(self, client:mqtt.Client, userdata, flags, rc:int):
            if rc==0:
                self.mqtt.subscribe(self.UP_STREAM_TOPIC)

        def on_mqtt_message(self, client:mqtt.Client, userdata, msg:mqtt.MQTTMessage):
            if msg.topic == self.UP_STREAM_TOPIC:
                msg = msg.payload.decode()
                self.cli.send_msg_to_user(26817659, msg)
                logger.info(msg)
            elif msg.topic == self.DOWN_STREAM_TOPIC:
                msg = msg.payload.decode()
                logger.info(f"down stream:{msg}")

        def on_feishu_message(self, _self:feishu_client, data:str):
            try:
                data_dict:dict = json.loads(data)
                logger.info(data_dict)
                chat_type = data_dict.get("event").get("message").get("chat_type")
                content:dict = json.loads(data_dict.get("event").get("message").get("content"))

                if data_dict.get("event").get("message").get("message_type") == "text":
                    if chat_type == "p2p":
                        # self_.send_msg_to_chat(data_dict.get("event").get("message").get("chat_id"), f"from p2p {content.get("text")}".replace("\"", "\\\""))
                        self.mqtt.publish(
                            self.DOWN_STREAM_TOPIC, 
                            f"{content.get("text")}".replace("\"", "\\\"")
                        )
                    elif chat_type == "group":
                        # self_.send_msg_to_chat(data_dict.get("event").get("message").get("chat_id"), f"from group {content.get("text")}".replace("\"", "\\\""))
                        self.mqtt.publish(
                            self.DOWN_STREAM_TOPIC, 
                            f"{content.get("text")}".replace("\"", "\\\"")
                        )
            except Exception as e:
                logger.error(e)
        def signal_handler(self, sig, frame):
            """Handle interrupt signals"""
            logger.info("Received interrupt signal, shutting down...")
            sys.exit(0)

    app = application()
    try:
        while True:  # 主线程可执行其他任务
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Program execution error: {e}")



    