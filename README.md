# Merlot 2.0

## Overview

Merlot 2.0 is a Python-based project that serves as a revised version of the Merlot stealer. This tool is designed for educational purposes only, providing insights into how data exfiltration tools operate. It is intended for cybersecurity professionals, researchers, and students who wish to understand the mechanics of such tools in a controlled and ethical environment.

## Disclaimer

**This project is for educational purposes only.** The use of this tool for malicious purposes is strictly prohibited. The authors and contributors are not responsible for any misuse of this software. Always ensure you have explicit permission before using this tool on any system.

## Features

- **Data Exfiltration**: Demonstrates techniques for extracting sensitive information.
- **Network Communication**: Simulates sending data to a remote server via a Telegram bot.
- **Shadow Copy**: Uses shadow copy to prevent browsers from crashing during data extraction.
- **Modular Design**: Easily extendable with new features and capabilities.
- **Chromium-Based Browsers**: Currently supports data extraction from Chromium-based browsers only.

## Under Development

We are actively working on adding more features to enhance the educational value of this project. Some of the upcoming features include:

- **Rotating API Keys And Chat_Id**: This feature retrieves API keys and Chat_Id from a server, ensuring they are regularly rotated for enhanced security As Hard coding API keys is not recommended.
- **Advanced Obfuscation Techniques**: To demonstrate how attackers hide their activities.
- **NTLM-Hash Stealer**: A section dedicated to stealing NTLM hashes.
- **Crypto-Wallet Stealer**: A section for extracting information from cryptocurrency wallets.
- **Improved Network Protocols**: For more realistic and Improved data exfiltration scenarios.


## Usage

Ensure you have the necessary permissions before running this tool. Before starting the tool, you need to replace `{API_KEY}` and `{Chat_Id}` with your own values directly in the code where these variables are defined.

1. Open the the section of the code where `{API_KEY}` and `{Chat_Id}` are defined.
2. Replace `{API_KEY}` with your actual Telegram bot API key.
3. Replace `{Chat_Id}` with your actual Telegram chat ID.
