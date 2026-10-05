import json
from typing import List
from app.core.config import settings
from app.schemas.match import JobMatchReasoning, ExtractedCandidateProfile
from app.models.job import Job

class ExplainerService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.client = None
        if self.provider == "openai" and settings.OPENAI_API_KEY != "mock-key":
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def explain_match(self, candidate: ExtractedCandidateProfile, job: Job) -> JobMatchReasoning:
        """
        Sử dụng Prompt Engineering & Suy luận có cấu trúc để giải thích tại sao công việc phù hợp,
        lỗ hổng kỹ năng còn thiếu và lời khuyên chuẩn bị phỏng vấn bằng tiếng Việt.
        """
        # Lấy danh sách tên kỹ năng của công việc
        job_skills = [s.name for s in job.skills]
        cand_skills = set(candidate.detected_skills)
        
        # Tính toán phần giao nhau và phần còn thiếu
        matched_set = cand_skills.intersection(set(job_skills))
        gap_set = set(job_skills).difference(cand_skills)

        # Tính toán điểm cơ bản theo heuristic
        total_req = max(len(job_skills), 1)
        skill_ratio = len(matched_set) / total_req
        base_score = int(min(98, max(45, int(skill_ratio * 70 + 25))))

        if self.provider == "openai" and self.client:
            prompt = f"""
Bạn là Chuyên gia Tuyển dụng Kỹ thuật và Cố vấn Hướng nghiệp IT cao cấp (Senior Tech Recruiter & Career Mentor).
Hãy đánh giá độ tương thích giữa ứng viên và tin tuyển dụng IT dưới đây hoàn toàn bằng TIẾNG VIỆT tự nhiên, súc tích và thực tế.

Thông Tin Ứng Viên:
- Tên/Hồ sơ: {candidate.name}
- Số năm kinh nghiệm: {candidate.years_of_experience} năm
- Kỹ năng cốt lõi: {', '.join(candidate.detected_skills) or 'Kỹ thuật phần mềm chung'}
- Tóm tắt năng lực: {candidate.summary}

Chi Tiết Công Việc Tuyển Dụng:
- Vị trí: {job.title} tại {job.company}
- Cấp bậc: {job.experience_level}
- Yêu cầu chính: {job.requirements_clean[:500]}
- Kỹ năng mục tiêu: {', '.join(job_skills)}

Phản hồi bắt buộc phải là định dạng JSON hợp lệ tuân thủ schema sau:
{{
  "match_score": <số nguyên từ 0 đến 100>,
  "matched_strengths": ["chuỗi tiếng Việt điểm mạnh 1", "chuỗi tiếng Việt điểm mạnh 2"],
  "skill_gaps": ["chuỗi tiếng Việt kỹ năng còn thiếu 1", "chuỗi tiếng Việt kỹ năng còn thiếu 2"],
  "career_advice": "chuỗi tiếng Việt lời khuyên hành động thực tế để phỏng vấn tốt"
}}
"""
            try:
                response = self.client.chat.completions.create(
                    model=settings.LLM_MODEL,
                    messages=[
                        {"role": "system", "content": "Bạn là chuyên gia tư vấn tuyển dụng IT. Chỉ trả về kết quả bằng JSON tiếng Việt."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2
                )
                data = json.loads(response.choices[0].message.content)
                return JobMatchReasoning(
                    match_score=int(data.get("match_score", base_score)),
                    matched_strengths=data.get("matched_strengths", [f"Thành thạo {s}" for s in matched_set]),
                    skill_gaps=data.get("skill_gaps", [f"Cần bổ sung {g}" for g in gap_set]),
                    career_advice=data.get("career_advice", "Tập trung trình bày rõ các dự án thực tế liên quan đến yêu cầu của tin tuyển dụng.")
                )
            except Exception as e:
                print(f"[WARN] OpenAI LLM Explain thất bại ({e}), chuyển sang chế độ Heuristic tiếng Việt.")

        # Cơ chế Fallback Heuristic bằng Tiếng Việt
        strengths = []
        for s in matched_set:
            strengths.append(f"Nền tảng vững chắc về {s} đáp ứng trực tiếp tiêu chí chuyên môn của vị trí {job.title}.")
        if not strengths:
            strengths.append(f"Kinh nghiệm giải quyết vấn đề và nền tảng kỹ thuật phù hợp với yêu cầu cấp bậc {job.experience_level}.")

        gaps = []
        for g in list(gap_set)[:3]:
            gaps.append(f"Vị trí này đặc biệt ưu tiên kỹ năng {g}, tuy nhiên chưa thấy thể hiện rõ nét trong hồ sơ ứng viên.")
        if not gaps:
            gaps.append("Hồ sơ đã bao quát đầy đủ các kỹ năng cốt lõi theo yêu cầu của công việc.")

        gap_str = ", ".join(list(gap_set)[:2])
        advice = (
            f"Ứng viên đáp ứng {len(matched_set)} kỹ năng trọng tâm của nhà tuyển dụng. "
            + (f"Để tối đa hóa cơ hội vượt qua vòng phỏng vấn, bạn nên chủ động ôn luyện thêm kiến thức về {gap_str}." if gap_str else "Hồ sơ của bạn rất sát với vị trí, hãy tự tin thể hiện các kết quả dự án gần nhất.")
        )

        return JobMatchReasoning(
            match_score=base_score,
            matched_strengths=strengths,
            skill_gaps=gaps,
            career_advice=advice
        )

explainer_service = ExplainerService()
