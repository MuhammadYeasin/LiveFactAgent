LiveFactAgent
LiveFactAgent is a real-time fact-checking AI agent built for the Perplexity Hackathon 2025. It processes live speech, transcribes it using Whisper, extracts claims with spaCy, and verifies them using Perplexity’s Sonar API via the Model Context Protocol (MCP). Deployed on Vercel with a Streamlit frontend, it delivers instant fact-checks for debates, speeches, or podcasts, combating misinformation on the fly.
🌟 Submitted for the Perplexity Hackathon: https://perplexityhackathon.devpost.com/🔗 Powered by Perplexity Sonar API: https://x.ai/api
Features

Real-time speech transcription using Whisper.
Claim extraction with spaCy for accurate fact identification.
Fact-checking via Perplexity’s Sonar API with trusted citations.
FastAPI server with MCP integration for seamless API connectivity.
Streamlit frontend for user-friendly result display.

Setup

Clone the Repository:
git clone https://github.com/your-username/LiveFactAgent.git
cd LiveFactAgent


Install Dependencies:
pip install -r requirements.txt
python -m spacy download en_core_web_sm


Configure Sonar API:

Get your API key from https://x.ai/api.
Add it to the .env file:echo "SONAR_API_KEY=your-sonar-api-key" > .env




Run the Application:

Start the FastAPI server:python src/server.py


In a separate terminal, run the Streamlit frontend:streamlit run src/streamlit_app.py




Access the App:

Open http://localhost:8501 in your browser.
Speak into your microphone to see real-time fact-checking.



Deployment

Deploy the FastAPI server on Vercel using their MCP template: https://vercel.com/templates.
Host the Streamlit app separately or integrate it into Vercel.

Demo
[Insert link to demo video or screenshots once created]
Future Work

Integrate Sonar Deep Research for complex claims.
Support multi-language transcription.
Enhance claim extraction with transformer models.

License
MIT License
