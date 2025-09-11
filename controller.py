# control_computer.py
from mcp.server.fastmcp import FastMCP

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import logging
import os
import platform
import subprocess
import ctypes
import time
import requests
import json


logger = logging.getLogger('ComputerControl')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("ComputerControl")

def is_windows():
    return platform.system() == 'Windows'

def open_application(app_name):
    """打开指定名称的应用程序"""
    try:
        if is_windows():
            # 使用Windows的start命令打开应用
            subprocess.Popen(f"start {app_name}", shell=True)
            return True
        else:
            # 在macOS/Linux上使用open/xdg-open
            open_command = 'open' if platform.system() == 'Darwin' else 'xdg-open'
            subprocess.Popen([open_command, app_name])
            return True
    except Exception as e:
        logger.error(f"打开应用失败: {e}")
        return False


@mcp.tool()
def open_wechat() -> dict:
    """
    打开微信应用程序
    
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info("正在打开微信")
    # 在Windows上尝试不同方式打开微信
    if is_windows():
        try:
            # 尝试通过应用名称打开
            subprocess.Popen("start Weixin:", shell=True)
            return {"success": True, "message": "微信已打开"}
        except:
            # 尝试直接启动微信可执行文件
            try:
                wechat_path = r"C:\Program Files (x86)\Tencent\Weixin\Weixin.exe"
                os.startfile(wechat_path)
                return {"success": True, "message": "微信已打开"}
            except Exception as e:
                return {"success": False, "message": f"打开微信失败: {e}"}
    else:
        success = open_application("wechat")
        return {"success": success, "message": "微信已打开" if success else "打开微信失败"}
    
@mcp.tool()
def open_vlc() -> dict:
    """
    打开VLC媒体播放器应用程序,播放电影使用
    
    Returns:
        dict: 包含操作是否成功的结果
    """
    logger.info("正在打开VLC媒体播放器")
    
    if is_windows():
        try:
            # 尝试通过应用名称打开
            path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
            os.startfile(path)
            return {"success": True, "message": "VLC已打开"}
        except:
            # 尝试多个可能的VLC安装路径
            vlc_paths = [
                r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
                os.path.expanduser(r"~\AppData\Local\VLC\vlc.exe")
            ]
            for vlc_path in vlc_paths:
                try:
                    os.startfile(vlc_path)
                    return {"success": True, "message": "VLC已打开"}
                except:
                    continue
            
            return {"success": False, "message": "打开VLC失败: 未找到VLC安装路径"}
    
    else:  # Linux和其他类Unix系统
        try:
            # 尝试直接运行vlc命令
            subprocess.Popen(["vlc"])
            return {"success": True, "message": "VLC已打开"}
        except Exception as e:
            return {"success": False, "message": f"打开VLC失败: {e}"}
        
# @mcp.tool()
# def browse_website(url: str) -> dict:
#     """
#     使用默认浏览器打开指定网站
    
#     Args:
#         url (str): 要访问的网址
        
#     Returns:
#         dict: 包含操作是否成功的结果
#     """
#     logger.info(f"正在访问网址: {url}")
#     try:
#         # 添加URL协议前缀如果缺失
#         if not url.startswith(('http://', 'https://')):
#             url = 'https://' + url
            
#         if is_windows():
#             os.startfile(url)
#         elif platform.system() == 'Darwin':
#             subprocess.Popen(['open', url])
#         else:  # Linux
#             subprocess.Popen(['xdg-open', url])
            
#         time.sleep(1)  # 等待浏览器启动
#         return {"success": True, "message": f"已打开浏览器访问 {url}"}
#     except Exception as e:
#         logger.error(f"浏览网页失败: {e}")
#         return {"success": False, "message": f"无法访问 {url}: {e}"}


    
    
#$env:MCP_ENDPOINT = "wss://api.xiaozhi.me/mcp/?token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQ0Nzc1NCwiYWdlbnRJZCI6NTgwNzE3LCJlbmRwb2ludElkIjoiYWdlbnRfNTgwNzE3IiwicHVycG9zZSI6Im1jcC1lbmRwb2ludCIsImlhdCI6MTc1Njc0Mjc4Mn0._yVH7b-qpQaA8x0TJLMd2NQMR6n_a7s40p46jcLGBYDMttWX5y65ax-Wj6g7h1RH901GtLwUqsYAgu_8HvwMVQ"


@mcp.tool()
def search_using_XNG(message: str) -> dict:
    """
    上网搜索，当用户问你去网上搜索什么东西的时候使用这个工具
    
    Args:
        message (str): 要搜索的消息内容

    Returns:
        dict: 包含操作是否成功的结果
    """
    ret = []
# def search_XNG():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # 初始化 WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 访问 SearXNG
        driver.get("https://searx.bndkt.io")
        time.sleep(1)  # 等待页面加载
        
        # 定位搜索框并输入查询
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(message)
        
        # 提交搜索
        search_box.submit()
        time.sleep(1)  # 等待结果加载
        
        # 提取搜索结果
        results = driver.find_elements(By.CSS_SELECTOR, ".result")
        for result in results:
            try:
                title = result.find_element(By.CSS_SELECTOR, "h3").text
                # url = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                snippet = result.find_element(By.CSS_SELECTOR, ".content").text
                
                # print(f"标题: {title}")
                # print(f"URL: {url}")
                # print(f"摘要: {snippet}")
                # print("-" * 50)
                ret.append({"title":title, "snippet":snippet})
            except:
                continue  # 跳过无法解析的结果
    finally:
        driver.quit()
        
    return {"ret": ret}

# 添加更多控制功能的示例模板
@mcp.tool()
def custom_action(parameter: str) -> dict:
    """
    自定义控制操作（示例模板）
    
    Args:
        parameter (str): 操作参数说明
        
    Returns:
        dict: 包含操作结果的信息
    """
    logger.info(f"执行自定义操作: {parameter}")
    # 在这里实现具体控制逻辑
    return {"success": True, "result": f"已完成 {parameter}"}

if __name__ == "__main__":
    mcp.run(transport="stdio")