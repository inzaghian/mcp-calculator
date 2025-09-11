# import requests
# import json
# import logging

# class ApiCaller:
#     def __init__(self, api_key=""):
#         self.api_key = "app-OpKNg5i3oufXWY0bxRiG774B"
#         self.api_url = "https://api.dify.ai/v1/chat-messages"

#     def run(self):
#         params = ()
#         headers = {}
#         response = requests.post(self.api_url, json=params, headers=headers)


import requests
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

def xiaozhi_save_msg(msg=''):
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
        "user": "小智",
        # "files": [{
        #     "type": "image",
        #     "transfer_method": "remote_url",
        #     "url": "https://cloud.dify.ai/logo/logo-site.png"
        # }]
    }

    # 发送请求

    try:
        response = requests.post(url, headers=headers, json=payload,timeout=10000)
        # response = requests.post(url, json=headers, data=json.dumps(payload),timeout=10000)
        
        response.raise_for_status()

        print(response.text)
    except Exception as e:
        # logger.error(f"API call error: {str(e)}")
        print(e)

def xiaozhi_get_msg(msg=''):
    url = "http://anzhu.vip/v1/chat-messages"

    # 替换成你的真实 API Key
    api_key = "app-IsGIPud1KsUcvw05Eds6CnyU"

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
        "user": "小智",
        # "files": [{
        #     "type": "image",
        #     "transfer_method": "remote_url",
        #     "url": "https://cloud.dify.ai/logo/logo-site.png"
        # }]
    }

    # 发送请求

    try:
        response = requests.post(url, headers=headers, json=payload,timeout=10000)
        # response = requests.post(url, json=headers, data=json.dumps(payload),timeout=10000)
        
        response.raise_for_status()

        print(response.text)
    except Exception as e:
        # logger.error(f"API call error: {str(e)}")
        print(e)

def xiaozhi_search_msg(msg=''):
    url = "https://api.dify.ai/v1/chat-messages"

    # 替换成你的真实 API Key
    # api_key = "app-LRWcSBElvEf8nWqHlUcF20NP"
    api_key = "app-ktR8R6AMPxqh0vvUIJGETw0l"

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
        "user": "小智",
        # "files": [{
        #     "type": "image",
        #     "transfer_method": "remote_url",
        #     "url": "https://cloud.dify.ai/logo/logo-site.png"
        # }]
    }

    # 发送请求

    try:
        response = requests.post(url, headers=headers, json=payload,timeout=10000)
        # response = requests.post(url, json=headers, data=json.dumps(payload),timeout=10000)
        
        response.raise_for_status()

        print(response.text)
    except Exception as e:
        # logger.error(f"API call error: {str(e)}")
        print(e)

def meal_search(key):
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
        print(response.text)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"其他错误: {e}")

def read_memory(msg: str) -> dict:
    """
    查看小本本
    
    Args:
        message (str): 要查看的内容
    Returns:
        dict: 包含操作是否成功的结果
    """

    url = "http://101.43.187.112/v1/chat-messages"

    # 替换成你的真实 API Key
    # api_key = "app-LRWcSBElvEf8nWqHlUcF20NP"
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
        # response = requests.post(url, json=headers, data=json.dumps(payload),timeout=10000)
        
        response.raise_for_status()

        print(response.text)
    except Exception as e:
        # logger.error(f"API call error: {str(e)}")
        print(e)

    return response.text


def knowledge_api_test():
    '''
http://49.232.29.237/datasets/eaa9ecc5-1ded-4980-a1f3-e2195ccb10e8/documents/63fceffe-115e-42fe-9706-701de0977be8
        POST
            /datasets/{dataset_id}/document/create-by-text
        curl --location --request POST 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}/update-by-text' \
        --header 'Authorization: Bearer {api_key}' \
        --header 'Content-Type: application/json' \
        --data-raw '{"name": "name","text": "text"}'

        curl --location --request POST 'https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}/segments' \
        --header 'Authorization: Bearer {api_key}' \
        --header 'Content-Type: application/json' \
        --data-raw '{"segments": [{"content": "1","answer": "1","keywords": ["a"]}]}'


        curl --location --request POST 'http://49.232.29.237/v1/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}/child_chunks' \
        --header 'Authorization: Bearer {api_key}' \
        --header 'Content-Type: application/json' \
        --data-raw '{"content": "子分段内容"}'
    '''
    dataset_id = "eaa9ecc5-1ded-4980-a1f3-e2195ccb10e8"
    
    document_id = "63fceffe-115e-42fe-9706-701de0977be8"
    # url = f"https://api.dify.ai/v1/datasets/{dataset_id}/document/create-by-text"
    # ?url = f"https://api.dify.ai/v1/datasets/{dataset_id}/documents/{document_id}/segments"
    url = f"http://49.232.29.237/v1/datasets/{dataset_id}/documents/{document_id}/segments"
    
    api_key = "dataset-w5WXQpytl2lPkHwEQfkXnynE"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "segments": [{"content": "1","answer": "1","keywords": ["a"]}]
        # "name": "text",
        # "text": "123",
        # "indexing_technique": "high_quality",
        # "process_rule": {
        #     "mode": "automatic"
        # }
    }
    try:
        response = requests.post(url, headers=headers, json=payload,timeout=10000)
        # response = requests.post(url, json=headers, data=json.dumps(payload),timeout=10000)
        
        response.raise_for_status()

        print(response.text)
    except Exception as e:
        # logger.error(f"API call error: {str(e)}")
        print(e)


def search(url_in):
    # url = "https://api.firecrawl.dev/v2/search"
    url = "http://101.43.187.112:3002/v2/scrape"
    

    payload = {
        # "query": key,
        # "sources": [
        #     "web"
        # ],
        # "categories": [],
        # "limit": 5,
        # "scrapeOptions": {
        #     "onlyMainContent": True,
        #     "maxAge": 172800000,
        #     "parsers": [
        #     "pdf"
        #     ],
        #     "formats": []
        # }
        "url":url_in,
        "formats":["markdown"]
    }

    headers = {
        "Authorization": "Bearer inzaghian",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
    
    with open("search.json", 'w', encoding='utf-8') as f:
        # json.dump(response.json().get("data").get("markdown"), f, ensure_ascii=False, separators=(',', ':'))
        json.dump(response.json(), f, ensure_ascii=False, separators=(',', ':'))
        

def search_xng( 
        url = "http://101.43.187.112:8080/search",
        time_range="year",
        qurry = ''
               ) -> dict:

    url = "http://101.43.187.112:8080/search"
    headers = {
        "Authorization": "Bearer fc-385cc35c351e4b1ebc0318523e3709b1",
        "Content-Type": "application/json"
    }
    payload = {
        "q": qurry,
        "time_range":time_range,
        "format": "json",
        "safesearch":0
    }

    try:
        response = requests.get(url, params=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        logger.info(response.json())
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP错误: {e}")
        logger.error(f"响应内容: {response.text}")
    except Exception as e:
        logger.error(f"其他错误: {e}")
    return result

def scrape( 
        url_in = ""
               ) -> dict:

    url = "http://101.43.187.112:3002/v2/scrape"
    headers = {
        "Authorization": "Bearer inzaghian",
        "Content-Type": "application/json"
    }
    payload = {
        "url":url_in,
        "formats":["markdown"]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        logger.info(response.json())
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP错误: {e}")
        logger.error(f"响应内容: {response.text}")
    except Exception as e:
        logger.error(f"其他错误: {e}")
    return result

def xiaozhi() -> dict:

    url = "https://xiaozhi.me//api/agents/580717/chats/16575162/messages"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQ0Nzc1NCwidXNlcm5hbWUiOiJpbnphZ2hpYW4iLCJ0ZWxlcGhvbmUiOiIrODYxODYqKioqMjM0NyIsImdvb2dsZUVtYWlsIjpudWxsLCJyb2xlIjoidXNlciIsImlhdCI6MTc1NzIwMTk4OSwiZXhwIjoxNzY0OTc3OTg5fQ.jpYxPapsx3gNq2g8qwH6fOogSrKkA2XHUXhro9znx30z4Hoq_Wx4elCfffBp0CJcQawstdjkNA3okY8kgkbcxA",
        "Content-Type": "application/json"
    }
    payload = {
    }
    try:
        response = requests.get(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        logger.info(response.json())
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP错误: {e}")
        logger.error(f"响应内容: {response.text}")
    except Exception as e:
        logger.error(f"其他错误: {e}")
    return result


if __name__ == "__main__":

    logger.info("123")
    # xiaozhi_save_msg("记录一下今天星期几")
    # knowledge_api_test()
    # xiaozhi_get_msg("昨天都干嘛了")
    search("https://www.sina.com")
    # xiaozhi_search_msg("姐姐当家")
    # print(search_XNG("姐姐当家"))
    # meal_search("中关村")
    # read_memory("昨天干嘛了")
    # search_xng(qurry="姐姐当家")
    # scrape("https://mp.weixin.qq.com/s?src=11&timestamp=1757041671&ver=6217&signature=ARJMryy5aNrk3Ek8ERWxFCd1ZqVZ-ciIYA9w-oyeWfgN8lR22Cga-LDiPPDyCYCV-PZ6UZg8Jk8k00EGUi1-axJuMI2I6lEsBzS%2A9XUkzCYF7mj%2A310d3rM91QXLUj2K&new=1")
    # search("https://movie.douban.com/subject/37296325/")
    # search("https://www.sina.com.cn")
    # xiaozhi()

