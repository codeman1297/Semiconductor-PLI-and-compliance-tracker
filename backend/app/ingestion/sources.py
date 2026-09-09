from dataclasses import dataclass
@dataclass(frozen=True)
class SourceCandidate:
    url:str; source_type:str; publisher:str; title:str|None=None; published_at:str|None=None; content:str|None=None
