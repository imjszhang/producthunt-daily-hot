# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Product Hunt Daily Hot is an automated system that generates daily Chinese-translated summaries of Product Hunt's top products using GitHub Actions. It scrapes Product Hunt data, translates content using OpenAI GPT-4, and publishes to WordPress.

## Core Architecture

### Data Pipeline
1. **Data Collection**: GraphQL queries to Product Hunt API for top 30 daily products
2. **Content Processing**: AI-powered translation (OpenAI GPT-4), keyword generation, and image extraction
3. **Publishing**: Markdown generation → WordPress XML-RPC integration

### Key Components

**scripts/product_hunt_list_to_md.py**: Core data processing engine
- Fetches Product Hunt data via GraphQL API
- Handles image extraction (API → OG fallback → error handling)
- AI translation pipeline with fallback mechanisms
- Generates markdown with Chinese keywords and translations

**scripts/publish_to_wordpress.py**: WordPress integration
- Converts markdown to HTML
- Publishes via WordPress REST API with category assignment

**scripts/republish_to_wordpress.py**: Manual republishing utility
- Individual file republishing with error handling
- Command-line interface for post management

**scripts/batch_republish.py**: Batch republishing for historical data
- Date range processing with configurable pauses
- Progress tracking and error reporting

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Generate daily content manually
python scripts/product_hunt_list_to_md.py

# Test with mock data (fallback built-in)
python scripts/product_hunt_list_to_md.py  # Will use mock data if API fails

# Publish to WordPress
python scripts/publish_to_wordpress.py

# Republish specific date
python scripts/republish_to_wordpress.py data/producthunt-daily-2024-12-25.md

# Batch republish date range
python scripts/batch_republish.py --start-date 2024-12-01 --end-date 2024-12-25
```

### GitHub Actions Workflows

**`.github/workflows/generate_markdown.yml`**:
- Scheduled: Daily 07:01 UTC (15:01 Beijing)
- Manual trigger available
- Uses secrets: `OPENAI_API_KEY`, `PRODUCTHUNT_DEVELOPER_TOKEN`, `PAT`

**`.github/workflows/publish_to_wordpress.yml`**:
- Auto-triggered after markdown generation
- Uses secrets: `WORDPRESS_URL`, `WORDPRESS_USERNAME`, `WORDPRESS_PASSWORD`

**`.github/workflows/fix_images.yml`**:
- Manual only (for fixing broken images)
- Configurable batch processing

### Environment Variables

Required for local development:
```bash
# Product Hunt API
PRODUCTHUNT_DEVELOPER_TOKEN=your_token

# OpenAI
OPENAI_API_KEY=your_key

# WordPress (optional for local)
WORDPRESS_URL=https://your-site.com
WORDPRESS_USERNAME=username
WORDPRESS_PASSWORD=password
```

## Key Implementation Details

### API Integration
- Product Hunt GraphQL API with pagination support
- Retry logic (3 attempts with exponential backoff)
- Rate limiting handling (429 responses)

### AI Processing
- GPT-4o-mini for translation and keyword generation
- Fallback to basic keyword extraction when AI unavailable
- Configurable token limits and temperature settings

### Image Handling
- Primary: Product Hunt API media field
- Fallback: OpenGraph meta tags scraping
- Final fallback: Empty string with error logging

### Timezone Management
- UTC → Beijing timezone conversion
- Consistent datetime formatting across all outputs

## File Structure

```
data/                    # Generated markdown files (YYYY-MM-DD.md)
scripts/                 # All Python automation scripts
├── product_hunt_list_to_md.py  # Main data pipeline
├── publish_to_wordpress.py     # WordPress publishing
├── republish_to_wordpress.py   # Single file republish
├── batch_republish.py          # Batch republish utility
└── fix_images.py               # Image fixing utility
```

## Data Format

Generated markdown includes:
- Chinese title with ranking
- Translated tagline and description
- Product website link
- Product Hunt link
- Keywords (Chinese)
- Vote count and featured status
- Beijing timezone timestamps
- Product image (with fallback)

## Common Tasks

### Adding New Features
1. Extend `Product` class in main script
2. Update `to_markdown()` method for new fields
3. Test with mock data before API testing
4. Update GitHub Actions if new secrets required

### Debugging Failed Runs
1. Check GitHub Actions logs for specific error
2. Verify API credentials in repository secrets
3. Test locally with same environment variables
4. Check `daily_report_errors.log` for detailed error logs

### Content Customization
- Modify prompt templates in `Product` class methods
- Adjust markdown formatting in `to_markdown()`
- Change WordPress category ID in publishing scripts
- Update timezone handling in datetime conversions