# file name: feishu_bitable_api_handler.py
from feishu_app_api import FeishuBitableAPI, get_tenant_access_token

class FeishuBitableAPIHandler:
    def __init__(self, FEISHU_APP_ID, FEISHU_APP_SECRET):
        self.FEISHU_APP_ID = FEISHU_APP_ID
        self.FEISHU_APP_SECRET = FEISHU_APP_SECRET
        self.FEISHU_TENANT_ACCESS_TOKEN = get_tenant_access_token(self.FEISHU_APP_ID, self.FEISHU_APP_SECRET)
        self.feishu_bitable_api = FeishuBitableAPI(self.FEISHU_TENANT_ACCESS_TOKEN)

    def get_record_list(self, app_token, table_id, args):
        """
        获取记录列表
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param args: dict, 查询参数
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.get_record_list(app_token, table_id, args)
    
    def get_record_content(self, app_token, table_id, record_id):
        """
        获取单条记录的内容
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param record_id: str, 记录的唯一标识符
        :return: dict, 记录的内容
        """
        return self.feishu_bitable_api.get_record_content(app_token, table_id, record_id)

    def create_record(self, app_token, table_id, fields):
        """
        创建一条新记录
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param fields: dict, 记录的字段内容
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.create_record(app_token, table_id, fields)

    def update_record(self, app_token, table_id, record_id, fields):
        """
        更新一条记录
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param record_id: str, 记录的唯一标识符
        :param fields: dict, 更新的字段内容
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.update_record(app_token, table_id, record_id, fields)

    def delete_record(self, app_token, table_id, record_id):
        """
        删除一条记录
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param record_id: str, 记录的唯一标识符
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.delete_record(app_token, table_id, record_id)

    def batch_create_records(self, app_token, table_id, records, user_id_type="open_id", client_token=None):
        """
        批量创建记录
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param records: list, 记录列表，每条记录是一个字典
        :param user_id_type: str, 用户 ID 类型，默认为 "open_id"
        :param client_token: str, 幂等操作的唯一标识符，默认为 None
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.batch_create_records(app_token, table_id, records, user_id_type, client_token)

    def batch_update_records(self, app_token, table_id, records, user_id_type="open_id"):
        """
        批量更新记录
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param records: list, 记录列表，每条记录是一个字典
        :param user_id_type: str, 用户 ID 类型，默认为 "open_id"
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.batch_update_records(app_token, table_id, records, user_id_type)

    def batch_get_records(self, app_token, table_id, record_ids, user_id_type="open_id", with_shared_url=False, automatic_fields=False):
        """
        批量获取记录
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param record_ids: list, 记录 ID 列表
        :param user_id_type: str, 用户 ID 类型，默认为 "open_id"
        :param with_shared_url: bool, 是否返回记录的分享链接，默认为 False
        :param automatic_fields: bool, 是否返回自动计算的字段，默认为 False
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.batch_get_records(app_token, table_id, record_ids, user_id_type, with_shared_url, automatic_fields)

    def batch_delete_records(self, app_token, table_id, record_ids):
        """
        批量删除记录
        :param app_token: str, 多维表格的唯一标识符
        :param table_id: str, 多维表格数据表的唯一标识符
        :param record_ids: list, 要删除的记录 ID 列表
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.batch_delete_records(app_token, table_id, record_ids)

    def create_bitable(self, name, folder_token=""):
        """
        创建一个新的多维表格
        :param name: str, 表格名称
        :param folder_token: str, 文件夹标识符，默认为空
        :return: dict, API 响应结果
        """
        return self.feishu_bitable_api.create_bitable(name, folder_token)