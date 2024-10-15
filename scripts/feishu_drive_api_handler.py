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
        response = self.feishu_drive_api.create_folder(folder_name, parent_folder_token)
        if response.get('code') == 0:
            folder_token = response.get('data', {}).get('token')
            return folder_token
        else:
            raise Exception(f"Failed to create folder: {response.get('msg', 'Unknown error')}")

    def get_folder_files(self, folder_token="", page_size=50, page_token=None, order_by="EditedTime", direction="DESC", user_id_type="open_id"):
        """
        Get the list of files in a folder with pagination and sorting options.
        :param folder_token: The token of the folder. If empty, it will fetch files from the root folder.
        :param page_size: The number of files to fetch per page. Default is 50.
        :param page_token: The token for pagination. If None, it will fetch from the beginning.
        :param order_by: The field to order the files by. Default is "EditedTime".
        :param direction: The direction of sorting. Default is "DESC".
        :param user_id_type: The type of user ID. Default is "open_id".
        :return: A tuple containing the list of files and the next page token (if any).
        """
        response = self.feishu_drive_api.get_folder_files(
            folder_token=folder_token,
            page_size=page_size,
            page_token=page_token,
            order_by=order_by,
            direction=direction,
            user_id_type=user_id_type
        )
        
        if response.get('code') == 0:
            files = response.get('data', {}).get('files', [])
            next_page_token = response.get('data', {}).get('page_token')
            return files, next_page_token
        else:
            raise Exception(f"Failed to get folder files: {response.get('msg', 'Unknown error')}")