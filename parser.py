import os
import re

def parse_mission2_files(data_dir="data"):
    """
    Parses Grand Saga markdown files from the specified directory.
    Expected format: **WORD** (meaning) - Context sentence
    """
    words = []
    seen_words = set()
    
    # regex matches: **WORD** (meaning)
    regex = r"\*\*(?P<word>[^*]+)\*\*\s*_?\((?P<meaning>[^)]+)\)"
    
    # We look for files matching grand_saga_group*.md
    files = [f for f in os.listdir(data_dir) if f.startswith("grand_saga_group") and f.endswith(".md")]
    
    # Sort files numerically by group number
    def extract_num(f):
        match = re.search(r'group(\d+)', f)
        return int(match.group(1)) if match else 999
    
    files.sort(key=extract_num)
    
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            for line in content.split('\n'):
                for match in re.finditer(regex, line):
                    w_text = match.group("word").strip()
                    # Skip if contains Hindi (Mission 2 logic)
                    if not re.search(r'[\u0900-\u097F]', w_text) and len(w_text) > 1:
                        w_upper = w_text.upper()
                        if w_upper not in seen_words:
                            words.append({
                                "word": w_upper,
                                "meaning": match.group("meaning").strip(),
                                "sentence": line.replace("**", "").replace("_", "").strip(),
                                "source": filename
                            })
                            seen_words.add(w_upper)
        except Exception as e:
            print(f"Error parsing {filename}: {e}")
            
    print(f"✅ Loaded {len(words)} Mission 2 words from {len(files)} files.")
    return words
