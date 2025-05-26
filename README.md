<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Multi-Agent RAG 應用質量保障建設</h3>

  <p align="center">
    Multi-Agent RAG 應用質量保障建設 的自動化測試專案
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#Linter Rules">Linter Rules</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
本 Repo 為一個專注於 **Multi-Agent RAG 應用質量保障建設** 的自動化測試專案。  
由於本專案已實際應用於內部服務，為保障資訊安全，內容經過**去敏處理**後公開，故目前無法直接執行測試腳本，建議可以參考專案的架構即可。

本專案的自動化測試涵蓋兩大核心部分：`api` 與 `ai` 測試。

✅ API 測試
- 進行服務的整合測試，確保各 API 的穩定性與可用性。
- 將 API 進行封裝，提供統一接口供 AI 測試調用，提升測試效率與可維護性。

 🤖 AI 測試
AI 測試模組涵蓋以下面向：
- Router 路由邏輯測試
- 大模型回覆內容的準確性與一致性測試
- 基礎設施與資料安全性測試

在大模型回覆測試方面，我們採用了「**用魔法對付魔法**」的策略（LLM as a Judge）  
以 LLM 對 LLM 輸出內容進行自動化評估，提升測試準確性與自動化程度。

 📬 歡迎交流
本專案致力於為 RAG 類應用提供系統性、可擴展的質量保障方案。  
如果您對 Multi-Agent RAG 測試與品質保障有興趣，歡迎與作者交流，一起推動智能應用的測試方法。

<!-- GETTING STARTED -->
## Getting Started
這個專案主要是透過 pytest 來進行建構的。

### Installation

Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services.

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Install packages
   ```sh
   cd auto-test/[api, ai]
   pip install -r requirements.txt
   ```
 3. Setup `.env` file


### Linter Rules
In this repository, code scan through [Ruff](https://beta.ruff.rs/docs/) (An extremely fast Python linter, written in Rust), and here is our skip rules:
* [E501](https://www.flake8rules.com/rules/E501.html)：Line too long (82 > 79 characters)
* [E402](https://www.flake8rules.com/rules/E402.html)：Module level import not at top of file
* [E701](https://www.flake8rules.com/rules/E701.html)：Multiple statements on one line (colon)
* [F401](https://www.flake8rules.com/rules/F401.html)：Module imported but unused
* [F405](https://www.flake8rules.com/rules/F405.html)：Name may be undefined, or defined from star imports: module
* [F403](https://www.flake8rules.com/rules/F403.html)：`from module import *` used; unable to detect undefined names

<!-- CONTACT -->
## Contact

Linkedin: [https://www.linkedin.com/in/max-tsai/](https://www.linkedin.com/in/max-tsai/)
