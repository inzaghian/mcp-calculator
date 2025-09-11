import json
import requests
import logging



class search:
    def __init__(self):
        self.logger = logging.getLogger("search")

    def search_xng( 
        self,
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
            self.logger.debug(response.json())
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}")
            self.logger.error(f"响应内容: {response.text}")
        except Exception as e:
            self.logger.error(f"其他错误: {e}")
        return result

    def scrape( 
            self,
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
            self.logger.debug(response.json())
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}")
            self.logger.error(f"响应内容: {response.text}")
        except Exception as e:
            self.logger.error(f"其他错误: {e}")
        return result
    
    def search_with_scrape(self, querry) -> str:
        try:
            url_array = self.search_xng(qurry=querry, time_range="day")
            result = self.scrape(url_array.get("results")[5].get("url"))
            ret = result.get("data").get("markdown")
        except Exception as e:
            self.logger.error(f"error: {e}")
        return ret
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    searcher = search()
    # url_array = searcher.search_xng(qurry="姐姐当家", time_range="day")
    # result = searcher.scrape(url_array.get("results")[0].get("url"))
    result = searcher.search_with_scrape("董璇")
    with open("result.md", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, separators=(',', ':'))
    
