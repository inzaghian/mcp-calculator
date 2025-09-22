# SDK 使用说明 SDK user guide：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# import lark_oapi as lark

import json    
import threading
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

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
    from mqtt_client import MQTTSubscriber


    class application:
        # 配置（从环境变量或配置文件读取更安全）
        BROKER = "xxx"
        PORT = 1883
        USERNAME = "admin"  # 公共代理无需认证
        PASSWORD = "admin"
        TOPIC = "test/mqtt_topic"
        UP_STREAM_TOPIC = "feishu/upstream"
        DOWN_STREAM_TOPIC = "feishu/downstream"
        
        APP_ID = "xxxx"
        APP_SECRET = "xxxx"
        def __init__(self):
            self.mqtt = MQTTSubscriber(self.on_message, self.BROKER, self.PORT, self.USERNAME, self.PASSWORD)
            self.mqtt.start()
            # self.mqtt.publish("test/mqtt_topic", "python sended")
            # self.mqtt.subscribe(self.TOPIC)
            self.mqtt.subscribe(self.UP_STREAM_TOPIC)
            # self.mqtt.subscribe(self.DOWN_STREAM_TOPIC)
            
            # 建立长连接 Establish persistent connection
            self.cli = feishu_client(self.APP_ID, self.APP_SECRET)
            # cli.send_msg_to_user(26817659, "hello")
            self.cli.listen(self.env_h)

        def on_message(self, _self:MQTTSubscriber, msg):
            self.cli.send_msg_to_user(26817659, msg)
            print(msg)


        def env_h(self, _self:feishu_client, data:str):
            try:
                data_dict:dict = json.loads(data)
                chat_type = data_dict.get("event").get("message").get("chat_type")
                content:dict = json.loads(data_dict.get("event").get("message").get("content"))

                if data_dict.get("event").get("message").get("message_type") == "text":
                    if chat_type == "p2p":
                        # self_.send_msg_to_chat(data_dict.get("event").get("message").get("chat_id"), f"from p2p {content.get("text")}".replace("\"", "\\\""))
                        self.mqtt.publish(self.DOWN_STREAM_TOPIC, f"{content.get("text")}".replace("\"", "\\\""))
                        pass
                    elif chat_type == "group":
                        # self_.send_msg_to_chat(data_dict.get("event").get("message").get("chat_id"), f"from group {content.get("text")}".replace("\"", "\\\""))
                        pass
            except Exception as e:
                print(e)


    

    app = application()
    while True:  # 主线程可执行其他任务
        time.sleep(3)
        # cli.send_msg_to_user(26817659, "hello")
        # cli.send_msg_to_chat("oc_76cfae567ba3e549cbf5db50abce80f8", "hello")
        # print("runing")


    