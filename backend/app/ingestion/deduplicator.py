import hashlib
def content_hash(content:str)->str: return hashlib.sha256(content.encode()).hexdigest()
def is_duplicate(existing_hashes:set[str],content:str)->bool: return content_hash(content) in existing_hashes
