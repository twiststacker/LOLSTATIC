# 🏆 LOLSTATIC // AI-Powered Hextech Dashboard

**LOLSTATIC** is a high-performance desktop companion for League of Legends players. It leverages local Large Language Models (LLMs) and Riot's Data Dragon to provide deep match analysis and meta-tier insights through a custom Hextech-themed interface.

---

## ✨ Key Features

* **🤖 Hextech AI Coach**: Connects to a local Ollama instance (DeepSeek-R1) to analyze your recent match history and provide macro-strategy coaching.
* **📊 Dynamic Tier List**: Generates live S-Tier rankings for the current patch using AI-driven meta analysis.
* **🖼️ Champion Archive**: A searchable database of all League champions with high-resolution icons pulled directly from Riot's Data Dragon CDN.
* **📜 Integrated Patch Notes**: Direct access to the latest game updates and patch notes within the dashboard.

---

## 🛠️ Technical Stack

* **Language**: Python 3.10
* **GUI Framework**: CustomTkinter (Hextech UI Theme)
* **Containerization**: Docker & Docker Compose
* **AI Core**: Ollama (Running local LLMs)
* **API Integration**: Riot Games API (Match-V5, Summoner-V4)

---

## 🚀 Getting Started

### Prerequisites
1.  **Docker Desktop**: Ensure Docker is installed and running.
2.  **X-Server (Windows)**: Install VcXsrv (XLaunch) to display the GUI from the container.
3.  **Ollama**: Install and run Ollama on your host machine.

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/twiststacker/LOLSTATIC.git](https://github.com/twiststacker/LOLSTATIC.git)
   cd LOLSTATIC
