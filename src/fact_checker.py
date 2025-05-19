import aiohttp
from dotenv import load_dotenv
import os
from typing import Dict, List
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

class FactCheckResult(BaseModel):
    claim: str
    status: str  # true/false/uncertain
    citations: List[Dict[str, str]]

class FactChecker:
    def __init__(self, api_url: str = "https://api.perplexity.ai/sonar"):
        self.api_url = api_url
        self.api_key = os.getenv("SONAR_API_KEY")
        if not self.api_key:
            raise ValueError("SONAR_API_KEY not found in .env file")

    async def query_sonar(self, claim: str) -> Dict:
        """Query Sonar API to verify a claim."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "query": f"Verify the claim: {claim}",
            "model": "sonar-pro",  # Use Sonar Pro for faster responses
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                return {"error": f"API request failed: {response.status}"}

    async def fact_check(self, claim: str) -> FactCheckResult:
        """Fact-check a claim using Sonar API."""
        sonar_response = await self.query_sonar(claim)
        if "error" in sonar_response:
            return FactCheckResult(claim=claim, status="uncertain", citations=[])

        # Parse Sonar response (simplified)
        answer = sonar_response.get("answer", "")
        citations = sonar_response.get("citations", [])
        status = "true" if "true" in answer.lower() else "false" if "false" in answer.lower() else "uncertain"

        return FactCheckResult(claim=claim, status=status, citations=citations)