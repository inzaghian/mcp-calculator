import requests
import json
import logging
import time
from p3_tools import convert_audio_to_p3,play_p3,convert_p3_to_audio
import os
from datetime import datetime
from Cloudflare_open_api import CloudFlare

def iso_to_timestamp(s):
    """
    使用 datetime 将 ISO 8601 UTC 字符串转换为毫秒级时间戳
    :param s: 输入字符串，如 "2025-09-09T12:23:42.000Z"
    :return: 毫秒级 UTC 时间戳（整数）
    """
    # 解析字符串为 datetime 对象
    dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
    
    # 转换为毫秒级整数
    return int(dt.timestamp())

def download_url(url, save_path=None):
    """
    下载 URL 内容
    参数:
        url (str): 要下载的 URL
        save_path (str, optional): 保存内容的文件路径，如果不提供则返回内容
    返回:
        如果 save_path 为 None，则返回下载的内容（文本或二进制）
        如果 save_path 提供，则返回保存的文件路径
    """
    try:
        # 发送 GET 请求
        response = requests.get(url)
        # 检查请求是否成功 (状态码 200)
        response.raise_for_status()
        # 判断内容类型并处理
        if save_path:
            # 二进制方式写入文件
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return save_path
        else:
            # 根据内容类型返回文本或二进制
            content_type = response.headers.get('Content-Type', '')
            if 'text' in content_type or 'json' in content_type:
                return response.text
            else:
                return response.content
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return None
    
    
class XiaozhiApi:
    class device:
        def __init__(self):
            self.id=0
            self.user_id=0
            self.mac_address=''
            self.created_at=''
            self.created_at_utc=0
            self.updated_at=''
            self.updated_at_utc=0
            self.last_connected_at=''
            self.last_connected_at_utc=0
            self.auto_update=0
            self.alias=''
            self.agent_id=0
            self.app_version=''
            self.board_name=''
            self.serial_number=''
            self.iccid=''
            self.is_auth=0

        def json(self):
            return {
                'id': self.id,
                'user_id': self.user_id,
                'mac_address': self.mac_address,
                'created_at': self.created_at,
                'created_at_utc': self.created_at_utc,
                'updated_at': self.updated_at,
                'updated_at_utc': self.updated_at_utc,
                'last_connected_at': self.last_connected_at,
                'last_connected_at_utc': self.last_connected_at_utc,
                'auto_update': self.auto_update,
                'alias': self.alias,
                'agent_id': self.agent_id,
                'app_version': self.app_version,
                'board_name': self.board_name,
                'serial_number': self.serial_number,
                'iccid': self.iccid,
                'is_auth': self.is_auth
            }
        
    class agent:
        def __init__(self):
            self.id = 0
            self.name=''
            self.tts_voice=''
            self.llm_model=''
            self.assistant_name=''
            self.user_name =''
            self.created_at=''
            self.created_at_utc:int=0
            self.updated_at=''
            self.updated_at_utc:int=0
            self.memory=''
            self.character=''
            self.long_memory_switch=0
            self.lang_code=''
            self.language=''
            self.tts_speech_speed=''
            self.asr_speed=''
            self.tts_pitch=0
            self.memory_updated_at=''
            self.memory_updated_at_utc:int=0
            self.last_device=None
            self.chat_list=[]
            self.device_list=[]

        def json(self):
            return{
                "id":self.id,
                "name":self.name,
                "tts_voice":self.tts_voice,
                "llm_model":self.llm_model,
                "assistant_name":self.assistant_name,
                "user_name":self.user_name,
                "created_at":self.created_at,
                "created_at_utc":self.created_at_utc,
                "updated_at":self.updated_at,
                "updated_at_utc":self.updated_at_utc,
                "memory":self.memory,
                "character":self.character,
                "long_memory_switch":self.long_memory_switch,
                "lang_code":self.lang_code,
                "language":self.language,
                "tts_speech_speed":self.tts_speech_speed,
                "asr_speed":self.asr_speed,
                "tts_pitch":self.tts_pitch,
                "memory_updated_at":self.memory_updated_at,
                "memory_updated_at_utc":self.memory_updated_at_utc,
                "last_device": self.last_device.json() if self.last_device is not None else None,
                "chat_list":[i.json() if i is not None else None for i in self.chat_list]
            }
        
    class summary:
        def __init__(self):
            self.title=''
            self.summary=''

        def json(self):
            return {
                "title":self.title,
                "summary":self.summary
            }
        
    class chat:
        def __init__(self):
            self.id=0
            self.user_id=0
            self.chat_id=''
            self.created_at=''
            self.created_at_utc:int=0
            
            self.device_id=0
            self.msg_count=0
            self.agent_id=0
            self.model=''
            self.token_count=0
            self.chat_summary=None
            self.mac_address=''
            self.msg_list=[]

        def json(self):
            return{
                'id':self.id,
                'user_id':self.user_id,
                'chat_id':self.chat_id,
                'created_at':self.created_at,
                'created_at_utc':self.created_at_utc,
                'device_id':self.device_id,
                'msg_count':self.msg_count,
                'agent_id':self.agent_id,
                'model':self.model,
                'token_count':self.token_count,
                'chat_summary':self.chat_summary.json() if self.chat_summary is not None else None,
                'mac_address':self.mac_address,
                'msg_list':[i.json() if i is not None else None for i in self.msg_list]
            }
        
    class message:
        def __init__(self):
            self.id=0
            self.user_id=0
            self.chat_id=0
            self.role=''
            self.content=''
            self.voice_embedding_id=0
            self.created_at=''
            self.created_at_utc:int=0
            self.name=''
            self.prompt_tokens=0
            self.total_tokens=0
            self.completion_tokens=0
            self.prompt_ms=0
            self.completion_ms=0
            self.model=''
            self.url=''
            self.voice=b''

        def json(self):
            return {
                'id':self.id,
                'user_id':self.user_id,
                'chat_id':self.chat_id,
                'role':self.role,
                'content':self.content,
                'voice_embedding_id':self.voice_embedding_id,
                'created_at':self.created_at,
                'created_at_utc':self.created_at_utc,
                'name':self.name,
                'prompt_tokens':self.prompt_tokens,
                'total_tokens':self.total_tokens,
                'completion_tokens':self.completion_tokens,
                'prompt_ms':self.prompt_ms,
                'completion_ms':self.completion_ms,
                'model':self.model,
                'url':self.url
            }

    def __init__(self, token='', name='xiaozhi open api', temp_path='temp'):
        self.token = token
        self.agent_list=[]
        self.temp_path=temp_path
        self.logger = logging.getLogger(name)
        # self.DB_ID = "a75f9dcc-cef3-4fa2-8532-37def771a895"
        self.DB_ID = "6622110f-ec38-4a29-911c-123af22042ce"
        self.API_TOKEN="N1hJo24Sf-T7jQUaCzsjMFxbhyMHNiAQDMszYR-b"
        self.ACCOUNT_ID="855ba57d2d9692b616da600e13e36283"
        self.cf = CloudFlare(self.API_TOKEN, self.ACCOUNT_ID, self.DB_ID)


    def agents_update(self)->list:
        url = f"https://xiaozhi.me/api/agents"
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
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
        try:
            if result.get("success") == True:
                for i in (result.get("data")):
                    a = self.agent()
                    a.id = i.get("id")
                    a.name=i.get("agent_name")
                    a.tts_voice=i.get("tts_voice")
                    a.llm_model=i.get("llm_model")
                    a.assistant_name=i.get("assistant_name")
                    a.user_name =i.get("user_name")
                    a.created_at=i.get("created_at")
                    a.created_at_utc = iso_to_timestamp(a.created_at)
                    a.updated_at=i.get("updated_at")
                    a.updated_at_utc = iso_to_timestamp(a.updated_at)
                    a.memory=i.get("memory")
                    a.character=i.get("character")
                    a.long_memory_switch=i.get("long_memory_switch")
                    a.lang_code=i.get("lang_code")
                    a.language=i.get("language")
                    a.tts_speech_speed=i.get("tts_speech_speed")
                    a.asr_speed=i.get("asr_speed")
                    a.tts_pitch=i.get("tts_pitch")
                    a.memory_updated_at=i.get("memory_updated_at")
                    a.memory_updated_at_utc=iso_to_timestamp(a.memory_updated_at)
                    a.last_device=self.device()
                    if i.get("last_device") is not None:
                        a.last_device.id=i.get("last_device").get("id")
                        a.last_device.mac_address=i.get("last_device").get("mac_address")
                        a.last_device.created_at=i.get("last_device").get("created_at")
                        a.last_device.created_at_utc=iso_to_timestamp(a.last_device.created_at)
                        a.last_device.updated_at=i.get("last_device").get("updated_at")
                        a.last_device.updated_at_utc=iso_to_timestamp(a.last_device.updated_at)
                        a.last_device.last_connected_at=i.get("last_device").get("last_connected_at")
                        a.last_device.auto_update=i.get("last_device").get("auto_update")
                        a.last_device.alias=i.get("last_device").get("alias")
                    self.agent_list.append(a)
                return self.agent_list
        except Exception as e:
            self.logger.error(f"error:{e}")       
        return None

    def devices_update(self, agent:agent)->agent:
        url = f"https://xiaozhi.me/api/agents/{agent.id}/devices"
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
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
        self.logger.info(result.get("data"))
        if result.get("success") == True:
            data = result.get("data")
            agent.chat_list.clear()
            for i in data:
                a = self.device()
                a.id=i.get('id')
                a.user_id=i.get('user_id')
                a.mac_address=i.get('mac_address')
                a.created_at=i.get('created_at')
                a.updated_at=i.get('updated_at')
                a.last_connected_at=i.get('last_connected_at')
                a.auto_update=i.get('auto_update')
                a.alias=i.get('alias')
                a.agent_id=i.get('agent_id')
                a.app_version=i.get('app_version')
                a.board_name=i.get('board_name')
                a.serial_number=i.get('serial_number')
                a.iccid=i.get('iccid')
                a.is_auth=i.get('is_auth')
                agent.device_list.append(a)
            return agent
        
    def chats_update(self, agent:agent)->agent:
        url = f"https://xiaozhi.me/api/agents/{agent.id}/chats"
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
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
        
        try:
            self.logger.info(result.get("data"))
            if result.get("success") == True:
                data = result.get("data")
                agent.chat_list.clear()
                for i in data:
                    a = self.chat()
                    a.id=i.get('id')
                    a.user_id=i.get('user_id')
                    a.chat_id=i.get('chat_id')
                    a.created_at=i.get('created_at')
                    a.created_at_utc=iso_to_timestamp(a.created_at)
                    a.device_id=i.get('device_id')
                    a.msg_count=i.get('msg_count')
                    a.agent_id=i.get('agent_id')
                    a.model=i.get('model')
                    a.token_count=i.get('token_count')
                    a.chat_summary=self.summary()
                    if i.get('chat_summary') is not None:
                        a.chat_summary.title=i.get('chat_summary').get('title')
                        a.chat_summary.summary=i.get('chat_summary').get('summary')
                    a.mac_address=i.get('mac_address')
                    agent.chat_list.append(a)
                return agent
        except Exception as e:
            self.logger.error(f"error:{e}")
        return None
    
    def messages_update(self, agent:agent, chat:chat)->chat:
        url = f"https://xiaozhi.me/api/agents/{agent.id}/chats/{chat.id}/messages"
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }
        payload = {
        }
        try:
            response = requests.get(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            # self.logger.info(response.json())
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {e}")
            self.logger.error(f"响应内容: {response.text}")
        except Exception as e:
            self.logger.error(f"其他错误: {e}")
        try:
            if result.get("success") == True:
                chat.msg_list.clear()
                for i in (result.get("data")):
                    a = self.message()
                    a.id=i.get("id")
                    a.user_id=i.get("user_id")
                    a.chat_id=chat.id #i.get("chat_id")
                    a.role=i.get("role")
                    a.content=i.get("content")
                    a.voice_embedding_id=i.get("voice_embedding_id")
                    a.created_at=i.get("created_at")
                    a.created_at_utc=iso_to_timestamp(a.created_at)
                    a.name=i.get("name")
                    a.prompt_tokens=i.get("prompt_tokens")
                    a.total_tokens=i.get("total_tokens")
                    a.completion_tokens=i.get("completion_tokens")
                    a.prompt_ms=i.get("prompt_ms")
                    a.completion_ms=i.get("completion_ms")
                    a.model=i.get("model")
                    p3_path=''
                    if i.get("url"):
                        a.url=i.get("url")
                    chat.msg_list.append(a)
                return chat
        except Exception as e:
            self.logger.error(f"error:{e}")
        return None
    
    def create_agent_table(self):
        sql=f'''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tts_voice TEXT NOT NULL,
                llm_model TEXT NOT NULL,
                assistant_name TEXT NOT NULL,
                user_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                created_at_utc INTEGER NOT NULL,
                updated_at TEXT NOT NULL,
                updated_at_utc INTEGER NOT NULL,
                memory TEXT NOT NULL,
                character TEXT NOT NULL,
                long_memory_switch INTEGER NOT NULL,
                lang_code TEXT NOT NULL,
                language TEXT NOT NULL,
                tts_speech_speed TEXT NOT NULL,
                asr_speed TEXT NOT NULL,
                tts_pitch INTEGER NOT NULL,
                memory_updated_at TEXT NOT NULL,
                memory_updated_at_utc INTEGER NOT NULL,
                last_device_id INTEGER
            );
            '''
        self.cf.query_db(sql)

    def create_device_table(self):
        sql=f'''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                mac_address TEXT NOT NULL,
                created_at TEXT NOT NULL,
                created_at_utc INTEGER NOT NULL,
                updated_at TEXT NOT NULL,
                updated_at_utc INTEGER NOT NULL,
                last_connected_at TEXT NOT NULL,
                last_connected_at_utc INTEGER NOT NULL,
                auto_update INTEGER NOT NULL,
                alias TEXT NOT NULL,
                agent_id INTEGER NOT NULL,
                app_version TEXT NOT NULL,
                board_name TEXT NOT NULL,
                serial_number TEXT NOT NULL,
                iccid TEXT NOT NULL,
                is_auth INTEGER NOT NULL,
                -- 外键约束
                FOREIGN KEY (agent_id) REFERENCES characters(id) ON DELETE CASCADE
            );
        '''
        self.cf.query_db(sql)
    
    def create_chats_table(self):
        sql=f'''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                chat_id TEXT NOT NULL,  -- UUID格式
                created_at TEXT NOT NULL,
                created_at_utc INTEGER NOT NULL,
                device_id INTEGER NOT NULL,
                msg_count INTEGER NOT NULL,
                agent_id INTEGER NOT NULL,
                model TEXT NOT NULL,
                token_count INTEGER NOT NULL,
                chat_title TEXT NOT NULL,      -- 从chat_summary提取
                chat_summary TEXT NOT NULL,    -- 从chat_summary提取
                mac_address TEXT NOT NULL,
                
                -- 外键约束
                FOREIGN KEY (agent_id) REFERENCES characters(id) ON DELETE CASCADE
            );
        '''
        self.cf.query_db(sql)
    
    def create_messages_table(self):
        sql=f'''
            CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            created_at_utc INTEGER NOT NULL,
            name TEXT NOT NULL,
            -- 外键约束
            FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
        );
        '''
        self.cf.query_db(sql)

    def create_voice_table(self):
        sql=f'''
            CREATE TABLE IF NOT EXISTS voice (
            id INTEGER PRIMARY KEY,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            voice_embedding_id TEXT,
            created_at TEXT NOT NULL,
            created_at_utc INTEGER NOT NULL,
            name TEXT NOT NULL,
            url TEXT NOT NULL DEFAULT '',
            voice BLOB,
            -- 外键约束
            FOREIGN KEY (id) REFERENCES messages(id) ON DELETE CASCADE
        );
        '''
        self.cf.query_db(sql)

    def insert_agent(self, agent:agent):
        sql=f'''
            INSERT INTO characters (
                id, name, tts_voice, llm_model, assistant_name, user_name, 
                created_at, created_at_utc, updated_at, updated_at_utc, 
                memory, character, long_memory_switch, lang_code, language, 
                tts_speech_speed, asr_speed, tts_pitch, 
                memory_updated_at, memory_updated_at_utc, last_device_id
            ) VALUES (
                {agent.id},
                '{self.cf.escape_quotes(agent.name)}',
                '{self.cf.escape_quotes(agent.tts_voice)}',
                '{self.cf.escape_quotes(agent.llm_model)}',
                '{self.cf.escape_quotes(agent.assistant_name)}',
                '{self.cf.escape_quotes(agent.user_name)}',
                '{self.cf.escape_quotes(agent.created_at)}',
                {agent.created_at_utc},
                '{self.cf.escape_quotes(agent.updated_at)}',
                {agent.updated_at_utc},
                '{self.cf.escape_quotes(agent.memory)}',
                '{self.cf.escape_quotes(agent.character)}',
                {agent.long_memory_switch},
                '{self.cf.escape_quotes(agent.lang_code)}',
                '{self.cf.escape_quotes(agent.language)}',
                '{self.cf.escape_quotes(agent.tts_speech_speed)}',
                '{self.cf.escape_quotes(agent.asr_speed)}',
                {agent.tts_pitch},
                '{self.cf.escape_quotes(agent.memory_updated_at)}',
                {agent.memory_updated_at_utc},
                {agent.last_device.id if agent.last_device is not None else 0}  -- 引用设备表的ID
            );
        '''
        self.cf.query_db(sql)

    def insert_device(self, device:device):
        sql=f'''
            INSERT INTO devices (
                id,
                user_id,
                mac_address,
                created_at,
                created_at_utc,
                updated_at,
                updated_at_utc,
                last_connected_at,
                last_connected_at_utc,
                auto_update,
                alias,
                agent_id,
                app_version,
                board_name,
                serial_number,
                iccid,
                is_auth
            ) VALUES (
                {device.id},
                {device.user_id},
                '{device.mac_address}',
                '{device.created_at}',
                {device.created_at_utc},
                '{device.updated_at}',
                {device.updated_at_utc},
                '{device.last_connected_at}',
                {device.last_connected_at_utc},
                {device.auto_update},
                '{device.alias}',
                {device.agent_id},
                '{device.app_version}',
                '{device.board_name}',
                '{device.serial_number}',
                '{device.iccid}',
                {device.is_auth}
            );
        '''
        self.cf.query_db(sql)

    def insert_chat(self, chat:chat):
        sql = f'''
            INSERT INTO chats (
                id, user_id, chat_id, created_at, created_at_utc, 
                device_id, msg_count, agent_id, model, token_count,
                chat_title, chat_summary, mac_address
            ) VALUES (
                {chat.id},
                {chat.user_id},
                '{self.cf.escape_quotes(chat.chat_id)}',
                '{self.cf.escape_quotes(chat.created_at)}',
                {chat.created_at_utc},
                {chat.device_id},  -- 关联设备表ID
                {chat.msg_count},
                {chat.agent_id},  -- 关联角色表ID
                '{self.cf.escape_quotes(chat.model)}',
                {chat.token_count},
                '{self.cf.escape_quotes(chat.chat_summary.title if chat.chat_summary is not None else '')}',  -- chat_summary.title
                '{self.cf.escape_quotes(chat.chat_summary.summary if chat.chat_summary is not None else '')}',  -- chat_summary.summary
                '{self.cf.escape_quotes(chat.mac_address)}'
            );
        '''
        self.cf.query_db(sql)

    def insert_message(self, message:message):
        sql = f'''
            INSERT INTO messages (
                id, chat_id, role, content,
                created_at, created_at_utc, name
            ) VALUES (
                {message.id},
                {message.chat_id},  -- 关联chats表的id
                '{self.cf.escape_quotes(message.role)}',
                '{self.cf.escape_quotes(message.content)}',
                '{self.cf.escape_quotes(message.created_at)}',
                {message.created_at_utc},
                '{self.cf.escape_quotes(message.name)}'
            );
        '''
        self.cf.query_db(sql)

    def insert_voice(self, message:message, voice:bytes):
        sql = f'''
            INSERT INTO voice (
                id, role, content, voice_embedding_id, 
                created_at, created_at_utc, name, url, voice
            ) VALUES (
                {message.id},
                '{self.cf.escape_quotes(message.role)}',
                '{self.cf.escape_quotes(message.content)}',
                '{self.cf.escape_quotes(message.voice_embedding_id)}',
                '{self.cf.escape_quotes(message.created_at)}',
                {message.created_at_utc},
                '{self.cf.escape_quotes(message.name)}',
                '{self.cf.escape_quotes(message.url)}',
                hex('{voice.hex()}')
            );
        '''
        self.cf.query_db(sql)

    def search(self, table:str, key:str, value):
        sql = f'''
            SELECT *
            FROM {table}
            WHERE {key} = {value};
        '''
        ret = self.cf.query_db(sql)
        if ret:
            if ret.get("result"):
                results:list = ret.get("result")[0].get("results")
                if results:
                    if len(results):
                        return results[0]
        return None
    
    def search_content_like(self,word:str):
        sql = f'''
            SELECT *
            FROM messages
            WHERE content LIKE '%{word}%';
        '''
        ret = self.cf.query_db(sql)
        if ret:
            if ret.get("result"):
                results:list = ret.get("result")[0].get("results")
                if results:
                    if len(results):
                        return results
        return None
    
    def get_agent_from_db(self, id):
        return self.search("characters", "id", id)
    def get_device_from_db(self, id):
        return self.search("devices", "id", id)
    def get_device_from_db(self, id):
        return self.search("devices", "id", id)
    def get_chat_from_db(self, id):
        return self.search("chats", "id", id)
    def get_message_from_db(self, id):
        return self.search("messages", "id", id)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("main")
    # 使用示例

    xz = XiaozhiApi("eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQ0Nzc1NCwidXNlcm5hbWUiOiJpbnphZ2hpYW4iLCJ0ZWxlcGhvbmUiOiIrODYxODYqKioqMjM0NyIsImdvb2dsZUVtYWlsIjpudWxsLCJyb2xlIjoidXNlciIsImlhdCI6MTc1NzIwMTk4OSwiZXhwIjoxNzY0OTc3OTg5fQ.jpYxPapsx3gNq2g8qwH6fOogSrKkA2XHUXhro9znx30z4Hoq_Wx4elCfffBp0CJcQawstdjkNA3okY8kgkbcxA")
    # print(xz.search_content_like('火锅'))

    xz.create_agent_table()
    time.sleep(0.01)
    xz.create_device_table()
    time.sleep(0.01)
    xz.create_chats_table()
    time.sleep(0.01)
    xz.create_messages_table()
    time.sleep(0.01)
    xz.create_voice_table()
    time.sleep(0.01)
    agent_list = xz.agents_update() #update agent
    if agent_list:
        for agent in agent_list:
            agent_db = xz.get_agent_from_db(agent.id)
            if agent_db:
                logger.info(agent_db)
            else:
                xz.insert_agent(agent)  #insert agent
            cur_agent = xz.chats_update(agent) #update chat list
            for device in agent.device_list:
                device_db = xz.get_device_from_db(device.id)
                if device_db:
                    logger.info(device_db)
                else:
                    xz.insert_device(device)
            for chat in agent.chat_list:
                chat_db = xz.get_chat_from_db(chat.id)
                if chat_db:
                    logger.info(chat_db)
                else:
                    xz.insert_chat(chat)
                    #only chat not found update message
                cur_chat = xz.messages_update(agent, chat)  #update message list
                for msg in chat.msg_list:
                    msg_db = xz.get_message_from_db(msg.id)
                    if msg_db:
                        pass
                    else:
                        xz.insert_message(msg)
                        if msg.url:
                            wav_file = xz.temp_path + f'/{msg.id}.wav'
                            p3_path = xz.temp_path + f'/{msg.id}.p3'
                            if download_url(msg.url, wav_file):
                                convert_audio_to_p3.encode_audio_to_opus(wav_file, p3_path)
                                os.remove(wav_file)
                                if os.path.exists(p3_path):
                                    with open(p3_path, 'rb') as p3:
                                        voice = p3.read()
                                        xz.insert_voice(msg, voice)


