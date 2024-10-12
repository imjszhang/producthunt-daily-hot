import json
import re
from datetime import datetime, timedelta, timezone
import pytz
from feishu_docx_api_handler import FeishuDocxAPIHandler, BlockType, BlockBatchUpdateRequestBuilder
import os
from dotenv import load_dotenv
#load_dotenv(override=True)

FEISHU_APP_ID = os.getenv('FEISHU_APP_ID')
FEISHU_APP_SECRET= os.getenv('FEISHU_APP_SECRET')
# 初始化 FeishuDocxAPIHandler
feishu_docx_api_handler = FeishuDocxAPIHandler(FEISHU_APP_ID, FEISHU_APP_SECRET)

def batch_modify_document_blocks(document_id, blocks, modifications):
    """
    批量修改文档中的块，根据块的类型选择合适的更新方法
    :param document_id: 文档 ID
    :param blocks: 文档的块信息
    :param modifications: 包含块 ID 和修改内容的字典列表
    :return: 批量更新块的响应
    """
    # 创建批量更新请求构建器
    batch_update_builder = BlockBatchUpdateRequestBuilder()

    # 遍历每个修改项，构建批量更新请求
    for modification in modifications:
        block_id = modification.get("block_id")
        new_content = modification.get("new_content")
        text_style = modification.get("text_style", None)

        # 查找对应的块类型
        block_type = None
        for block in blocks:
            if block.get("block_id") == block_id:
                block_type = block.get("block_type")
                break

        # 根据块类型选择合适的更新方法
        if block_type == BlockType.TEXT.position:
            # 如果是文本块，使用 add_update_text
            print(f"块 {block_id} 是文本块，更新内容为: {new_content}")
            batch_update_builder.add_update_text(block_id, new_content, text_style)
        elif block_type == BlockType.HEADING2.position:
            # 如果是标题块，使用 add_update_text，并可能应用不同的样式
            print(f"块 {block_id} 是标题块，更新内容为: {new_content}")
            batch_update_builder.add_update_text(block_id, new_content, text_style)
        elif block_type == BlockType.BULLET.position:
            # 如果是列表块，使用 add_update_text
            print(f"块 {block_id} 是列表块，更新内容为: {new_content}")
            batch_update_builder.add_update_text(block_id, new_content)
        elif block_type == BlockType.CALLOUT.position:
            # 如果是 callout 块，使用 add_update_text_elements
            print(f"块 {block_id} 是 callout 块，更新内容为: {new_content}")
            batch_update_builder.add_update_text_elements(block_id, new_content)
        else:
            # 其他类型的块，暂时不处理
            print(f"块 {block_id} 的类型 {block_type} 暂不支持更新")

    # 构建批量更新请求
    requests_list = batch_update_builder.build()
    print(f"批量更新请求列表: {requests_list}")

    # 调用批量更新接口
    return feishu_docx_api_handler.batch_update_blocks(document_id, requests_list)



def parse_markdown_to_feishu_docx(content, report_date):
    """
    解析Markdown内容，将其转换为飞书文档日报的记录格式，并组织成指定的日报格式。
    """
    sections = []
    products = content.split('---')  # 每个产品用 "---" 分隔

    for product in products:
        lines = product.strip().splitlines()
        if not lines:
            continue

        section = {}
        content_list = []
        product_website = {}
        product_hunt = {}
        image_url = ""

        for i, line in enumerate(lines):
            if line.startswith('## '):  # 产品名称和链接
                product_name_with_link = line[3:]
                product_name = product_name_with_link.split('](')[0].strip('[')
                product_link = line.split('](')[1].strip(')')
            elif line.startswith('**标语**'):
                slogan = line.split('：', 1)[1].strip()
            elif line.startswith('**介绍**'):
                introduction = line.split('：', 1)[1].strip()
                content_list.append(introduction)
            elif line.startswith('**产品网站**'):
                product_website_url = line.split('](')[1].strip(')')
                product_website = {
                    "text": "立即访问",
                    "url": product_website_url
                }
            elif line.startswith('**Product Hunt**'):
                product_hunt_url = line.split('](')[1].strip(')')
                product_hunt = {
                    "text": "View on Product Hunt",
                    "url": product_hunt_url
                }
            elif line.startswith('![Savvyshot]') or line.startswith('!['):  # 产品图片
                image_url = line.split('(')[1].strip(')')
            elif line.startswith('**关键词**'):
                keywords = line.split('：', 1)[1].strip()
            elif line.startswith('**票数**'):
                votes = int(line.split('🔺')[1].strip())
                content_list.append(f"票数：🔺{votes}")
            elif line.startswith('**是否精选**'):
                featured = '是' if '是' in line else '否'
            elif line.startswith('**发布时间**'):
                raw_date = line.split('：', 1)[1].strip()
                # 使用正则表达式提取日期和时间部分
                date_match = re.search(r'(\d{4}年\d{2}月\d{2}日)\s*(PM|AM)?(\d{2}:\d{2})?', raw_date)
                if date_match:
                    # 提取日期部分
                    date_str = date_match.group(1)
                    time_str = date_match.group(3) if date_match.group(3) else "00:00"  # 如果没有时间，默认是00:00
                    am_pm = date_match.group(2)  # AM/PM 标记

                    # 将日期和时间拼接成完整的字符串
                    full_datetime_str = f"{date_str} {time_str}"
                    
                    # 解析为 datetime 对象
                    parsed_date = datetime.strptime(full_datetime_str, '%Y年%m月%d日 %H:%M')

                    # 如果是 PM 且时间小于 12 点，转换为 24 小时制
                    if am_pm == 'PM' and parsed_date.hour < 12:
                        parsed_date = parsed_date.replace(hour=parsed_date.hour + 12)
                    elif am_pm == 'AM' and parsed_date.hour == 12:
                        # 如果是 AM 且时间是 12 点，转换为 0 点
                        parsed_date = parsed_date.replace(hour=0)

                    # 设置为北京时间 (UTC+8)
                    beijing_tz = pytz.timezone('Asia/Shanghai')
                    localized_date = beijing_tz.localize(parsed_date)

                    # 转换为 UTC 时间戳
                    unix_timestamp = int(localized_date.astimezone(pytz.utc).timestamp())
                    content_list.append(f"发布时间：{unix_timestamp*1000}")  # 需要转换为毫秒
                else:
                    # 如果没有匹配到日期，保留原始的发布时间
                    content_list.append(f"发布时间：{raw_date}")

        # 组装 section
        section['heading'] = product_name + "：" + slogan
        section['content'] = content_list
        section['product_website'] = product_website
        section['product_hunt'] = product_hunt
        section['image_url'] = image_url

        if section:
            sections.append(section)

    # 组装最终的 report_data
    report_data = {
        "title": "每日产品报告",
        "date": report_date,
        "sections": sections
    }

    return report_data


def extract_top_projects_from_report(date_block_id, report_data, block_ids, top_n=3):
    """
    从 parse_markdown_to_feishu_docx 函数的输出中提取内容，并生成飞书文档的修改列表。
    允许通过 top_n 参数指定提取的项目数量，并通过 block_ids 数组为每个项目动态分配 block_id。
    """
    modifications = [
        # 日期块
        {
            "block_name": "日期",
            "block_id": date_block_id,  # 块 ID
            "new_content": [
                {"content": report_data["date"], "text_element_style": {"bold": False}}  # 使用报告中的日期
            ]
        }
    ]
    
    # 项目模板
    project_template = [
        {
            "block_name": "项目 {index}：名字",
            "block_id": "test",  # 块 ID
            "new_content": [
                {"content": "{name}：{tagline}", "text_element_style": {"bold": False}}  # 新的标题内容
            ]
        },
        {
            "block_name": "项目 {index}：票数",
            "block_id": "test",  # 块 ID
            "new_content": [
                {"content": "票数：🔺{votes}", "text_element_style": {"bold": False}}  # 更新票数
            ]
        },
        {
            "block_name": "项目 {index}：描述",
            "block_id": "test",  # 块 ID
            "new_content": [
                {"content": "{description}", "text_element_style": {"bold": False}}  # 更新描述
            ]
        },
        {
            "block_name": "项目 {index}：网址",
            "block_id": "test",  # 块 ID
            "new_content": [
                {"content": "网址：", "text_element_style": {"bold": False}},
                {"content": "查看", "text_element_style": {
                    "bold": False,
                    "link": {"url": "{url}"}  # 更新网址
                }}
            ]
        }
    ]
    
    # 遍历报告中的每个 section，最多提取 top_n 个项目
    for i, section in enumerate(report_data["sections"][:top_n], start=1):
        name, tagline = section["heading"].split("：", 1)  # 提取产品名称和标语
        description = section["content"][0]  # 产品介绍
        votes = section["content"][1].split("🔺")[1]  # 提取票数
        url = section["product_website"]["url"]  # 产品网站链接
        
        
        # 填充每个项目的字段
        for j, template in enumerate(project_template, start=1):
            # 获取当前项目的 block_id
            block_id = block_ids[i - 1][j - 1] if j - 1 < len(block_ids[i - 1]) else "default_block_id"  # 如果 block_ids 不够用，使用默认值            
            filled_template = {
                "block_name": template["block_name"].format(index=i),
                "block_id": block_id,  # 使用动态分配的 block_id
                "new_content": [
                    {
                        "content": template["new_content"][0]["content"].format(
                            index=i, name=name, tagline=tagline, votes=votes, description=description, url=url
                        ),
                        "text_element_style": {"bold": False}
                    }
                ]
            }
            
            # 检查 new_content 列表是否有第二个元素，并且该元素包含 "link"
            if len(template["new_content"]) > 1 and "link" in template["new_content"][1]["text_element_style"]:
                filled_template["new_content"].append({
                    "content": "查看",
                    "text_element_style": {
                        "bold": False,
                        "link": {"url": url}
                    }
                })
            
            modifications.append(filled_template)
    
    return modifications


# 读取本地Markdown文件
def read_markdown_file(file_path):
    """
    从本地文件读取Markdown内容
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 读取并解析 Markdown 文件
def process_markdown_file_for_date(startdate, block_ids, date_block_id, document_id, blocks):
    """
    处理指定日期的 Markdown 文件，生成 report_data 并应用到飞书文档中。
    :param startdate: 开始日期
    :param block_ids: 每个项目的 block_id 列表
    :param date_block_id: 日期块的 block_id
    :param document_id: 飞书文档的 ID
    :param blocks: 文档的块信息
    """
    # 格式化日期
    startdate_str = startdate.strftime('%Y-%m-%d')

    # 获取最新的Markdown文件内容
    file_path = f'data/producthunt-daily-{startdate_str}.md'
    markdown_content = read_markdown_file(file_path)

    # 从Markdown生成report_data
    report_date = startdate_str
    report_data = parse_markdown_to_feishu_docx(markdown_content, report_date)

    # 从report_data生成modifications，提取前3个项目
    modifications = extract_top_projects_from_report(date_block_id, report_data, block_ids)

    # 调用批量修改方法
    batch_modify_document_blocks(document_id, blocks, modifications)


# 处理多个日期的 Markdown 文件
def process_multiple_dates(document_id, blocks, date_block_ids, block_ids_list, days_to_process=0):
    """
    处理多个日期的 Markdown 文件，并将其内容应用到飞书文档中。
    :param document_id: 飞书文档的 ID
    :param blocks: 文档的块信息
    :param date_block_ids: 每个日期对应的块 ID 列表
    :param block_ids_list: 每个项目的 block_id 列表
    :param days_to_process: 要处理的天数
    """
    today = datetime.now(timezone.utc)

    for i in range(3):
        # 获取开始日期
        startdate = today - timedelta(days=i + days_to_process)

        # 获取对应的 block_id
        date_block_id = date_block_ids[i]
        block_ids = block_ids_list[i]

        # 处理指定日期的 Markdown 文件
        process_markdown_file_for_date(startdate, block_ids, date_block_id, document_id, blocks)


# 主函数
def main():

    # 指定要获取的文档 ID
    document_id = "S2mTdzFrToxGSjx4aAgc4fDBnjb"
    document_blocks = feishu_docx_api_handler.get_document_blocks(document_id)
    blocks = document_blocks.get('data', {}).get('items', [])

    # 预定义的 block_id 数组
    date_block_ids = [
        "L2PYd2YnAocH13x5dP0c9S5anGk",  # 第一天的日期块 ID
        "WeNFdCfZhoKb1sx39Fzclvqqnkb",  # 第二天的日期块 ID
        "Pfjhdjay4o54UzxEpZ8cEaU0nwd"   # 第三天的日期块 ID
    ]

    block_ids_list = [
        [
            [
            "DQu8dWOQKoGfH0x07pccVXqBnDc",
            "UPksdUdI0owjGZxVFszcdFQznjf",
            "XWlkdXv1WoDxiXxC6uQcofySnhf",
            "Ih7idClESoKYWcxTq4acaCYPngc"
            ],
            [
            "KjtldZmafoSuOoxRwRccgtmhnth",
            "REyGd1lUxoSDCvxu16icxpmznLf",
            "IM5odauOSotDTdxhRmecW9LlnGf",
            "LjaydEnyto0gtlxmUAPcisGnndh"
            ],
            [
            "Jk98depSKoQHMFxqlxXcCBd0npb",
            "CWGDdSxp9ouLCZxClJacl48anYd",
            "X94IdhD86o0yhTxR8RicNZXZnXe",
            "LbytdSH8Tos9xhx9JrecpOY4nPe"
            ]
        ],
        [
            [
            "LXcPduKZFo99SXxUapicphiYndb",
            "JL2Odru6Mo1kbFx0onvcum4SnGe",
            "DJvjdOIDEoGDSKxoUSzckEcKnGe",
            "OBOcd9274o8oZVxmyuEc9Hqnnqv"
            ],
            [
            "YyvCd7AV6ocMtAxsccGccB54npC",
            "EST7dineBovqT4xQlZWcHzW3nef",
            "AFnOdLAeZoK9RqxzwWYcOimvnOc",
            "DaVqdfopRoduaNxiqjlc7hVWnag"
            ],
            [
            "PUtjdu7guob9e5x3xzAcPYdgnZg",
            "MCmCdjW67oUzrnxl8aAcQhDon8d",
            "KaujdbRHoo9IiVxpgnqcqUebn2e",
            "PjfadZe7koDwYkxIli6cn1j7nHh"
            ]
        ],
        [
            [
            "GygTdXzXHoYoI4xfhmpcoVMknrg",
            "QRMydAKMPo9QPgxpfwvciwPVnde",
            "THIUdjHpDo6MkXxMfLlclkUcnIf",
            "EmW3d7yKVoiDiYxXDSkcCZconSc"
            ],
            [
            "GZsVdwntsovexqxqu92cpUxgn9g",
            "ZbavdPa54o8yrpxJ2Kdc1jiMnPg",
            "S2jDdRFMUottVEx09TgclMDTn9c",
            "Cy3MdaZMQovDAix2uXOco9MLnZs"
            ],
            [
            "XNgHd7N8JoOD3exYtjDci26En7d",
            "VBcpdCnYOoFjCGxgJL8cynVqnRd",
            "VKSud6Hrbogx0MxVEdScA9gnnfe",
            "VtG1dz4euo9zLfxMaOXc4yGAnIg"
            ]
        ]
    ]

    # 处理最近 3 天的 Markdown 文件
    process_multiple_dates(document_id, blocks, date_block_ids, block_ids_list, days_to_process=0)


if __name__ == "__main__":
    main()