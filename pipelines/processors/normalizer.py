import re
import json
from pathlib import Path
from typing import List, Set, Tuple, Dict, Any

TAXONOMY_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "taxonomy" / "skills_taxonomy.json"

class SkillNormalizer:
    def __init__(self, taxonomy_file: Path = TAXONOMY_PATH):
        self.taxonomy = self._load_taxonomy(taxonomy_file)
        self.skill_map = self._build_alias_map()

    def _load_taxonomy(self, path: Path) -> Dict[str, Any]:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"skills": []}

    def _build_alias_map(self) -> Dict[str, Tuple[str, str]]:
        """
        Builds a lookup mapping from lowercase alias to (Canonical Skill Name, Category)
        """
        lookup = {}
        for item in self.taxonomy.get("skills", []):
            canonical = item["name"]
            category = item.get("category", "General")
            aliases = item.get("aliases", [canonical.lower()])
            for alias in aliases:
                lookup[alias.lower().strip()] = (canonical, category)
        return lookup

    def extract_skills(self, text: str) -> List[str]:
        """
        Extracts standardized canonical skills from raw text using boundary regex.
        """
        if not text:
            return []
            
        text_lower = " " + text.lower() + " "
        matched_canonical: Set[str] = set()

        for alias, (canonical, _) in self.skill_map.items():
            # Match whole word boundaries (taking care of +, #, . in C++, C#, .NET, Node.js)
            escaped = re.escape(alias)
            pattern = rf'(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower):
                matched_canonical.add(canonical)

        return sorted(list(matched_canonical))

    def infer_experience_level(self, text: str, title: str = "") -> str:
        """
        Infers whether the job is Junior, Mid-Level, Senior, or Lead
        """
        combined = f"{title} {text}".lower()

        if re.search(r'\b(lead|principal|architect|head of|director|trưởng nhóm)\b', combined):
            return "Lead"
        if re.search(r'\b(senior|sr\.?|chuyên viên cấp cao|5\+|6\+|7\+|8\+ years)\b', combined):
            return "Senior"
        if re.search(r'\b(junior|fresher|intern|thực tập|mới tốt nghiệp|entry level|0-1 year|1 year)\b', combined):
            return "Junior"
        
        return "Mid-Level"

skill_normalizer = SkillNormalizer()
