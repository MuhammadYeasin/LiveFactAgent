import spacy
from typing import List

class ClaimExtractor:
    def __init__(self, model_name: str = "en_core_web_sm"):
        self.nlp = spacy.load(model_name)

    def extract_claims(self, text: str) -> List[str]:
        """Extract factual claims from text using spaCy."""
        doc = self.nlp(text)
        claims = []
        for sent in doc.sents:
            # Heuristic: sentences with numbers, stats, or declarative verbs
            if any(token.is_digit or token.text.lower() in ["is", "was", "are", "were"] for token in sent):
                claims.append(sent.text.strip())
        return claims