import requests
import json

class FeishuDriveAPI:
    def __init__(self, access_token):
        """
        初始化 FeishuDriveAPI 类
        :param access_token: tenant_access_token 或 user_access_token
        """
        self.access_token = access_token
        self.base_url = "https://open.feishu.cn/open-apis"

    def _get_headers(self):
        """
        获取请求头，包含认证信息
        :return: 请求头字典
        """
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def get_folder_files(self, folder_token="", page_size=50, page_token=None, order_by="EditedTime", direction="DESC", user_id_type="open_id"):
        """
        获取文件夹中的文件清单
        :param folder_token: 文件夹的 token，不填写或为空字符串时获取根目录下的文件
        :param page_size: 每页显示的数据项数量，最大值为200，默认50
        :param page_token: 分页标记，第一次请求不填，表示从头开始遍历
        :param order_by: 定义清单中文件的排序方式，默认按编辑时间排序
        :param direction: 定义清单中文件的排序规则，默认降序
        :param user_id_type: 用户 ID 类型，默认 open_id
        :return: 文件夹中的文件清单
        """
        url = f"{self.base_url}/drive/v1/files"
        headers = self._get_headers()
        params = {
            "folder_token": folder_token,
            "page_size": page_size,
            "order_by": order_by,
            "direction": direction,
            "user_id_type": user_id_type
        }
        if page_token:
            params["page_token"] = page_token

        response = requests.get(url, headers=headers, params=params)
        return response.json()

class FeishuWikiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://open.feishu.cn/open-apis"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def get_space_list(self, page_token=""):
        url = f"{self.base_url}/wiki/v2/spaces"
        headers = self._get_headers()
        payload = {
            "page_token": page_token
        }
        
        response = requests.get(url, headers=headers, data=json.dumps(payload))
        return response.json()
    
    def get_space_info(self, space_id):
        url = f"{self.base_url}/wiki/v2/spaces/{space_id}"
        headers = self._get_headers()
        
        response = requests.get(url, headers=headers)
        return response.json()
    
    def create_space(self, name, description=""):
        url = f"{self.base_url}/wiki/v2/spaces"
        headers = self._get_headers()
        payload = {
            "name": name,
            "description": description
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    
    def create_nodes(self, space_id, obj_type,parent_node_token="", node_type="origin", origin_node_token="", title=""):
        url = f"{self.base_url}/wiki/v2/spaces/{space_id}/nodes"
        headers = self._get_headers()
        payload = {
            "obj_type": obj_type,
            "parent_node_token": parent_node_token,
            "node_type": node_type,
            "origin_node_token": origin_node_token,
            "title": title
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    
    def get_node_info(self, token,obj_type="wiki"):
        url = f"{self.base_url}/wiki/v2/spaces/get_node"
        headers = self._get_headers()
        payload = {
            "obj_type": obj_type,
            "token": token
        }
        
        response = requests.get(url, headers=headers, data=json.dumps(payload))
        return response.json()

class FeishuDocxAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://open.feishu.cn/open-apis"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def create_document(self, title, folder_token=""):
        url = f"{self.base_url}/docx/v1/documents"
        headers = self._get_headers()
        payload = {
            "folder_token": folder_token,
            "title": title,
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def get_document_info(self, document_id):
        url = f"{self.base_url}/docx/v1/documents/{document_id}"
        headers = self._get_headers()
        
        response = requests.get(url, headers=headers)
        return response.json()

    def get_document_raw_content(self, document_id):
        url = f"{self.base_url}/docx/v1/documents/{document_id}/raw_content"
        headers = self._get_headers()
        
        response = requests.get(url, headers=headers)
        return response.json()

    def get_document_blocks(self, document_id):
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks"
        headers = self._get_headers()
        
        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_block_contents(self, document_id, block_id):
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}"
        headers = self._get_headers()
        
        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_block_children(self, document_id, block_id):
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}/children"
        headers = self._get_headers()
        
        response = requests.get(url, headers=headers)
        return response.json()   
      
    def create_block(self, document_id, block_id, children: list, index=-1):
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}/children"
        headers = self._get_headers()
        payload = {
            "children": children,
            "index": index
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def update_block(self, document_id, block_id, operation: list):
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}"
        headers = self._get_headers()
        payload = operation
        
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        return response.json()
    
    def delete_block(self, document_id, block_id, start_index=0, end_index=1):
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}/children/batch_delete"
        headers = self._get_headers()
        payload = {
            "start_index": start_index,
            "end_index": end_index
        }
        
        response = requests.delete(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def batch_update_blocks(self, document_id, requests_list, document_revision_id=-1, client_token=None, user_id_type="open_id"):
        """
        批量更新文档中的块。

        :param document_id: 文档的唯一标识
        :param requests_list: 批量更新块的请求列表，每个请求包含块的更新信息
        :param document_revision_id: 要操作的文档版本，默认为 -1 表示最新版本
        :param client_token: 操作的唯一标识，用于幂等操作
        :param user_id_type: 用户 ID 类型，默认为 "open_id"
        :return: 返回批量更新的结果
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/batch_update"
        headers = self._get_headers()
        
        # 构建请求体
        payload = {
            "requests": requests_list,
            "document_revision_id": document_revision_id,
            "client_token": client_token,
            "user_id_type": user_id_type
        }
        
        # 发送 PATCH 请求
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        return response.json()



class FeishuBitableAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://open.feishu.cn/open-apis"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def create_bitable(self, name, folder_token=""):
        url = f"{self.base_url}/bitable/v1/apps"
        headers = self._get_headers()
        payload = {
            "folder_token": folder_token,
            "name": name,
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def get_record_content(self, app_token, table_id, record_id):
        args = {
        "filter": {
            "conjunction": "and",
            "conditions": [
                {
                    "field_name": "record_id",
                    "operator": "is",
                    "value": [
                        record_id                
                    ]
                }
            ]
        },
        "automatic_fields": False
        }
        result= self.get_record_list(app_token, table_id, args)
        record=result.get('data', {}).get('items', [{}])[0].get('fields', {})
        return record

    def get_record_list(self, app_token, table_id, args: list, page_token=""):
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/search?page_token={page_token}"
        headers = self._get_headers()
        
        payload = args
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()    

    def create_record(self, app_token, table_id, fields: list):
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = self._get_headers()
        payload = {
            "fields": fields,
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def update_record(self, app_token, table_id, record_id, fields: list):
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        headers = self._get_headers()
        payload = {
            "fields": fields,
        }
        
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def delete_record(self, app_token, table_id, record_id):
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        headers = self._get_headers()
        
        response = requests.delete(url, headers=headers)
        return response.json()

    def batch_create_records(self, app_token, table_id, records, user_id_type="open_id", client_token=None):
        """
        批量创建多维表格记录

        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param records: list, 本次请求将要新增的记录列表
        :param user_id_type: str, 用户 ID 类型，默认为 "open_id"
        :param client_token: str, 幂等操作的唯一标识符，默认为 None
        :return: dict, API 响应结果
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
        headers = self._get_headers()

        # 构建请求体
        payload = {
            "records": records
        }

        # 如果提供了 user_id_type 或 client_token，则添加到查询参数中
        params = {
            "user_id_type": user_id_type
        }
        if client_token:
            params["client_token"] = client_token

        # 发送 POST 请求
        response = requests.post(url, headers=headers, params=params, data=json.dumps(payload))
        return response.json()

    def batch_update_records(self, app_token, table_id, records, user_id_type="open_id"):
        """
        批量更新多维表格中的记录

        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param records: list, 本次请求将要更新的记录列表
        :param user_id_type: str, 用户 ID 类型，默认为 "open_id"
        :return: dict, API 响应结果
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update"
        headers = self._get_headers()

        # 构建请求体
        payload = {
            "records": records
        }

        # 构建查询参数
        params = {
            "user_id_type": user_id_type
        }

        # 发送 POST 请求
        response = requests.post(url, headers=headers, params=params, data=json.dumps(payload))
        return response.json()

    def batch_get_records(self, app_token, table_id, record_ids, user_id_type="open_id", with_shared_url=False, automatic_fields=False):
        """
        批量获取多维表格中的记录信息

        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param record_ids: list, 记录 ID 列表，最多支持 100 条记录
        :param user_id_type: str, 用户 ID 类型，默认为 "open_id"
        :param with_shared_url: bool, 是否返回记录的分享链接，默认为 False
        :param automatic_fields: bool, 是否返回自动计算的字段，默认为 False
        :return: dict, API 响应结果
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_get"
        headers = self._get_headers()

        # 构建请求体
        payload = {
            "record_ids": record_ids,
            "with_shared_url": with_shared_url,
            "automatic_fields": automatic_fields
        }

        # 构建查询参数
        params = {
            "user_id_type": user_id_type
        }

        # 发送 POST 请求
        response = requests.post(url, headers=headers, params=params, data=json.dumps(payload))
        return response.json()

    def batch_delete_records(self, app_token, table_id, record_ids):
        """
        批量删除多维表格中的记录

        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param record_ids: list, 要删除的记录 ID 列表，最多支持 500 条记录
        :return: dict, API 响应结果
        """
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete"
        headers = self._get_headers()

        # 构建请求体
        payload = {
            "records": record_ids
        }

        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()



def get_app_access_token(app_id, app_secret):
    url = f"https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "app_id": app_id,
        "app_secret": app_secret,
    }
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    return response_data.get("app_access_token")

def get_tenant_access_token(app_id, app_secret):
    url = f"https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "app_id": app_id,
        "app_secret": app_secret,
    }
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    return response_data.get("tenant_access_token")

def get_user_access_token(app_access_token,auth_code):
    url = f"https://open.feishu.cn/open-apis/authen/v1/oidc/access_token"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {app_access_token}"
    }
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code
    } 
    response = requests.post(url, headers=headers, json=payload)  
    response_data = response.json()
    return response_data


#刷新飞书access_token
def refresh_feishu_access_token(access_token,refresh_token):
    url = "https://open.feishu.cn/open-apis/authen/v1/oidc/refresh_access_token"


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()


def parse_text_to_feishu_json(text, is_first_line_heading=True, max_blocks_per_group=50):
    lines = text.strip().split('\n')
    if not lines:
        return []

    json_result = []
    current_group = []
    block_count = 0

    def add_group_to_result(group):
        if group:
            json_result.append(group)

    # 如果第一行为标题
    if is_first_line_heading and lines:
        title = lines[0].strip()
        current_group.append({
            "block_type": 3,
            "heading1": {
                "elements": [
                    {
                        "text_run": {
                            "content": title
                        }
                    }
                ],
                "style": {}
            }
        })
        block_count += 1
        lines = lines[1:]  # 剔除已经作为标题的第一行

    # 后续每行作为内容
    for content in lines:
        if max_blocks_per_group is not None and block_count >= max_blocks_per_group:
            add_group_to_result(current_group)
            current_group = []
            block_count = 0

        current_group.append({
            "block_type": 2,
            "text": {
                "elements": [
                    {
                        "text_run": {
                            "content": content.strip()
                        }
                    }
                ],
                "style": {}
            }
        })
        block_count += 1

    # 添加最后一个组
    add_group_to_result(current_group)
    
    return json_result