from app.ingestion.sources import SourceCandidate
def parse_manual_source(**values)->SourceCandidate: return SourceCandidate(**values)
