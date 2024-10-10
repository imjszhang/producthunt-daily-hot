#file name: feishu_bitable_api_handler.py
from feishu_app_api import FeishuBitableAPI, get_tenant_access_token

class FeishuBitableAPIHandler:
    def __init__(self, FEISHU_APP_ID, FEISHU_APP_SECRET):
        self.FEISHU_APP_ID = FEISHU_APP_ID
        self.FEISHU_APP_SECRET = FEISHU_APP_SECRET
        self.FEISHU_TENANT_ACCESS_TOKEN = get_tenant_access_token(self.FEISHU_APP_ID, self.FEISHU_APP_SECRET)
        self.feishu_bitable_api = FeishuBitableAPI(self.FEISHU_TENANT_ACCESS_TOKEN)

    def get_record_list(self, app_token, table_id, args):
        self.__init__()
        return self.feishu_bitable_api.get_record_list(app_token, table_id, args)
    
    def get_record_content(self, app_token, table_id, record_id):
        self.__init__()
        return self.feishu_bitable_api.get_record_content(app_token, table_id, record_id)

    def update_record(self, app_token, table_id, record_id, fields):
        self.__init__()
        return self.feishu_bitable_api.update_record(app_token, table_id, record_id, fields)