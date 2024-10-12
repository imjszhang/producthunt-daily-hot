# Product Hunt Daily Hot List - Automatically Sync to Feishu and Blog Every Day

[English](README.en.md) | [中文](README.md)

![License](https://img.shields.io/github/license/ViggoZ/producthunt-daily-hot) ![Python](https://img.shields.io/badge/python-3.x-blue)

The Product Hunt Daily Hot List is an automation tool based on GitHub Action. It automatically generates a Markdown file of the top trending products on Product Hunt every day and submits it to a GitHub repository. This project aims to help users quickly view the daily Product Hunt hot list and provide more detailed product information.

On top of the original project, features have been added to automatically update to Feishu and support calling Dify's API as a replacement for the OpenAI API.

The list is automatically updated every day at 3 PM, and you can view it [🌐 here](https://sxwqam5d2bh.feishu.cn/docx/S2mTdzFrToxGSjx4aAgc4fDBnjb?from=from_copylink).

## Preview
![Preview](./preview_feishu_wiki.gif)
![Preview](./preview_feishu_bitable.gif)
![Preview](./preview.gif)

## Features Overview

- **Automatic Data Retrieval**: Automatically fetches the top 30 products from Product Hunt every day.
- **Keyword Generation**: Generates concise and easy-to-understand Chinese keywords to help users better understand the product content.
- **High-Quality Translation**: Uses OpenAI's GPT-4 model to provide high-quality translations of product descriptions.
- **Markdown File Generation**: Generates a Markdown file containing product data, keywords, and translated descriptions, making it easy to publish on websites or other platforms.
- **Daily Automation**: Automatically generates and submits the daily Markdown file via GitHub Actions.
- **Configurable Workflow**: Supports manual triggers or scheduled content generation via GitHub Actions.
- **Flexible Customization**: The script is easy to extend or modify, allowing for additional product details or adjustments to the file format.
- **Automatic Publishing to WordPress**: The generated Markdown file can be automatically published to a WordPress site.
- **Automatic Update to Feishu Bitable**: The generated Markdown file can be automatically updated to Feishu Bitable.
- **Automatic Feishu Document Generation**: Generates files in a specified Feishu folder.
- **Automatic Feishu Document Briefing**: Generates a briefing in a specified Feishu document, enabling automatic updates to the Feishu knowledge base.

## Quick Start

### Prerequisites

- Python 3.x
- GitHub account and repository
- OpenAI API Key or Dify API
- Product Hunt API credentials
- WordPress site and credentials (for automatic publishing)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/imjszhang/producthunt-daily-hot.git
cd producthunt-daily-hot
```

2. **Install Python dependencies:**

Ensure that Python 3.x is installed on your system. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Setup

1. **GitHub Secrets:**

   Add the following secrets to your GitHub repository:

   - `OPENAI_API_KEY`: OpenAI API key.
   - `DIFY_API_BASE_URL`: Dify API base URL.
   - `DIFY_API_KEY`: Dify API key.
   - `PRODUCTHUNT_CLIENT_ID`: Product Hunt API client ID.
   - `PRODUCTHUNT_CLIENT_SECRET`: Product Hunt API client secret.
   - `PAT`: Personal access token for pushing changes to the repository.
   - `WORDPRESS_URL`: WordPress site URL.
   - `WORDPRESS_USERNAME`: WordPress username.
   - `WORDPRESS_PASSWORD`: WordPress password.
   - `FEISHU_APP_ID`: Feishu app ID.
   - `FEISHU_APP_SECRET`: Feishu app secret.
   - `FEISHU_BITABLE_APP_TOKEN`: Feishu Bitable app token.
   - `FEISHU_BITABLE_TABLE_ID`: Feishu Bitable table ID.
   - `FEISHU_DOCX_FOLDER_TOKEN`: Feishu folder token ID.

2. **GitHub Actions Workflow:**

   The workflows are defined in the `.github/workflows/` directory.
   - `generate_markdown.yml`: Generates the Product Hunt daily hot product Markdown file. This workflow runs automatically every day at 07:01 UTC (15:01 Beijing time) and can also be triggered manually.
   - `publish_to_wordpress.yml`: Automatically publishes the Markdown file to a WordPress site. It is triggered after `generate_markdown` and can be configured to enable or disable it.
   - `publish_to_feishubitable.yml`: Automatically publishes to Feishu Bitable. It is triggered after `generate_markdown` and can be configured to enable or disable it. Products already present in `processed_records.json` will not be published again.
   - `publish_to_feishudocx.yml`: Automatically creates a Feishu document and publishes it to a Feishu folder. It is triggered after `generate_markdown` and can be configured to enable or disable it.
   - `update_feishudocx_template.yml`: Automatically generates a briefing in a specified Feishu document. It is triggered after `generate_markdown` and can be configured to enable or disable it.

### Usage

Once set up, GitHub Action will automatically generate and submit a Markdown file containing the daily trending products from Product Hunt and automatically publish it to the WordPress site and Feishu Bitable. The files are stored in the `data/` directory.

### Customization

- You can modify the `scripts/product_hunt_list_to_md.py` file to customize the format of the generated file or add additional content. This version uses the OpenAI API.
- You can modify the `scripts/product_hunt_list_to_md_dify.py` file to customize the format of the generated file or add additional content. This version uses the Dify API.
- If needed, you can adjust the scheduled task's runtime in `.github/workflows/generate_markdown.yml`.

### Example Output

The generated files are stored in the `data/` directory. Each file is named in the format `PH-daily-YYYY-MM-DD.md`.

### Contribution

Any form of contribution is welcome! If you have any suggestions for improvements or new features, please submit an issue or pull request.

### License

This project is open-sourced under the MIT License - for more details, please refer to the [LICENSE](LICENSE) file.

