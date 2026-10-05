import re
import html
from bs4 import BeautifulSoup

class JobCleaner:
    # Common boilerplate noise keywords in IT job descriptions (Perks, benefits, general info)
    BOILERPLATE_PATTERNS = [
        r'(?:benefits|phúc lợi|quyền lợi|chế độ đãi ngộ|what we offer|perks|compensation).*',
        r'(?:about us|về chúng tôi|about our company|giới thiệu công ty).*?(?=(?:requirements|yêu cầu|qualifications|kỹ năng|$))',
        r'(?:how to apply|cách thức ứng tuyển|contact us|liên hệ).*',
        r'(?:equal opportunity employer|chính sách bình đẳng).*',
    ]

    REQUIREMENT_HEADERS = [
        r'(?:requirements|yêu cầu công việc|yêu cầu ứng viên|qualifications|what you need|what we are looking for|kỹ năng cần có|technical requirements|job requirements)',
        r'(?:responsibilities|trách nhiệm|mô tả công việc|what you will do|role description)'
    ]

    @classmethod
    def clean_html(cls, raw_html: str) -> str:
        """Strip HTML tags, unescape entities, remove scripts and normalize spaces."""
        if not raw_html:
            return ""
        
        soup = BeautifulSoup(raw_html, "html.parser")
        
        # Remove noisy tags
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg", "form"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        text = html.unescape(text)

        # Normalize linebreaks and whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    @classmethod
    def extract_core_requirements(cls, full_text: str) -> str:
        """
        Extracts the technical requirements section from the full job description,
        filtering out generic company boilerplate and compensation sections.
        """
        if not full_text:
            return ""

        clean_text = full_text

        # Try to find the start of the requirements section
        req_start = -1
        for pattern in cls.REQUIREMENT_HEADERS:
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                req_start = match.start()
                break

        if req_start != -1:
            clean_text = clean_text[req_start:]

        # Cut off benefits / perks section if found afterwards
        for pattern in cls.BOILERPLATE_PATTERNS:
            match = re.search(pattern, clean_text, re.IGNORECASE | re.DOTALL)
            if match and match.start() > 150: # Only cut if we already captured sufficient text
                clean_text = clean_text[:match.start()]
                break

        # Remove repetitive excess spaces
        clean_text = re.sub(r'[ \t]+', ' ', clean_text)
        clean_text = re.sub(r'\n{3,}', '\n\n', clean_text).strip()

        # Fallback to the first 2000 chars if extraction resulted in very short text
        if len(clean_text) < 100:
            return full_text[:2000]

        return clean_text[:3000]

job_cleaner = JobCleaner()
