LinkedIn Post Generator with Self-Evaluation (LangGraph)

An AI-powered LinkedIn post generator that writes, evaluates, and optimizes posts automatically using a multi-step LangGraph workflow.
The system simulates a real editorial pipeline: creator → strict evaluator → optimizer.

Built with LangGraph, LangChain, Groq LLMs, and Streamlit.

⸻

🚀 Features
	•	✍️ Post Generation
Generates intelligent, professional LinkedIn posts based on a given topic.
	•	🧠 Strict AI Evaluation
Evaluates the post like a senior LinkedIn editor using predefined rules:
	•	Professional & intelligent tone
	•	Simple, human-like English
	•	No Q&A format
	•	Subtle humor only
	•	Max 280 words
	•	🔁 Iterative Optimization Loop
If the post fails evaluation, it is rewritten using evaluator feedback.
The loop continues until:
	•	The post is Approved, or
	•	The maximum iteration limit is reached.
	•	🧩 LangGraph State Machine
Uses conditional routing to control the generation → evaluation → optimization flow.
	•	🖥️ Simple Streamlit UI
One input (topic) → one output (final LinkedIn post).

⸻

🏗️ Architecture Overview

START
  ↓
Generate Post
  ↓
Evaluate Post
  ↓
Approved? ── Yes → END
   |
   No
   ↓
Optimize Post (using feedback)
   ↓
Re-evaluate


⸻

🛠️ Tech Stack
	•	Python
	•	LangGraph – State-based workflow orchestration
	•	LangChain
	•	Groq LLMs (openai/gpt-oss-20b)
	•	Pydantic – Structured evaluation output
	•	Streamlit – Web UI
	•	dotenv – Environment variable management

⸻

📁 Project Structure

├── PostGenerator.py
├── .env
├── requirements.txt
└── README.md


⸻

🔐 Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

⚠️ Do not commit your API keys to GitHub.

⸻

▶️ How to Run
	1.	Clone the repository

git clone https://github.com/koffin-master/linkedin-post-generator.git
cd linkedin-post-generator

	2.	Install dependencies

pip install -r requirements.txt

	3.	Run the Streamlit app

streamlit run PostGenerator.py

	4.	Open in browser

http://localhost:8501


⸻

🧪 Example Use Case
	•	Enter topic:
Learning LangGraph as an AI Engineer
	•	Output:
A refined, professional LinkedIn post that has passed strict editorial evaluation.

⸻

🎯 Why This Project Matters
	•	Demonstrates Agentic AI workflows
	•	Shows real-world use of LangGraph conditional routing
	•	Implements self-refining LLM pipelines
	•	Reduces hallucination and generic outputs via evaluator feedback
	•	Mirrors real content production pipelines

⸻

📌 Future Improvements
	•	Add post sentiment scoring
	•	Support hashtags & formatting toggle
	•	Add multiple writing styles
	•	Save iteration history
	•	Deploy on cloud (Streamlit Cloud / Hugging Face Spaces)

⸻

🤝 Acknowledgements
	•	LangChain & LangGraph teams
	•	Groq for fast inference
	•	Streamlit for rapid UI development

⸻

📄 License

This project is open-source and available under the MIT License.
