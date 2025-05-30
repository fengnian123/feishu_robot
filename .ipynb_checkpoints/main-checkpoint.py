import lark_oapi as lark
from lark_oapi.api.im.v1 import *
import json
from config import knowledge, qwen_model, agent, app_id, app_secret
from camel.messages import BaseMessage
import os
# 注册接收消息事件，处理接收到的消息。
# Register event handler to handle received messages.
# https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    res_content = ""
    if data.event.message.message_type == "text":
        knowledge_message = BaseMessage.make_user_message(
            role_name="User", content=f"Based on the following knowledge: {knowledge}"
        )
        agent.update_memory(knowledge_message, "user")
        assistant_response = agent.step(json.loads(data.event.message.content)["text"])
        res_content = assistant_response.msgs[0].content
    else:
        res_content = "解析消息失败，请发送文本消息\nparse message failed, please send text message"

<<<<<<< HEAD
    content_data = {
        "zh_cn": {
            "content": [
                [
                    {"tag": "md", "text": res_content}
                ]
            ]
        }
    }
    content = json.dumps(content_data)
=======
    content = json.dumps(
        {
            "text": ""
            + res_content
        }
    )
>>>>>>> 01711ad55d00a0a0a6b94443a24e48d2d92630e9

    if data.event.message.chat_type == "p2p":
        request = (
            CreateMessageRequest.builder()
            .receive_id_type("chat_id")
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(data.event.message.chat_id)
<<<<<<< HEAD
                .msg_type("post")
=======
                .msg_type("text")
>>>>>>> 01711ad55d00a0a0a6b94443a24e48d2d92630e9
                .content(content)
                .build()
            )
            .build()
        )
        # 使用OpenAPI发送消息
        # Use send OpenAPI to send messages
        # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        response = client.im.v1.chat.create(request)

        if not response.success():
            raise Exception(
                f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
            )
    else:
        request: ReplyMessageRequest = (
            ReplyMessageRequest.builder()
            .message_id(data.event.message.message_id)
            .request_body(
                ReplyMessageRequestBody.builder()
                .content(content)
<<<<<<< HEAD
                .msg_type("post")
=======
                .msg_type("text")
>>>>>>> 01711ad55d00a0a0a6b94443a24e48d2d92630e9
                .build()
            )
            .build()
        )
        # 使用OpenAPI回复消息
        # Reply to messages using send OpenAPI
        # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/reply
        response: ReplyMessageResponse = client.im.v1.message.reply(request)
        if not response.success():
            raise Exception(
                f"client.im.v1.message.reply failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
            )


# 注册事件回调
# Register event handler.
event_handler = (
    lark.EventDispatcherHandler.builder("", "")
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1)
    .build()
)


# 创建 LarkClient 对象，用于请求OpenAPI, 并创建 LarkWSClient 对象，用于使用长连接接收事件。
# Create LarkClient object for requesting OpenAPI, and create LarkWSClient object for receiving events using long connection.
client = lark.Client.builder().app_id(app_id).app_secret(app_secret).build()
wsClient = lark.ws.Client(
    app_id,
    app_secret,
    event_handler=event_handler,
    log_level=lark.LogLevel.DEBUG,
)


def main():
    #  启动长连接，并注册事件处理器。
    #  Start long connection and register event handler.
    wsClient.start()


if __name__ == "__main__":
    main()
