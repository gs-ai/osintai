# OSINTai - Sentinel Crawler

## Overview
**Sentinel Crawler** is an advanced web crawling tool designed for **Open Source Intelligence (OSINT)** professionals, security analysts, and investigators. It automates the systematic collection of web-based intelligence, extracting relevant URLs, analyzing structured content, and leveraging AI for in-depth analysis.

With capabilities including **user-agent rotation**, **depth-based crawling**, **keyword identification**, and **AI-powered analysis**, Sentinel Crawler enables precise data extraction for intelligence operations.

---

## Features
- **Configurable Crawling Parameters** – Define depth, URL limits, and seed URLs for targeted intelligence gathering.
- **User-Agent Randomization** – Avoid detection and prevent request blocking.
- **Keyword Detection & Content Parsing** – Identify terms related to credentials, personal data, and operational intelligence.
- **AI-Enhanced Content Analysis** – Integrates **Ollama Gemma** for automated text evaluation and anomaly detection.
- **Data Extraction & Comparison** – Identifies significant differences between raw and analyzed content.
- **Secure Output Storage** – Retains all processed intelligence in structured reports.

---

## Installation
Ensure you have **Python 3.7+** installed.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/OSINTai.git
cd OSINTai
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv osintaiENV
source osintaiENV/bin/activate  # macOS/Linux
osintaiENV\Scripts\activate    # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
_(If `requirements.txt` is unavailable, manually install:)_
```bash
pip install beautifulsoup4 requests
```

### 4. Install Ollama (for AI-based Analysis)
```bash
brew install ollama  # macOS (Homebrew)
```

---

## Usage
Execute the crawler interactively:
```bash
python OSINTai3.2.py
```

### Example Input
```
Enter the seed URL to start crawling: https://example.com
Enter the maximum depth for crawling: 3
Enter the maximum number of URLs to crawl: 100
Enter search terms (comma-separated) or press enter to skip: email, username, password
```

### Output
- Extracted and categorized URLs
- Content intelligence analysis using **Ollama Gemma**
- Structural and semantic variations in extracted data
- Generated reports stored as structured text files

---

## Why Use Sentinel Crawler?
- **Precision OSINT Gathering** – Automates intelligence collection efficiently.
- **Obfuscation Features** – Employs randomized User-Agents to prevent detection.
- **AI-Driven Intelligence Processing** – Enhances raw data with contextual analysis.
- **Customizable Crawling** – Define search parameters for tailored intelligence needs.

---

## Legal Disclaimer
This tool is strictly for **ethical intelligence research** and **compliance-driven investigations**. Unauthorized data extraction or use of this tool for illicit activities is **prohibited**. The author assumes **no liability** for misuse.

---

## License
This project is distributed under the **MIT License**.

---

## Contributing
Contributions are encouraged! Submit pull requests to improve functionality and security.

---

## Contact
Paint the pigeon red.
