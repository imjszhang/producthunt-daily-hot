import os
import aiohttp
import asyncio
import json
import re
from datetime import datetime, timezone
import pytz  # 用于处理时区
from dotenv import load_dotenv
from urllib.parse import unquote  # 用于解码 URL
import ssl

# 定义一个全局的信号量，限制并发请求数量
semaphore = asyncio.Semaphore(5)  # 限制并发请求数量为 5

PROCESSED_RECORDS_LOG = 'processed_records.json'

def load_processed_records():
    """
    从日志文件中加载已处理的记录。
    """
    if os.path.exists(PROCESSED_RECORDS_LOG):
        with open(PROCESSED_RECORDS_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_processed_record(file_name, record_name):
    """
    将已处理的记录保存到日志文件中。
    """
    processed_records = load_processed_records()
    if file_name not in processed_records:
        processed_records[file_name] = []
    processed_records[file_name].append(record_name)

    with open(PROCESSED_RECORDS_LOG, 'w', encoding='utf-8') as f:
        json.dump(processed_records, f, ensure_ascii=False, indent=4)

async def get_tenant_access_token(app_id, app_secret):
    url = f"https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "app_id": app_id,
        "app_secret": app_secret,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            response_data = await response.json()
            return response_data.get("tenant_access_token")

async def upload_image_to_feishu(api_key, image_url, file_name, app_token, retries=3):
    async with semaphore:  # 使用信号量限制并发
        print(f"Uploading image from URL: {image_url}")
        url = "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        # 解码 URL，防止特殊字符问题
        image_url = unquote(image_url)
        
        # 创建一个不验证 SSL 的上下文
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # 下载图片
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(image_url, ssl=ssl_context) as image_response:
                    image_data = await image_response.read()
            except aiohttp.client_exceptions.InvalidURL as e:
                print(f"Invalid URL: {image_url}")
                return None
        
        # 构建上传请求
        data = aiohttp.FormData()
        data.add_field('file_name', file_name)
        data.add_field('parent_type', 'bitable_image')
        data.add_field('parent_node', app_token)
        data.add_field('file', image_data, filename=file_name)
        data.add_field("size", str(len(image_data)))  # 如果需要 size，可以将其转换为字符串

        # 上传图片，带有重试机制
        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, data=data, ssl=ssl_context) as response:
                        # 打印响应的内容类型和状态码
                        print(f"Response status: {response.status}")
                        print(f"Response content-type: {response.headers.get('Content-Type')}")

                        # 尝试解析为 JSON
                        try:
                            response_data = await response.json()
                        except aiohttp.ContentTypeError:
                            # 如果不是 JSON 响应，打印原始的响应内容
                            response_text = await response.text()
                            print(f"Non-JSON response: {response_text}")
                            return None

                        if response_data.get('code') == 0:
                            return response_data['data']['file_token']
                        else:
                            print(f"Failed to upload image: {response_data}")
                            return None
            except aiohttp.ClientResponseError as e:
                if e.status == 429:  # 429 表示频率限制
                    retry_after = int(e.headers.get("Retry-After", 1))  # 获取重试等待时间
                    print(f"Rate limit hit, retrying after {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    raise  # 其他错误直接抛出
        print(f"Failed to upload image after {retries} attempts")
        return None

async def create_record_with_image(api_key, app_token, table_id, fields, file_token, retries=3):
    async with semaphore:  # 使用信号量限制并发
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 将 file_token 添加到 fields 中的附件字段
        fields['附件'] = [{"file_token": file_token}]
        
        payload = {
            "fields": fields,
        }

        # 创建记录，带有重试机制
        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=payload) as response:
                        return await response.json()
            except aiohttp.ClientResponseError as e:
                if e.status == 429:  # 429 表示频率限制
                    retry_after = int(e.headers.get("Retry-After", 1))  # 获取重试等待时间
                    print(f"Rate limit hit, retrying after {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    raise  # 其他错误直接抛出
        print(f"Failed to create record after {retries} attempts")
        return None

def parse_markdown_to_records(content):
    """
    解析Markdown内容，将其转换为飞书多维表格的记录格式。
    """
    records = []
    products = content.split('---')  # 每个产品用 "---" 分隔

    for product in products:
        lines = product.strip().splitlines()
        if not lines:
            continue

        record = {}
        for i, line in enumerate(lines):
            if line.startswith('## '):  # 产品名称和链接
                product_name_with_link = line[3:]
                product_name = re.sub(r'^\[\d+\.\s*', '[', product_name_with_link)  # 去掉序号
                product_name = product_name.split('](')[0].strip('[')
                product_link = line.split('](')[1].strip(')')
                record['产品名称'] = product_name
                record['产品链接'] = product_link
            elif line.startswith('**标语**'):
                record['标语'] = line.split('：', 1)[1].strip()
            elif line.startswith('**介绍**'):
                record['介绍'] = line.split('：', 1)[1].strip()
            elif line.startswith('**产品网站**'):
                record['产品网站'] = line.split('](')[1].strip(')')
            elif line.startswith('**Product Hunt**'):
                record['Product Hunt 链接'] = line.split('](')[1].strip(')')
            elif line.startswith('![Savvyshot]') or line.startswith('!['):  # 产品图片
                record['产品图片'] = line.split('(')[1].strip(')')
                print(f"Extracted image URL: {record['产品图片']}")  # 添加调试信息
            elif line.startswith('**关键词**'):
                record['关键词'] = line.split('：', 1)[1].strip()
            elif line.startswith('**票数**'):
                record['票数'] = int(line.split('🔺')[1].strip())
            elif line.startswith('**是否精选**'):
                record['是否精选'] = '是' if '是' in line else '否'
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
                    record['发布时间'] = unix_timestamp*1000  # 需要转换为毫秒
                else:
                    # 如果没有匹配到日期，保留原始的发布时间
                    record['发布时间'] = raw_date

        if record:
            records.append(record)

    return records

async def process_record(feishu_api_key, app_token, table_id, record, file_name=""):
    # 上传图片并获取 file_token
    image_url = record.get('产品图片')
    if image_url:
        file_token = await upload_image_to_feishu(feishu_api_key, image_url, "product_image.jpeg", app_token)
        if file_token:
            response = await create_record_with_image(feishu_api_key, app_token, table_id, record, file_token)
            if response.get('code') == 0:
                print(f"Record created successfully: {record['产品名称']}")
                # 记录已处理的记录
                save_processed_record(file_name, record['产品名称'])
            else:
                print(f"Failed to create record: {response}")
        else:
            print(f"Failed to upload image for product: {record['产品名称']}")
    else:
        print(f"No image found for product: {record['产品名称']}")


async def publish_to_feishu_bitable():
    """
    处理今天的 Markdown 文件并将其内容发布到飞书多维表格。
    """
    # 从环境变量中获取飞书 API 相关信息
    load_dotenv(override=True)
    FEISHU_APP_ID = os.getenv('FEISHU_APP_ID')
    FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET')    
    feishu_api_key = await get_tenant_access_token(FEISHU_APP_ID, FEISHU_APP_SECRET)
    app_token = os.getenv('FEISHU_BITABLE_APP_TOKEN')
    table_id = os.getenv('FEISHU_BITABLE_TABLE_ID')

    # 获取今天的日期并格式化
    today = datetime.now(timezone.utc)
    date_today = today.strftime('%Y-%m-%d')

    # 获取最新的Markdown文件内容
    file_name = f'data/producthunt-daily-{date_today}.md'

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_name}")
        return

    # 解析Markdown内容为飞书多维表格的记录
    records = parse_markdown_to_records(content)

    # 加载已处理的记录
    processed_records = load_processed_records().get(file_name, [])

    # 创建异步任务列表
    tasks = []
    for record in records:
        # 检查该记录是否已经处理过
        if record['产品名称'] in processed_records:
            print(f"Skipping already processed record: {record['产品名称']}")
            continue  # 跳过已处理的记录

        # 如果没有处理过，则添加到任务列表中
        tasks.append(process_record(feishu_api_key, app_token, table_id, record, file_name))

    # 并发执行所有任务
    await asyncio.gather(*tasks)


async def publish_to_feishu_bitable_by_path(file_path):
    """
    处理单个 Markdown 文件并将其内容发布到飞书多维表格。
    :param file_path: Markdown 文件的路径
    """
    # 从环境变量中获取飞书 API 相关信息
    load_dotenv(override=True)
    FEISHU_APP_ID = os.getenv('FEISHU_APP_ID')
    FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET')    
    feishu_api_key = await get_tenant_access_token(FEISHU_APP_ID, FEISHU_APP_SECRET)
    app_token = os.getenv('FEISHU_BITABLE_APP_TOKEN')
    table_id = os.getenv('FEISHU_BITABLE_TABLE_ID')

    # 读取指定的Markdown文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return

    # 解析Markdown内容为飞书多维表格的记录
    records = parse_markdown_to_records(content)

    # 加载已处理的记录
    processed_records = load_processed_records().get(os.path.basename(file_path), [])

    # 创建异步任务列表
    for record in records:
        if record['产品名称'] in processed_records:
            print(f"Skipping already processed record: {record['产品名称']}")
            continue  # 跳过已处理的记录

        await process_record(feishu_api_key, app_token, table_id, record, os.path.basename(file_path))

async def process_all_markdown_files():
    """
    批量处理 data 文件夹中的所有 Markdown 文件，按顺序一个文件处理完成后再处理下一个。
    如果中断，下次运行时会跳过已处理的文件和记录。
    """
    # 获取 data 文件夹中的所有 Markdown 文件
    data_folder = 'data'
    markdown_files = [f for f in os.listdir(data_folder) if f.endswith('.md')]

    if not markdown_files:
        print(f"No markdown files found in {data_folder}")
        return

    # 顺序处理每个文件
    for file_name in markdown_files:
        file_path = os.path.join(data_folder, file_name)
        print(f"Processing file: {file_path}")
        await publish_to_feishu_bitable_by_path(file_path)  # 顺序执行，等待一个文件处理完成后再处理下一个

if __name__ == "__main__":
    # 单独处理今天的 Markdown 文件
    asyncio.run(publish_to_feishu_bitable())


    # 如果需要批量处理所有 Markdown 文件，可以取消注释以下行
    #asyncio.run(process_all_markdown_files())