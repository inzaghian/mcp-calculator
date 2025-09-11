import requests
import json
import logging
import time
import cloudflare


class CloudFlare:
    def __init__(self, token:str, account_id:str, db_id:str):
        self.logger = logging.getLogger("CloudeFlare")
        self.token = token
        self.account_id = account_id
        self.db_id = db_id

    def create_db(self, name:str):
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token,
        }
        payload = {
            "name": name,
            "primary_location_hint": "wnam"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            self.logger.info(response.json())
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}")
            self.logger.error(f"响应内容: {response.text}")
        except Exception as e:
            self.logger.error(f"其他错误: {e}")
        return result
    
    def get_db_info(self):
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.db_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token,
        }
        payload = {

        }
        try:
            response = requests.get(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            self.logger.info(response.json())
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}")
            self.logger.error(f"响应内容: {response.text}")
        except Exception as e:
            self.logger.error(f"其他错误: {e}")
        return result
    
    def get_db_list(self):
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token,
        }
        payload = {

        }
        try:
            response = requests.get(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            self.logger.info(response.json())
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}")
            self.logger.error(f"响应内容: {response.text}")
        except Exception as e:
            self.logger.error(f"其他错误: {e}")
        return result
    
    def query_db(self, sql=''):
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.db_id}/query"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token,
        }
        payload = {
            "sql": sql,
            # "params": [
            #     "firstParam",
            #     "secondParam"
            # ]
        }
        result = {}
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            self.logger.debug(response.json())
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}")
            self.logger.error(f"SQL: {sql}")
            self.logger.error(f"响应内容: {response.text}")
        except Exception as e:
            self.logger.error(f"其他错误: {e}")
        return result
    
    def escape_quotes(self, param):
        if isinstance(param, str):
            # 检查是否存在引号并直接构建映射表
            if any(c in '\'"' for c in param):
                # 创建引号到转义形式的映射
                trans_map = str.maketrans({"'": "#", '"': '#'})
                return param.translate(trans_map)
        return param
    
if __name__=="__main__":
    DB_ID = "a75f9dcc-cef3-4fa2-8532-37def771a895"
    API_TOKEN="N1hJo24Sf-T7jQUaCzsjMFxbhyMHNiAQDMszYR-b"
    ACCOUNT_ID="855ba57d2d9692b616da600e13e36283"
    cf = CloudFlare(API_TOKEN, ACCOUNT_ID, DB_ID)
    # rt = cf.create_db("123")
    # rt = cf.get_db_info("a75f9dcc-cef3-4fa2-8532-37def771a895")
    # rt = cf.get_db_list()
    # print(rt)
    # sql="SELECT * FROM test WHERE bbb = 123;"
    # sql="INSERT INTO test (aaa, bbb) VALUES ('test', 123);"
    # sql="UPDATE test SET bbb = 456 WHERE aaa = 'test';"
    # rt = cf.query_db(DB_ID, sql)
    # print(rt)
    test="今天天气不错'123123'"
    print(cf.escape_quotes(test))