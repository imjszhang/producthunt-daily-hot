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

    def get_root_folder_meta(self):
        """
        获取我的空间（根文件夹）的元数据
        :return: 根文件夹的元数据
        """
        url = f"{self.base_url}/drive/explorer/v2/root_folder/meta"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        return response.json()

    def get_folder_files(self, folder_token):
        """
        获取文件夹中的文件清单
        :param folder_token: 文件夹的 token
        :return: 文件夹中的文件清单
        """
        url = f"{self.base_url}/drive/v1/files?folder_token={folder_token}"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        return response.json()

    def get_folder_meta(self, folder_token):
        """
        获取文件夹的元数据
        :param folder_token: 文件夹的 token
        :return: 文件夹的元数据
        """
        url = f"{self.base_url}/drive/explorer/v2/folder/{folder_token}/meta"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        return response.json()

    def create_folder(self, folder_name, parent_folder_token=""):
        """
        新建文件夹
        :param folder_name: 新建文件夹的名称
        :param parent_folder_token: 父文件夹的 token，默认为根文件夹
        :return: 新建文件夹的元数据
        """
        url = f"{self.base_url}/drive/v1/files/create_folder"
        headers = self._get_headers()
        payload = {
            "name": folder_name,
            "folder_token": parent_folder_token
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def move_file_or_folder(self, file_token, target_folder_token):
        """
        移动文件或文件夹
        :param file_token: 文件或文件夹的 token
        :param target_folder_token: 目标文件夹的 token
        :return: 移动操作的结果
        """
        url = f"{self.base_url}/drive/v1/files/{file_token}/move"
        headers = self._get_headers()
        payload = {
            "target_folder_token": target_folder_token
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def delete_file_or_folder(self, file_token):
        """
        删除文件或文件夹
        :param file_token: 文件或文件夹的 token
        :return: 删除操作的结果
        """
        url = f"{self.base_url}/drive/v1/files/{file_token}"
        headers = self._get_headers()
        response = requests.delete(url, headers=headers)
        return response.json()

    def check_task_status(self, task_id):
        """
        查询异步任务状态
        :param task_id: 异步任务的 ID
        :return: 任务状态
        """
        url = f"{self.base_url}/drive/v1/files/task_check?task_id={task_id}"
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
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

    """
    {
        "code": 0,
        "msg": "success",
        "data": {
            "document": {
            "document_id": "doxcni6mOy7jLRWbEylaKKC7K88",
            "revision_id": 1,
            "title": "undefined"
            }
        }
    }    
    """
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
      
    def create_block(self, document_id, block_id, children: list,index=-1):
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
    
    def delete_block(self, document_id, block_id, start_index=0,end_index=1):
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}/children/batch_delete"
        headers = self._get_headers()
        payload = {
            "start_index": start_index,
            "end_index": end_index
        }
        
        response = requests.delete(url, headers=headers, data=json.dumps(payload))
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

    def get_record_list(self, app_token, table_id, args: list,page_token=""):
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/search?page_token={page_token}"
        headers = self._get_headers()
        
        payload = args
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()    


    def create_record(self, app_token, table_id, fields:list):
        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = self._get_headers()
        payload = {
            "fields": fields,

        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()

    def update_record(self, app_token, table_id, record_id, fields:list):
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