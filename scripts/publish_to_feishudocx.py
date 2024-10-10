import json
import re
from datetime import datetime, timedelta, timezone
import pytz
from feishu_docx_api_handler import FeishuDocxAPIHandler, BlockType, BlockFactory
import os
from dotenv import load_dotenv
load_dotenv(override=True)

FEISHU_APP_ID = os.getenv('FEISHU_APP_ID')
FEISHU_APP_SECRET= os.getenv('FEISHU_APP_SECRET')

def parse_markdown_to_feishu_docx(content, report_title, report_date):
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
                product_name = product_name_with_link #re.sub(r'^\[\d+\.\s*', '[', product_name_with_link)  # 去掉序号
                product_name = product_name.split('](')[0].strip('[')
                product_link = line.split('](')[1].strip(')')                
            elif line.startswith('**标语**'):
                slogan = line.split('：', 1)[1].strip()
                #content_list.append(slogan)
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
                #content_list.append(f"分类：{keywords}")
            elif line.startswith('**票数**'):
                votes = int(line.split('🔺')[1].strip())
                content_list.append(f"票数：🔺{votes}")
            elif line.startswith('**是否精选**'):
                featured = '是' if '是' in line else '否'
                #content_list.append(f"是否精选：{featured}")
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
                    #content_list.append(f"发布时间：{unix_timestamp*1000}")  # 需要转换为毫秒
                    content_list.append(f"发布时间：{raw_date}")
                else:
                    # 如果没有匹配到日期，保留原始的发布时间
                    content_list.append(f"发布时间：{raw_date}")

        # 组装 section
        section['heading'] = product_name+"："+slogan
        section['content'] = content_list
        section['product_website'] = product_website
        section['product_hunt'] = product_hunt
        section['image_url'] = image_url

        if section:
            sections.append(section)

    # 组装最终的 report_data
    report_data = {
        "title": report_title,
        "date": report_date,
        "sections": sections
    }

    return report_data

class DailyReportGenerator:
    def __init__(self, feishu_docx_api_handler: FeishuDocxAPIHandler):
        self.feishu_docx_api_handler = feishu_docx_api_handler

    def generate_report(self, document_id: str, parent_block_id: str, report_data: dict):
        """
        生成日报
        :param document_id: 文档 ID
        :param parent_block_id: 父块 ID
        :param report_data: 日报数据
        """
        # 创建标题块 (HEADING1)
        title_block = BlockFactory.create_block(
            BlockType.HEADING1, 
            [{"content": report_data["title"], "text_element_style": {"bold": True}}],
            style={"align": 1}
        )
        self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [title_block])

        # 创建日期块 (TEXT)
        date_block = BlockFactory.create_block(
            BlockType.TEXT, 
            [{"content": f"日期: {report_data['date']}"}],
            style={"align": 1}
        )
        #self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [date_block])

        # 创建分割线块 (DIVIDER)
        divider_block = BlockFactory.create_divider_block()
        self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [divider_block])

        # 创建各个部分的块
        for section in report_data["sections"]:
            # 创建每个部分的标题 (HEADING2)
            section_heading_block = BlockFactory.create_block(
                BlockType.HEADING2, 
                [{"content": section["heading"]}],
                style={"align": 1}
            )
            self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [section_heading_block])

            # 创建每个部分的内容（无序列表）(BULLET)
            for content in section["content"]:
                content_block = BlockFactory.create_block(
                    BlockType.BULLET, 
                    [{"content": content}],
                    style={"align": 1}
                )
                self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [content_block])

            # 添加产品网站链接块 (TEXT + LINK)
            if "product_website" in section:
                product_website_block = BlockFactory.create_block(
                    BlockType.TEXT, 
                    [{"content": f"产品网站："}]
                )
                self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [product_website_block])

                # 创建链接(LINK)
                link_preview_block = BlockFactory.create_block(
                    BlockType.TEXT, 
                    [{"content": f"{section['product_website']['text']}",
                      "text_element_style": {"link": {"url": section['product_website']['url']}}}]
                )
                self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [link_preview_block])

            # 添加Product Hunt链接块 (TEXT + LINK)
            if "product_hunt" in section:
                product_hunt_block = BlockFactory.create_block(
                    BlockType.TEXT, 
                    [{"content": f"Product Hunt："}]
                )
                self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [product_hunt_block])

                # 创建链接预览块 (LINK)
                link_preview_block = BlockFactory.create_block(
                    BlockType.TEXT, 
                    [{"content": f"{section['product_hunt']['text']}",
                      "text_element_style": {"link": {"url": section['product_hunt']['url']}}}]
                )
                self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [link_preview_block])

            # 创建图片块 (IFRAME)
            if "image_url" in section:
                image_block = BlockFactory.create_iframe_block(section["image_url"])
                self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [image_block])

            # 添加分割线块 (DIVIDER)
            self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [divider_block])

        # 添加最后的分割线块 (DIVIDER)
        self.feishu_docx_api_handler.create_block(document_id, parent_block_id, [divider_block])

#根据日期，创建一个日报
def generate_daily_report(date_today):
    # 初始化 FeishuDocxAPIHandler
    feishu_docx_api_handler = FeishuDocxAPIHandler(FEISHU_APP_ID, FEISHU_APP_SECRET)
    # 创建一个新文档
    folder_token = os.getenv('FEISHU_DOCX_FOLDER_TOKEN')
    new_document_title = f"producthunt-daily-{date_today}"
    new_document_id = feishu_docx_api_handler.create_new_document(new_document_title, folder_token=folder_token)

    if new_document_id:
        print(f"新文档已创建，文档 ID 为: {new_document_id}")

        # 获取根块 ID
        root_block_id = new_document_id  # 根块的 block_id 通常与 document_id 相同

       # 获取最新的Markdown文件内容
        file_path = f'data/producthunt-daily-{date_today}.md'

        # 读取指定的Markdown文件内容
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return None

        # 日报数据
        if markdown_content:
            report_title = f"PH今日热榜 | {date_today}"
            report_date = f"{date_today}"
            report_data = parse_markdown_to_feishu_docx(markdown_content, report_title, report_date)
            #print(report_data)

        # 创建日报生成器
        report_generator = DailyReportGenerator(feishu_docx_api_handler)

        # 生成日报
        report_generator.generate_report(new_document_id, root_block_id, report_data)
        print(f"{date_today}日报文档已创建。")
        return new_document_id
    else:
        print(f"{date_today}日报文档创建失败。")
        return None

import logging

# 配置日志记录
logging.basicConfig(filename='daily_report_errors.log', level=logging.ERROR)

#生成从某一天开始往前多少天的日报
def generate_daily_reports(start_date, days):
    for i in range(days):
        date_today = (start_date - timedelta(days=i)).strftime('%Y-%m-%d')
        try:
            generate_daily_report(date_today)
        except Exception as e:
            # 捕获所有异常并记录错误信息到日志文件
            logging.error(f"Error occurred while generating report for {date_today}: {str(e)}", exc_info=True)
            continue  # 继续处理下一天的日报

# 主函数
def main():
    # 获取今天的日期并格式化
    today = datetime.now(timezone.utc)
    date_today = today.strftime('%Y-%m-%d')

    # 生成今天的日报
    #generate_daily_report(date_today)

    
    startdate= today - timedelta(days=5)
    
    #生成往前60天的日报
    generate_daily_reports(startdate, 60)


if __name__ == "__main__":
    main()