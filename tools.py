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
from xiaozhi_open_api import XiaozhiApi

# Create an MCP server
mcp = FastMCP("tools")
searcher = search()
xz = XiaozhiApi("eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQ0Nzc1NCwidXNlcm5hbWUiOiJpbnphZ2hpYW4iLCJ0ZWxlcGhvbmUiOiIrODYxODYqKioqMjM0NyIsImdvb2dsZUVtYWlsIjpudWxsLCJyb2xlIjoidXNlciIsImlhdCI6MTc1NzIwMTk4OSwiZXhwIjoxNzY0OTc3OTg5fQ.jpYxPapsx3gNq2g8qwH6fOogSrKkA2XHUXhro9znx30z4Hoq_Wx4elCfffBp0CJcQawstdjkNA3okY8kgkbcxA")

# Add an addition tool
@mcp.tool()
def calculator(python_expression: str) -> dict:
    """For mathamatical calculation, always use this tool to calculate the result of a python expression. You can use 'math' or 'random' directly, without 'import'."""
    result = eval(python_expression, {"math": math, "random": random})
    logger.info(f"Calculating formula: {python_expression}, result: {result}")
    return {"success": True, "result": result}
# Add an addition tool
@mcp.tool()
def send_feishu_message(message: str, title: str = "系统通知") -> dict:
    """
    给猴猴发消息
    
    Args:
        message (str): 要发送的消息内容
        title (str): 消息标题，默认为"系统通知"
    
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info(f"发送飞书消息: {title} - {message}")
    
    # 构建飞书Webhook URL
    webhook_url = f"https://open.feishu.cn/open-apis/bot/v2/hook/963dcb5d-6717-41a2-baa0-264fa0a88df1"
    
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
                    "content": title
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
        # 发送POST请求
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                return {"success": True, "message": "飞书消息发送成功"}
            else:
                return {"success": False, "message": f"飞书消息发送失败: {result.get('msg', '未知错误')}"}
        else:
            return {"success": False, "message": f"HTTP错误: {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        logger.error(f"飞书消息发送请求异常: {e}")
        return {"success": False, "message": f"网络请求异常: {e}"}
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
def search_xng1(message='') -> dict:
    """
    上网搜索

    Args:
        message (str): 要搜索的内容
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info(f"上网搜索: {message}")
    url = "http://localhost:8080/search"
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
