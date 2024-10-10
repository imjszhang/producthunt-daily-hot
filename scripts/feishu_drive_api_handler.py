#file name: feishu_drive_api_handler.py
from feishu_app_api import FeishuDriveAPI, get_tenant_access_token


class FeishuDriveAPIHandler:
    def __init__(self, FEISHU_APP_ID, FEISHU_APP_SECRET):
        self.FEISHU_APP_ID = FEISHU_APP_ID
        self.FEISHU_APP_SECRET = FEISHU_APP_SECRET
        self.FEISHU_TENANT_ACCESS_TOKEN = get_tenant_access_token(self.FEISHU_APP_ID, self.FEISHU_APP_SECRET)
        self.feishu_drive_api = FeishuDriveAPI(self.FEISHU_TENANT_ACCESS_TOKEN)

    def create_new_folder(self, folder_name, parent_folder_token=""):
        """
        Create a new folder in Feishu Drive.
        :param folder_name: The name of the new folder.
        :param parent_folder_token: Optional parent folder token where the folder will be created.
        :return: The folder token of the newly created folder.
        """
        self.__init__()
        response = self.feishu_drive_api.create_folder(folder_name, parent_folder_token)
        folder_token = response.get('data', {}).get('token')
        return folder_token

    def get_folder_files(self, folder_token):
        """
        Get the list of files in a folder.
        :param folder_token: The token of the folder.
        :return: The list of files in the folder.
        """
        self.__init__()
        response = self.feishu_drive_api.get_folder_files(folder_token)
        return response.get('data', {}).get('files', [])