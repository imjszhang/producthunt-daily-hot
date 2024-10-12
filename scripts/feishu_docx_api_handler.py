#file name: feishu_docx_api_handler.py
from feishu_app_api import FeishuDocxAPI, get_tenant_access_token
from enum import Enum

class BlockType(Enum):
    PAGE = (1, "page")
    TEXT = (2, "text")
    HEADING1 = (3, "heading1")
    HEADING2 = (4, "heading2")
    HEADING3 = (5, "heading3")
    HEADING4 = (6, "heading4")
    HEADING5 = (7, "heading5")
    HEADING6 = (8, "heading6")
    HEADING7 = (9, "heading7")
    HEADING8 = (10, "heading8")
    HEADING9 = (11, "heading9")
    BULLET = (12, "bullet")
    ORDERED = (13, "ordered")
    CODE = (14, "code")
    QUOTE = (15, "quote")
    TODO = (17, "todo")
    BITABLE = (18, "bitable")
    CALLOUT = (19, "callout")
    CHAT_CARD = (20, "chat_card")
    DIAGRAM = (21, "diagram")
    DIVIDER = (22, "divider")
    FILE = (23, "file")
    GRID = (24, "grid")
    GRID_COLUMN = (25, "grid_column")
    IFRAME = (26, "iframe")
    IMAGE = (27, "image")
    ISV = (28, "isv")
    MINDNOTE = (29, "mindnote")
    SHEET = (30, "sheet")
    TABLE = (31, "table")
    TABLE_CELL = (32, "table_cell")
    VIEW = (33, "view")
    UNDEFINED = (34, "undefined")
    QUOTE_CONTAINER = (35, "quote_container")
    TASK = (36, "task")
    OKR = (37, "okr")
    OKR_OBJECTIVE = (38, "okr_objective")
    OKR_KEY_RESULT = (39, "okr_key_result")
    OKR_PROGRESS = (40, "okr_progress")
    ADD_ONS = (41, "add_ons")
    JIRA_ISSUE = (42, "jira_issue")
    WIKI_CATALOG = (43, "wiki_catalog")
    BOARD = (44, "board")
    AGENDA = (45, "agenda")
    AGENDA_ITEM = (46, "agenda_item")
    AGENDA_ITEM_TITLE = (47, "agenda_item_title")
    AGENDA_ITEM_CONTENT = (48, "agenda_item_content")
    LINK_PREVIEW = (49, "link_preview")

    @property
    def position(self):
        return self.value[0]

    @property
    def string_value(self):
        return self.value[1]

    @classmethod
    def get_string_by_position(cls, position):
        for block in cls:
            if block.position == position:
                return block.string_value
        return None


class BlockFactory:
    @staticmethod
    def create_block(block_type: BlockType, text_runs: list, style: dict = None):
        """
        创建一个块，支持多个 text_run
        :param block_type: 块的类型
        :param text_runs: 包含多个 text_run 的列表，每个 text_run 是一个字典，包含 content 和 text_element_style
        :param style: 块的样式
        :return: 块的字典表示
        """
        if style is None:
            style = {}

        # 构建 elements 列表
        elements = []
        for text_run in text_runs:
            content = text_run.get("content", "")
            text_element_style = text_run.get("text_element_style", {})
            elements.append({
                "text_run": {
                    "content": content,
                    "text_element_style": text_element_style
                }
            })

        return {
            "block_type": block_type.position,
            f"{block_type.string_value}": {
                "style": style,
                "elements": elements
            }
        }

    @staticmethod
    def create_divider_block():
        return {
            "block_type": BlockType.DIVIDER.position,
            f"{BlockType.DIVIDER.string_value}": {}
        }

    @staticmethod
    def create_callout_block(content: str, background_color: int = 2, border_color: int = 2, emoji_id: str = "bulb"):
        return {
            "block_type": BlockType.CALLOUT.position,
            f"{BlockType.CALLOUT.string_value}": {
                "background_color": background_color,
                "border_color": border_color,
                "emoji_id": emoji_id,
                "elements": [
                    {
                        "text_run": {
                            "content": content,
                            "text_element_style": {}
                        }
                    }
                ]
            }
        }

    @staticmethod
    def create_quote_container_block(children: list):
        return {
            "block_type": BlockType.QUOTE_CONTAINER.position,
            f"{BlockType.QUOTE_CONTAINER.string_value}": {},
            "children": children
        }

    @staticmethod
    def create_code_block(content: str, language: int = 28, wrap: bool = False):
        return {
            "block_type": BlockType.CODE.position,
            f"{BlockType.CODE.string_value}": {
                "style": {
                    "language": language,
                    "wrap": wrap
                },
                "elements": [
                    {
                        "text_run": {
                            "content": content,
                            "text_element_style": {}
                        }
                    }
                ]
            }
        }

    @staticmethod
    def create_iframe_block(url: str, iframe_type: int = 99):
        return {
            "block_type": BlockType.IFRAME.position,
            f"{BlockType.IFRAME.string_value}": {
                "component": {
                    "iframe_type": iframe_type,
                    "url": url
                }
            }
        }

class BlockBatchUpdateRequestBuilder:
    def __init__(self):
        self.requests = []

    def add_update_text_elements(self, block_id, text_elements):
        """
        添加更新文本元素的请求
        :param block_id: 块的唯一标识
        :param text_elements: 更新后的文本元素列表
        """
        request = {
            "block_id": block_id,
            "update_text_elements": {
                "elements": text_elements
            }
        }
        self.requests.append(request)

    def add_update_text(self, block_id, text_runs, text_style=None):
        """
        添加更新文本内容的请求
        :param block_id: 块的唯一标识
        :param text_runs: 文本内容列表，每个文本内容是一个字典，包含 content 和 text_element_style
        :param text_style: 可选的文本样式
        """
        elements = []
        for text_run in text_runs:
            content = text_run.get("content", "")
            text_element_style = text_run.get("text_element_style", {})
            elements.append({
                "text_run": {
                    "content": content,
                    "text_element_style": text_element_style
                }
            })

        request = {
            "block_id": block_id,
            "update_text_elements": {
                "elements": elements
            }
        }

        if text_style:
            request["update_text_elements"]["style"] = text_style

        self.requests.append(request)

    def add_update_table_property(self, block_id, table_property):
        """
        添加更新表格属性的请求
        :param block_id: 块的唯一标识
        :param table_property: 表格属性
        """
        request = {
            "block_id": block_id,
            "update_table_property": table_property
        }
        self.requests.append(request)

    def add_insert_table_row(self, block_id, row_index, row_data):
        """
        添加插入表格行的请求
        :param block_id: 块的唯一标识
        :param row_index: 插入行的索引
        :param row_data: 插入行的数据
        """
        request = {
            "block_id": block_id,
            "insert_table_row": {
                "row_index": row_index,
                "row_data": row_data
            }
        }
        self.requests.append(request)

    def add_insert_table_column(self, block_id, column_index, column_data):
        """
        添加插入表格列的请求
        :param block_id: 块的唯一标识
        :param column_index: 插入列的索引
        :param column_data: 插入列的数据
        """
        request = {
            "block_id": block_id,
            "insert_table_column": {
                "column_index": column_index,
                "column_data": column_data
            }
        }
        self.requests.append(request)

    def add_delete_table_rows(self, block_id, row_indices):
        """
        添加删除表格行的请求
        :param block_id: 块的唯一标识
        :param row_indices: 要删除的行索引列表
        """
        request = {
            "block_id": block_id,
            "delete_table_rows": {
                "row_indices": row_indices
            }
        }
        self.requests.append(request)

    def add_delete_table_columns(self, block_id, column_indices):
        """
        添加删除表格列的请求
        :param block_id: 块的唯一标识
        :param column_indices: 要删除的列索引列表
        """
        request = {
            "block_id": block_id,
            "delete_table_columns": {
                "column_indices": column_indices
            }
        }
        self.requests.append(request)

    def add_merge_table_cells(self, block_id, cell_ranges):
        """
        添加合并表格单元格的请求
        :param block_id: 块的唯一标识
        :param cell_ranges: 要合并的单元格范围
        """
        request = {
            "block_id": block_id,
            "merge_table_cells": {
                "cell_ranges": cell_ranges
            }
        }
        self.requests.append(request)

    def add_unmerge_table_cells(self, block_id, cell_ranges):
        """
        添加取消合并表格单元格的请求
        :param block_id: 块的唯一标识
        :param cell_ranges: 要取消合并的单元格范围
        """
        request = {
            "block_id": block_id,
            "unmerge_table_cells": {
                "cell_ranges": cell_ranges
            }
        }
        self.requests.append(request)

    def add_replace_image(self, block_id, image_key):
        """
        添加替换图片的请求
        :param block_id: 块的唯一标识
        :param image_key: 新图片的 key
        """
        request = {
            "block_id": block_id,
            "replace_image": {
                "image_key": image_key
            }
        }
        self.requests.append(request)

    def add_replace_file(self, block_id, file_key):
        """
        添加替换文件的请求
        :param block_id: 块的唯一标识
        :param file_key: 新文件的 key
        """
        request = {
            "block_id": block_id,
            "replace_file": {
                "file_key": file_key
            }
        }
        self.requests.append(request)

    def build(self):
        """
        构建最终的批量更新请求
        :return: 批量更新请求列表
        """
        return self.requests

class FeishuDocxAPIHandler:
    def __init__(self, FEISHU_APP_ID, FEISHU_APP_SECRET):
        self.FEISHU_APP_ID = FEISHU_APP_ID
        self.FEISHU_APP_SECRET = FEISHU_APP_SECRET
        self.FEISHU_TENANT_ACCESS_TOKEN = get_tenant_access_token(self.FEISHU_APP_ID, self.FEISHU_APP_SECRET)
        self.feishu_docx_api = FeishuDocxAPI(self.FEISHU_TENANT_ACCESS_TOKEN)

    def get_document_raw_content(self, document_id):
        """
        获取文档的原始内容
        :param document_id: 文档 ID
        :return: 文档的原始内容
        """
        return self.feishu_docx_api.get_document_raw_content(document_id)

    def create_new_document(self, title, folder_token=""):
        """
        创建一个新文档
        :param title: 文档标题
        :param folder_token: 可选的文件夹 token
        :return: 新文档的 document_id
        """
        response = self.feishu_docx_api.create_document(title, folder_token)
        document_id = response.get('data', {}).get('document', {}).get('document_id')
        return document_id

    def get_document_info(self, document_id):
        """
        获取文档的基本信息
        :param document_id: 文档 ID
        :return: 文档的基本信息
        """
        return self.feishu_docx_api.get_document_info(document_id)

    def get_document_blocks(self, document_id):
        """
        获取文档的所有块
        :param document_id: 文档 ID
        :return: 文档的块信息
        """
        return self.feishu_docx_api.get_document_blocks(document_id)

    def get_block_contents(self, document_id, block_id):
        """
        获取某个块的内容
        :param document_id: 文档 ID
        :param block_id: 块 ID
        :return: 块的内容
        """
        return self.feishu_docx_api.get_block_contents(document_id, block_id)

    def get_block_children(self, document_id, block_id):
        """
        获取某个块的子块
        :param document_id: 文档 ID
        :param block_id: 块 ID
        :return: 子块信息
        """
        return self.feishu_docx_api.get_block_children(document_id, block_id)

    def create_block(self, document_id, block_id, children: list, index=-1):
        """
        在文档中创建块
        :param document_id: 文档 ID
        :param block_id: 父块 ID
        :param children: 子块内容
        :param index: 插入位置
        :return: 创建块的响应
        """
        response = self.feishu_docx_api.create_block(document_id, block_id, children, index)
        if response.get('code') == 0:
            print(f"块创建成功: {BlockType.get_string_by_position(children[0]['block_type'])}")
        else:
            print(f"块创建失败: {response.get('msg')}")
        return response

    def update_block(self, document_id, block_id, operation: list):
        """
        更新块的内容
        :param document_id: 文档 ID
        :param block_id: 块 ID
        :param operation: 更新操作的列表
        :return: 更新块的响应
        """
        return self.feishu_docx_api.update_block(document_id, block_id, operation)

    def delete_block(self, document_id, block_id, start_index=0, end_index=1):
        """
        删除块中的子块
        :param document_id: 文档 ID
        :param block_id: 块 ID
        :param start_index: 开始删除的子块索引
        :param end_index: 结束删除的子块索引
        :return: 删除块的响应
        """
        return self.feishu_docx_api.delete_block(document_id, block_id, start_index, end_index)

    def batch_update_blocks(self, document_id, requests_list, document_revision_id=-1, client_token=None, user_id_type="open_id"):
        """
        批量更新文档中的块
        :param document_id: 文档 ID
        :param requests_list: 批量更新块的请求列表，每个请求包含块的更新信息
        :param document_revision_id: 要操作的文档版本，默认为 -1 表示最新版本
        :param client_token: 操作的唯一标识，用于幂等操作
        :param user_id_type: 用户 ID 类型，默认为 "open_id"
        :return: 批量更新块的响应
        """
        response = self.feishu_docx_api.batch_update_blocks(document_id, requests_list, document_revision_id, client_token, user_id_type)
        if response.get('code') == 0:
            print("批量更新成功")
        else:
            print(f"批量更新失败: {response.get('msg')}")
        return response