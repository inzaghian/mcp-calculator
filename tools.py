# server.py
from mcp.server.fastmcp import FastMCP
import sys
import logging
from search import search

logger = logging.getLogger('tools')

# Fix UTF-8 encoding for Windows console
# if sys.platform == 'win32':
#     sys.stderr.reconfigure(encoding='utf-8')
#     sys.stdout.reconfigure(encoding='utf-8')

import math
import random
import requests
import json
import time
import os
import logging
from xiaozhi_open_api import XiaozhiApi
from feishu import feishu_client

logger=logging.getLogger('tools')
# Create an MCP server
mcp = FastMCP("tools")
searcher = search()
token = os.environ.get('xiaozhi_token')
if token is None:
    logger.error("xiaozhi_token is None")
logger.info(f"xiaozhi_token: {token}")

xz = XiaozhiApi(token)
APP_ID = os.environ.get('feishu_app_id')
APP_SECRET = os.environ.get('feishu_app_secret')
fs = feishu_client(app_id=APP_ID, app_secret=APP_SECRET)

# Add an addition tool
@mcp.tool()
def calculator(python_expression: str) -> dict:
    """For mathamatical calculation, always use this tool to calculate the result of a python expression. You can use 'math' or 'random' directly, without 'import'."""
    result = eval(python_expression, {"math": math, "random": random})
    logger.info(f"Calculating formula: {python_expression}, result: {result}")
    return {"success": True, "result": result}
# Add an addition tool
@mcp.tool()
def send_feishu_message(user: str, message: str = "系统通知") -> dict:
    """
    发送飞书消息给指定用户（user枚举: owner代表主人,monkey代表猴猴， other代表其他人)
    
    Args:
        user (str): ["owner", "monkey"，"other"] 
        message (str): 消息内容
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info(f"发送飞书消息: {user} - {message}")

    # 构建请求数据
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": user
                },
                "template": "blue"  # 蓝色主题
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": message
                    }
                },
                {
                    "tag": "hr"  # 分隔线
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": f"发送时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        if user == "owner":
            ret = fs.send_msg_to_user(user_id="37bg232d", msg=message)
        elif user == "monkey":
            ret = fs.send_msg_to_user(user_id="d74594e8", msg=message)
        else:
            ret = fs.send_msg_to_chat(chat_id="oc_37657c6c172643bc9dbc9785b5b9725e", msg=message)
        if ret == True:
            return {"success": True, "message": "飞书消息发送成功"}
        else:
            return {"success": False, "message": f"飞书消息发送失败: {ret}"}

    except Exception as e:
        logger.error(f"飞书消息发送失败: {e}")
        return {"success": False, "message": f"发送失败: {e}"}

# Add an addition tool
@mcp.tool()
def read_memory(msg: str) -> dict:
    """
    查看小本本
    
    Args:
        message (str): 要查看的内容
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info(f"查看小本本: {msg}")
    # url = "http://101.43.187.112/v1/chat-messages"
    url = "http://localhost/v1/chat-messages"
    api_key = "app-cAKi4MGOlz0fvcduRJVhxxQn"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {api_key}",
        'X-Custom': 'value'
    }
    payload = {
        "inputs": {},
        "query": msg,
        "response_mode": "blocking", #  "blocking" or "streaming"
        "conversation_id": "",
        "user": "小智"
    }
    # 发送请求
    try:
        response = requests.post(url, headers=headers, json=payload,timeout=10000)
        response.raise_for_status()
    except Exception as e:
        logger.error(e)
    return response.text    
    
@mcp.tool()
def save_msg(msg='') -> dict:
    """
    记录小本本
    Args:
        message (str): 要记录的内容
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info(f"记录小本本: {msg}")
    url = "https://api.dify.ai/v1/chat-messages"

    # 替换成你的真实 API Key
    api_key = "app-OpKNg5i3oufXWY0bxRiG774B"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {api_key}",
        'X-Custom': 'value'
    }

    payload = {
        "inputs": {},
        "query": msg,
        "response_mode": "blocking", #  "blocking" or "streaming"
        "conversation_id": "",
        "user": "小智"
    }
    # 发送请求

    try:
        response = requests.post(url, headers=headers, json=payload,timeout=10000)
        response.raise_for_status()
        logger.info(response.text)
    except Exception as e:
        logger.error(f"API call error: {str(e)}")
        # print(e)
    return response.text

# Add an addition tool
@mcp.tool()
def meal_search(key) -> dict:
    """
    查找美食
    
    Args:
        message (str): 要查看的位置
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info(f"查找美食: {key}")
    url = "https://restapi.amap.com/v3/place/around"

    # 参数直接放在URL查询字符串中（不需要JSON）
    params = {
        "key": "26cb17f8c07aeb711aafbc6f98cb7a4c",
        "location": "116.473168,39.993015",
        # "radius": 10000,
        "keywords": key,
        "show_fields":["name", "address", "opentime2","'ratin" ],
        "types":"050000"
    }

    # 发送GET请求
    response = requests.get(url, params=params)

    # 检查响应状态
    try:
        response.raise_for_status()
        result = response.json()
        logger.info(result)
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP错误: {e}")
        logger.error(f"响应内容: {response.text}")
    except Exception as e:
        logger.error(f"其他错误: {e}")
    return response.text

@mcp.tool()
def search_xng(message='') -> dict:
    """
    上网搜索，当用户需要查找某些信息时，可以使用这个工具

    Args:
        message (str): 要搜索的内容
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info(f"上网搜索: {message}")
    url = "http://101.43.187.112:8080/search"
    payload = {
    "q": message,
    "format": "json"
    }
    headers = {
        "Authorization": "Bearer fc-385cc35c351e4b1ebc0318523e3709b1",
        "Content-Type": "application/json"
    }
    response = requests.get(url, params=payload, headers=headers)

    return (response.json())
    # return searcher.search_with_scrape(message)

# @mcp.tool()
# def firecrawl(msg='') -> dict:
#     """
#     当需要查看某些网址的内容时，可以使用爬虫工具获取并总结
#     Args:
#         message (str): 必须是正确的一个URL网址，注意格式和数量必须正确，不可以添加其他内容
#     Returns:
#         dict: 包含操作是否成功的结果
#     """
#     logger.info(f"爬虫工具: {msg}")
#     url = "http://localhost/v1/chat-messages"

#     # 替换成你的真实 API Key
#     api_key = "app-eHXDuQeeUG5TAgAnQEIRXgOj"
#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "Authorization": f"Bearer {api_key}",
#         'X-Custom': 'value'
#     }

#     payload = {
#         "inputs": {},
#         "query": msg,
#         "response_mode": "blocking", #  "blocking" or "streaming"
#         "conversation_id": "",
#         "user": "小智"
#     }

#     # 发送请求
#     try:
#         response = requests.post(url, headers=headers, json=payload,timeout=10000)
#         response.raise_for_status()
#         logger.info(response.text)
#     except Exception as e:
#         logger.error(f"API call error: {str(e)}")
#     return response.text
@mcp.tool()
def search_sql(message='') -> dict:
    """
    搜索历史，记忆查找，当用户问：还记得xxx或者你想想之前说过的话时使用这个方法

    Args:
        message (str): 要搜索的内容
    Returns:
        dict: 包含操作是否成功的结果
    """
    return xz.search_content_like(message)
# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
