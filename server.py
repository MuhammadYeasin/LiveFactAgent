import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.audio_processor import AudioProcessor
from src.claim_extractor import ClaimExtractor
from src.fact_checker import FactChecker
from typing import List
from pydantic import BaseModel

# Define request model
class ClaimRequest(BaseModel):
    claim: str

app = FastAPI(title="LiveFactAgent API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
audio_processor = AudioProcessor()
claim_extractor = ClaimExtractor()
fact_checker = FactChecker()

@app.post("/fact-check")
async def fact_check(request: ClaimRequest):
    """Regular endpoint for fact-checking."""
    result = await fact_checker.fact_check(request.claim)
    return result.dict()

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    print("WebSocket connection attempt received")
    await websocket.accept()
    print("WebSocket connection accepted")
    try:
        while True:
            print("Recording audio...")
            audio_file = audio_processor.record_audio()
            print(f"Audio recorded to {audio_file}")
            transcript = await audio_processor.transcribe_audio(audio_file)
            print(f"Transcription: {transcript}")

            claims = claim_extractor.extract_claims(transcript)
            print(f"Extracted claims: {claims}")
            results = []
            for claim in claims:
                result = await fact_checker.fact_check(claim)
                results.append(result.dict())

            await websocket.send_json({"transcript": transcript, "results": results})
            print("Results sent to client")
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        import traceback
        traceback.print_exc()
        await websocket.send_json({"error": str(e)})
    finally:
        print("WebSocket connection closed")
        await websocket.close()

@app.get("/")
async def root():
    return {"message": "LiveFactAgent API is running. Connect to /ws/audio for real-time fact-checking."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)