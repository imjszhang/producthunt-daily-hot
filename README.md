# Product Hunt 每日中文热榜 - 每天自动同步到飞书和博客

[English](README.en.md) | [中文](README.md)

![License](https://img.shields.io/github/license/ViggoZ/producthunt-daily-hot) ![Python](https://img.shields.io/badge/python-3.x-blue)

Product Hunt 每日热榜是一个基于 GitHub Action 的自动化工具，它能够每天定时生成 Product Hunt 上的热门产品榜单 Markdown 文件，并自动提交到 GitHub 仓库中。该项目旨在帮助用户快速查看每日的 Product Hunt 热门榜单，并提供更详细的产品信息。

在原项目基础上,增加了自动更新到飞书的功能, 以及支持调用Dify的API来替代OPENAI的API。


榜单会在每天下午3点自动更新，可以在 [🌐 这里查看](https://sxwqam5d2bh.feishu.cn/docx/S2mTdzFrToxGSjx4aAgc4fDBnjb?from=from_copylink)。

## 预览
![Preview](./preview_feishu_wiki.gif)
![Preview](./preview_feishu_bitable.gif)
![Preview](./preview.gif)

## 功能概述

- **自动获取数据**：每天自动获取前一天的 Product Hunt Top 30 产品数据。
- **关键词生成**：生成简洁易懂的中文关键词，帮助用户更好地理解产品内容。
- **高质量翻译**：使用 OpenAI 的 GPT-4 模型对产品描述进行高质量翻译。
- **Markdown 文件生成**：生成包含产品数据、关键词和翻译描述的 Markdown 文件，方便在网站或其他平台上发布。
- **每日自动化**：通过 GitHub Actions 自动生成并提交每日的 Markdown 文件。
- **可配置工作流**：支持手动触发或通过 GitHub Actions 定时生成内容。
- **灵活定制**：脚本易于扩展或修改，可以包括额外的产品细节或调整文件格式。
- **自动发布到 WordPress**：生成的 Markdown 文件可以自动发布到 WordPress 网站。
- **自动更新到飞书多维表格**：生成的 Markdown 文件可以自动更新到飞书多维表格。
- **自动生成飞书文档**：生成文件到指定飞书文件夹。
- **自动生成飞书文档简报**：生成简报在指定的飞书文档里，实现了自动更新飞书知识库。

## 快速开始

### 前置条件

- Python 3.x
- GitHub 账户及仓库
- OpenAI API Key 或者 Dify的API
- Product Hunt API 凭证
- WordPress 网站及凭证（用于自动发布）

### 安装

1. **克隆仓库：**

```bash
git clone https://github.com/imjszhang/producthunt-daily-hot.git
cd producthunt-daily-hot
```

2. **安装 Python 依赖：**

确保您的系统已安装 Python 3.x。然后安装所需的依赖包：

```bash
pip install -r requirements.txt
```

### 设置

1. **GitHub Secrets：**

   在您的 GitHub 仓库中添加以下 Secrets：

   - `OPENAI_API_KEY`: OpenAI API 密钥。
   - `DIFY_API_BASE_URL`: DIFY API 的网址 URL。
   - `DIFY_API_KEY`: DIFY API 密钥。
   - `PRODUCTHUNT_CLIENT_ID`: Product Hunt API 客户端 ID。
   - `PRODUCTHUNT_CLIENT_SECRET`: Product Hunt API 客户端密钥。
   - `PAT`: 用于推送更改到仓库的个人访问令牌。
   - `WORDPRESS_URL`: WordPress 网站 URL。
   - `WORDPRESS_USERNAME`: WordPress 用户名。
   - `WORDPRESS_PASSWORD`: WordPress 密码。
   - `FEISHU_APP_ID`: 飞书应用的 App
   - `FEISHU_APP_SECRET`: 飞书应用的 Secret
   - `FEISHU_BITABLE_APP_TOKEN`: 飞书多维表格的APP Token
   - `FEISHU_BITABLE_TABLE_ID`: 飞书多维表格的TABLE ID
   - `FEISHU_DOCX_FOLDER_TOKEN`: 飞书文件夹的TOKEN ID


2. **GitHub Actions 工作流：**

   工作流定义在 `.github/workflows/` 中。
   - `generate_markdown.yml`：生成 Product Hunt 每日热门产品的 Markdown 文件。该工作流每天 UTC 时间 07:01（北京时间 15:01）自动运行，也可以手动触发。
   - `publish_to_wordpress.yml`：自动发布 Markdown 文件到 WordPress 网站。在generate_markdown之后触发，可在里面配置是否启用。
   - `publish_to_feishubitable.yml`：自动发布到飞书多维表格。在generate_markdown之后触发，可在里面配置是否启用。processed_records.json里已存在产品将不会重复发布。
   - `publish_to_feishudocx.yml`：自动创建飞书文档，发布到飞书文件夹里。在generate_markdown之后触发，可在里面配置是否启用。
   - `update_feishudocx_template.yml`：自动在指定飞书文档里生成简报。在generate_markdown之后触发，可在里面配置是否启用。   
### 使用

设置完成后，GitHub Action 将自动生成并提交包含 Product Hunt 每日热门产品的 Markdown 文件，并自动发布到 WordPress 网站和飞书多维表格。文件存储在 `data/` 目录下。

### 自定义

- 您可以修改 `scripts/product_hunt_list_to_md.py` 文件来自定义生成文件的格式或添加额外内容。这个是openai的API的版本。
- 您可以修改 `scripts/product_hunt_list_to_md_dify.py` 文件来自定义生成文件的格式或添加额外内容。这个是dify的API的版本。
- 如果需要，可以在 `.github/workflows/generate_markdown.yml` 中调整定时任务的运行时间。

### 示例输出

生成的文件存储在 `data/` 目录下。每个文件以 `PH-daily-YYYY-MM-DD.md` 的格式命名。

### 贡献

欢迎任何形式的贡献！如有任何改进或新功能的建议，请提交 issue 或 pull request。

### 许可证

本项目基于 MIT 许可证开源 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。
