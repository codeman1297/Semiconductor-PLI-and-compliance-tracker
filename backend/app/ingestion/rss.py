"""RSS ingestion adapter placeholder. Fetching is deliberately deferred until feeds are reviewed."""
from app.ingestion.sources import SourceCandidate
def candidates_from_feed(_feed_url:str)->list[SourceCandidate]: return []
