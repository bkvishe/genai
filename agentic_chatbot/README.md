# genai-agent-tools

## Setup & Execution

This project demonstrates a basic agentic AI system using OpenAI's API and external tools like weather and currency conversion APIs.

1. **Clone the Repository**

```bash
git clone https://github.com/bkvishe/genai.git
cd genai/agentic_chatbot
```

2. **Create Virtual Environment (Optional but Recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Environment Variables**
##### Create a .env file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key
```

5. **Run the Agent**

```bash
python app.py
```

## **🤖 Using Other LLMs**

This project currently uses OpenAI's GPT models via the openai Python SDK.
However, the architecture is modular and can be easily adapted to work with other LLMs (e.g., Google Gemini, Anthropic Claude, Mistral, or local models via Hugging Face).

To switch to another LLM provider:

- Replace the openai client calls with the respective SDK or API.
- Ensure the response follows the expected JSON structure used in this agent loop.
- Update requirements.txt accordingly.
