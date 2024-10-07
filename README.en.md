# Product Hunt Daily Hot List - Auto Update to Feishu Bitable

[English](README.en.md) | [中文](README.md)

![License](https://img.shields.io/github/license/ViggoZ/producthunt-daily-hot) ![Python](https://img.shields.io/badge/python-3.x-blue)

Product Hunt Daily Hot is a GitHub Action-based automation tool that generates a daily Markdown file summarizing the top products from Product Hunt and automatically commits it to a GitHub repository. The project aims to help users quickly view the daily Product Hunt leaderboard and provide more detailed product information.

In this enhanced version, we have added the ability to automatically update the data to Feishu Bitable and support for using Dify's API as an alternative to OpenAI's API.

The leaderboard is automatically updated daily at 3:00 PM Beijing Time. You can view it [🌐 here](https://decohack.com/category/producthunt/).

## Preview

![Preview](./preview.gif)

## Features

- **Automated Data Retrieval**: Automatically retrieves the top 30 products from Product Hunt from the previous day.
- **Keyword Generation**: Generates easy-to-understand Chinese keywords to help users better understand the product content.
- **High-Quality Translation**: Uses OpenAI's GPT-4 model for high-quality translations of product descriptions.
- **Markdown File Generation**: Generates Markdown files containing product data, keywords, and translated descriptions, which can be easily published on websites or other platforms.
- **Daily Automation**: Automatically generates and commits the daily Markdown file via GitHub Actions.
- **Configurable Workflow**: Supports manual triggering or scheduled generation via GitHub Actions.
- **Flexible Customization**: The script is easy to extend or modify to include additional product details or adjust the file format.
- **Automatic Publishing to WordPress**: The generated Markdown files can be automatically published to a WordPress website.
- **Automatic Update to Feishu Bitable**: The generated Markdown files can be automatically updated to Feishu Bitable.

## Getting Started

### Prerequisites

- Python 3.x
- GitHub account and repository
- OpenAI API Key or Dify API
- Product Hunt API credentials
- WordPress website and credentials (for automatic publishing)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/imjszhang/producthunt-daily-hot.git
cd producthunt-daily-hot
```

2. **Install Python dependencies:**

Ensure you have Python 3.x installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### Setup

1. **GitHub Secrets:**

   Add the following secrets to your GitHub repository:

   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `DIFY_API_BASE_URL`: The base URL for the Dify API.
   - `DIFY_API_KEY`: Your Dify API key.
   - `PRODUCTHUNT_CLIENT_ID`: Your Product Hunt API client ID.
   - `PRODUCTHUNT_CLIENT_SECRET`: Your Product Hunt API client secret.
   - `PAT`: Personal Access Token for pushing changes to the repository.
   - `WORDPRESS_URL`: Your WordPress website URL.
   - `WORDPRESS_USERNAME`: Your WordPress username.
   - `WORDPRESS_PASSWORD`: Your WordPress password.
   - `FEISHU_APP_ID`: Feishu App ID.
   - `FEISHU_APP_SECRET`: Feishu App Secret.
   - `FEISHU_BITABLE_APP_TOKEN`: Feishu Bitable App Token.
   - `FEISHU_BITABLE_TABLE_ID`: Feishu Bitable Table ID.

2. **GitHub Actions Workflow:**

   The workflows are defined in `.github/workflows/`:
   - `generate_markdown.yml`: Generates the Product Hunt daily hot list in Markdown format. This workflow runs daily at 07:01 UTC (15:01 Beijing Time) and can also be manually triggered.
   - `publish_to_wordpress.yml`: Automatically publishes the Markdown file to a WordPress website. This runs after `generate_markdown` and can be configured to enable or disable publishing.
   - `publish_to_feishubitable.yml`: Automatically updates the data to Feishu Bitable. This runs after `generate_markdown` and can be configured to enable or disable publishing. Products already present in `processed_records.json` will not be duplicated.

### Usage

Once set up, the GitHub Action will automatically generate and commit a Markdown file each day with the top products from Product Hunt, and automatically publish it to your WordPress website and Feishu Bitable. These files are stored in the `data/` directory.

### Customization

- You can modify the `scripts/product_hunt_list_to_md.py` file to customize the format or add additional content. This version uses OpenAI's API.
- You can modify the `scripts/product_hunt_list_to_md_dify.py` file to customize the format or add additional content. This version uses Dify's API.
- If needed, adjust the schedule in `.github/workflows/generate_markdown.yml` to change the time of the daily task.

### Example Output

The generated files are stored in the `data/` directory. Each file is named in the format `PH-daily-YYYY-MM-DD.md`.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.