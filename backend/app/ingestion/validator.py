from app.ingestion.sources import SourceCandidate
def validate_candidate(item:SourceCandidate)->list[str]:
    errors=[]
    if not item.url.startswith(('https://','http://')): errors.append('A public http(s) URL is required')
    if not item.publisher: errors.append('Publisher is required')
    return errors
