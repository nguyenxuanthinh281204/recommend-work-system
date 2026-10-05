import React, { useState, useEffect } from 'react';
import {
  FileText,
  Search,
  BarChart3,
  Cpu,
  CheckCircle2,
  AlertCircle,
  Briefcase,
  MapPin,
  DollarSign,
  TrendingUp,
  Sparkles,
  ChevronDown,
  ChevronUp,
  ArrowRight,
  Database
} from 'lucide-react';

const API_BASE = '/api/v1';

// Mẫu hồ sơ ứng viên mẫu để bấm 1-click kiểm thử ngay lập tức
const CV_TEMPLATES = {
  data_ai: `Trần Thị Bích - Kỹ Sư Dữ Liệu & Trí Tuệ Nhân Tạo (Data & AI Engineer)
Email: bich.tran.ai@example.com | Số điện thoại: 0912 345 678
Kinh nghiệm: 3 năm kinh nghiệm trong ngành IT
Công nghệ cốt lõi: Python, FastAPI, Apache Airflow, Apache Spark, PostgreSQL, Deep Learning / LLM, Vector Search, Machine Learning.
Tóm tắt năng lực: Chuyên sâu xây dựng đường ống xử lý dữ liệu lớn (ETL Pipeline), tích hợp hệ thống tìm kiếm ngữ nghĩa RAG (Semantic Search với pgvector), và triển khai mô hình học máy vào thực tế.`,
  
  devops: `Nguyễn Văn An - Kỹ Sư DevOps & Điện Toán Đám Mây (Senior DevOps)
Email: an.nguyen.devops@example.com | Số điện thoại: 0988 123 456
Kinh nghiệm: 4 năm kinh nghiệm làm việc
Công nghệ cốt lõi: Docker, Kubernetes, AWS (EKS, EC2, S3), CI/CD (GitHub Actions, GitLab CI), Terraform, Linux.
Tóm tắt năng lực: Có kinh nghiệm dày dặn về tự động hóa hạ tầng đám mây, điều phối container phân tán và xây dựng hệ thống vi dịch vụ chịu tải cao, tính sẵn sàng 99.99%.`,
  
  fullstack: `Lê Hoàng Cường - Lập Trình Viên Fullstack (React & Node.js)
Email: cuong.le.dev@example.com | Số điện thoại: 0903 888 999
Kinh nghiệm: 2.5 năm kinh nghiệm
Công nghệ cốt lõi: React, TypeScript, Node.js, PostgreSQL, Docker, RESTful APIs.
Tóm tắt năng lực: Phát triển giao diện web hiện đại với React và TypeScript; thiết kế backend tối ưu với Node.js và CSDL quan hệ PostgreSQL.`
};

export default function App() {
  const [activeTab, setActiveTab] = useState('matcher'); // 'matcher' | 'analytics' | 'explorer'
  const [cvText, setCvText] = useState(CV_TEMPLATES.data_ai);
  const [isLoading, setIsLoading] = useState(false);
  const [matchResult, setMatchResult] = useState(null);
  const [expandedJobId, setExpandedJobId] = useState(null);
  
  // Trạng thái dữ liệu thống kê
  const [analyticsData, setAnalyticsData] = useState(null);

  // Trạng thái tra cứu việc làm
  const [jobsList, setJobsList] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLevel, setSelectedLevel] = useState('');

  // Tải dữ liệu ban đầu
  useEffect(() => {
    fetchAnalytics();
    fetchJobs();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const res = await fetch(`${API_BASE}/analytics/hot-skills`);
      if (res.ok) {
        const data = await res.json();
        setAnalyticsData(data);
      }
    } catch {
      // Dữ liệu mẫu hiển thị offline khi chưa bật Docker Backend
      setAnalyticsData({
        top_skills: [
          { skill: 'Python', category: 'Backend', count: 18 },
          { skill: 'Docker', category: 'DevOps & Cloud', count: 16 },
          { skill: 'PostgreSQL', category: 'Database', count: 15 },
          { skill: 'Kubernetes', category: 'DevOps & Cloud', count: 12 },
          { skill: 'AWS', category: 'DevOps & Cloud', count: 12 },
          { skill: 'FastAPI', category: 'Backend', count: 10 },
          { skill: 'Deep Learning / LLM', category: 'Data & AI', count: 9 },
          { skill: 'React', category: 'Frontend', count: 8 },
          { skill: 'Apache Airflow', category: 'Data & AI', count: 7 },
        ],
        categories: [
          { category: 'DevOps & Cloud', count: 40 },
          { category: 'Data & AI', count: 34 },
          { category: 'Backend', count: 28 },
          { category: 'Database', count: 22 },
          { category: 'Frontend', count: 16 }
        ]
      });
    }
  };

  const fetchJobs = async () => {
    try {
      const res = await fetch(`${API_BASE}/jobs?limit=20`);
      if (res.ok) {
        const data = await res.json();
        setJobsList(data);
      }
    } catch {
      // Danh sách việc làm mẫu tiếng Việt khi chạy độc lập
      setJobsList([
        {
          id: 1,
          title: "Kỹ Sư AI / LLM (RAG & Semantic Search)",
          company: "NextGen AI Labs",
          location: "Làm việc từ xa (Remote)",
          salary_range: "2.000$ - 3.000$",
          experience_level: "Mid-Level",
          requirements_clean: "Có kinh nghiệm thực chiến phát triển các ứng dụng Deep Learning / LLM và kiến trúc RAG. Thành thạo Python, FastAPI, và các cơ sở dữ liệu Vector Search như pgvector, Milvus hoặc Pinecone.",
          skills: [{ id: 1, name: "Python", category: "Backend" }, { id: 2, name: "FastAPI", category: "Backend" }, { id: 3, name: "Deep Learning / LLM", category: "Data & AI" }, { id: 4, name: "Vector Search", category: "Data & AI" }]
        },
        {
          id: 2,
          title: "Senior Data Engineer (Apache Airflow & Spark)",
          company: "Fintech Analytics Ltd",
          location: "Hà Nội / Hybrid",
          salary_range: "2.200$ - 3.200$",
          experience_level: "Senior",
          requirements_clean: "Kinh nghiệm chuyên sâu xây dựng hạ tầng xử lý dữ liệu lớn (Batch & Streaming). Thành thạo Apache Airflow, Apache Spark, Python và tối ưu hóa truy vấn CSDL PostgreSQL.",
          skills: [{ id: 1, name: "Python", category: "Backend" }, { id: 5, name: "Apache Airflow", category: "Data & AI" }, { id: 6, name: "Apache Spark", category: "Data & AI" }, { id: 7, name: "PostgreSQL", category: "Database" }]
        },
        {
          id: 3,
          title: "Senior DevOps & Cloud Platform Engineer",
          company: "CloudNative Global",
          location: "Hồ Chí Minh / Remote",
          salary_range: "2.500$ - 3.500$",
          experience_level: "Senior",
          requirements_clean: "Chuyên sâu về Docker, điều phối cụm Kubernetes, viết Terraform và tự động hóa CI/CD với GitHub Actions. Kinh nghiệm quản trị đám mây AWS (EKS, EC2, S3).",
          skills: [{ id: 10, name: "Docker", category: "DevOps & Cloud" }, { id: 11, name: "Kubernetes", category: "DevOps & Cloud" }, { id: 12, name: "AWS", category: "DevOps & Cloud" }, { id: 13, name: "CI/CD", category: "DevOps & Cloud" }]
        }
      ]);
    }
  };

  const handleMatch = async () => {
    if (!cvText.trim()) return;
    setIsLoading(true);
    setExpandedJobId(null);

    try {
      const formData = new FormData();
      formData.append('cv_text', cvText);
      formData.append('top_k', '10');

      const res = await fetch(`${API_BASE}/match/cv`, {
        method: 'POST',
        body: formData
      });

      if (res.ok) {
        const data = await res.json();
        setMatchResult(data);
      } else {
        throw new Error('API request failed');
      }
    } catch {
      // Mô phỏng kết quả phân tích bằng tiếng Việt trực quan khi chạy demo
      setTimeout(() => {
        setMatchResult({
          candidate: {
            name: "Hồ Sơ Ứng Viên",
            years_of_experience: 3.0,
            detected_skills: ["Python", "FastAPI", "PostgreSQL", "Deep Learning / LLM", "Vector Search"],
            summary: "Kỹ sư chuyên sâu về xử lý dữ liệu, xây dựng hệ thống tìm kiếm ngữ nghĩa RAG và triển khai mô hình học máy ứng dụng."
          },
          top_matches: [
            {
              job: {
                id: 1,
                title: "Kỹ Sư AI / LLM (RAG & Semantic Search)",
                company: "NextGen AI Labs",
                location: "Làm việc từ xa (Remote)",
                salary_range: "2.000$ - 3.000$",
                experience_level: "Mid-Level",
                requirements_clean: "Có kinh nghiệm thực chiến phát triển các ứng dụng Deep Learning / LLM và kiến trúc RAG. Thành thạo Python, FastAPI, và các cơ sở dữ liệu Vector Search như pgvector, Milvus hoặc Pinecone.",
                skills: [{ id: 1, name: "Python" }, { id: 2, name: "FastAPI" }, { id: 3, name: "Deep Learning / LLM" }, { id: 4, name: "Vector Search" }]
              },
              match_score: 95,
              matched_skills: ["Python", "FastAPI", "Deep Learning / LLM", "Vector Search"],
              missing_skills: [],
              reasoning: {
                match_score: 95,
                matched_strengths: [
                  "Trùng khớp 100% Tech Stack cốt lõi: Python, FastAPI, Deep Learning / LLM và Vector Search.",
                  "Có kinh nghiệm thực tế về kiến trúc RAG và tìm kiếm vector với pgvector đáp ứng hoàn hảo bài toán tuyển dụng."
                ],
                skill_gaps: [
                  "Cần nhấn mạnh thêm kinh nghiệm tối ưu hóa độ trễ (latency benchmarking) khi phục vụ mô hình tải cao."
                ],
                career_advice: "Hồ sơ của bạn cực kỳ tiềm năng cho vị trí này! Trong buổi phỏng vấn, hãy chuẩn bị kỹ sơ đồ thiết kế hệ thống RAG và thuật toán xếp hạng RRF mà bạn đã từng triển khai."
              }
            },
            {
              job: {
                id: 2,
                title: "Senior Data Engineer (Apache Airflow & Spark)",
                company: "Fintech Analytics Ltd",
                location: "Hà Nội / Hybrid",
                salary_range: "2.200$ - 3.200$",
                experience_level: "Senior",
                requirements_clean: "Kinh nghiệm chuyên sâu xây dựng hạ tầng xử lý dữ liệu lớn (Batch & Streaming). Thành thạo Apache Airflow, Apache Spark, Python và tối ưu hóa CSDL PostgreSQL.",
                skills: [{ id: 1, name: "Python" }, { id: 5, name: "Apache Airflow" }, { id: 6, name: "Apache Spark" }, { id: 7, name: "PostgreSQL" }]
              },
              match_score: 78,
              matched_skills: ["Python", "PostgreSQL"],
              missing_skills: ["Apache Airflow", "Apache Spark"],
              reasoning: {
                match_score: 78,
                matched_strengths: [
                  "Nền tảng lập trình Python vững chắc và khả năng làm việc tốt với cơ sở dữ liệu PostgreSQL."
                ],
                skill_gaps: [
                  "Công việc đòi hỏi chuyên sâu về điều phối dữ liệu lớn với Apache Spark và lên lịch DAG trên Airflow."
                ],
                career_advice: "Để nâng cao tỷ lệ trúng tuyển, bạn nên thực hành thêm các bài toán ETL phân tán với PySpark và thiết lập pipeline tự động trên Airflow."
              }
            }
          ]
        });
      }, 600);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleExpand = (id) => {
    setExpandedJobId(expandedJobId === id ? null : id);
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="glass-panel app-header">
        <div className="brand-wrapper">
          <div className="brand-logo">
            <Cpu size={24} />
          </div>
          <div>
            <h1 className="brand-title">MatchAI Pro</h1>
            <div className="brand-tagline">Hệ Thống Gợi Ý Việc Làm Thông Minh & Semantic Search (CV ↔ JD)</div>
          </div>
        </div>
        <div className="status-badge">
          <span className="status-dot"></span>
          <span>PostgreSQL + pgvector Đang Kích Hoạt</span>
        </div>
      </header>

      {/* Tabs Navigation */}
      <nav className="tabs-nav">
        <button
          className={`tab-btn ${activeTab === 'matcher' ? 'active' : ''}`}
          onClick={() => setActiveTab('matcher')}
        >
          <Sparkles size={16} />
          <span>So Khớp CV & Cố Vấn AI</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          <BarChart3 size={16} />
          <span>Radar Xu Hướng Kỹ Năng IT</span>
        </button>
        <button
          className={`tab-btn ${activeTab === 'explorer' ? 'active' : ''}`}
          onClick={() => setActiveTab('explorer')}
        >
          <Database size={16} />
          <span>Tra Cứu Kho Việc Làm</span>
        </button>
      </nav>

      {/* TAB 1: SO KHỚP CV */}
      {activeTab === 'matcher' && (
        <div className="matcher-grid animate-fade-in">
          {/* Cột trái: Form nhập CV */}
          <div className="glass-panel input-section">
            <div className="section-heading">
              <FileText size={20} color="var(--primary)" />
              <span>Dữ Liệu Hồ Sơ CV Ứng Viên</span>
            </div>

            {/* Quick Demo Templates */}
            <div>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '8px', display: 'block' }}>
                ⚡ Tải nhanh hồ sơ ứng viên mẫu để kiểm thử:
              </span>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <button
                  type="button"
                  style={{ fontSize: '11px', padding: '5px 10px', background: 'rgba(255,255,255,0.06)', border: '1px solid var(--border-color)', color: '#fff', borderRadius: '4px', cursor: 'pointer' }}
                  onClick={() => setCvText(CV_TEMPLATES.data_ai)}
                >
                  Kỹ sư Data / AI
                </button>
                <button
                  type="button"
                  style={{ fontSize: '11px', padding: '5px 10px', background: 'rgba(255,255,255,0.06)', border: '1px solid var(--border-color)', color: '#fff', borderRadius: '4px', cursor: 'pointer' }}
                  onClick={() => setCvText(CV_TEMPLATES.devops)}
                >
                  Kỹ sư DevOps / Cloud
                </button>
                <button
                  type="button"
                  style={{ fontSize: '11px', padding: '5px 10px', background: 'rgba(255,255,255,0.06)', border: '1px solid var(--border-color)', color: '#fff', borderRadius: '4px', cursor: 'pointer' }}
                  onClick={() => setCvText(CV_TEMPLATES.fullstack)}
                >
                  Lập trình viên Fullstack
                </button>
              </div>
            </div>

            <textarea
              className="cv-textarea"
              placeholder="Dán nội dung hồ sơ CV hoặc tóm tắt kinh nghiệm làm việc vào đây..."
              value={cvText}
              onChange={(e) => setCvText(e.target.value)}
            />

            <button
              className="btn-primary"
              onClick={handleMatch}
              disabled={isLoading || !cvText.trim()}
            >
              {isLoading ? (
                <>
                  <Sparkles className="animate-spin" size={18} />
                  <span>Đang tính toán Vector Embedding & Xếp hạng RRF...</span>
                </>
              ) : (
                <>
                  <Sparkles size={18} />
                  <span>Phân Tích & So Khớp CV Bằng AI</span>
                </>
              )}
            </button>

            {/* Khung phân tích hồ sơ ứng viên */}
            {matchResult?.candidate && (
              <div className="candidate-badge-card animate-fade-in">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '14px', fontWeight: '700' }}>Thông Tin Ứng Viên Nhận Diện</span>
                  <span style={{ fontSize: '12px', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)' }}>
                    ~{matchResult.candidate.years_of_experience} năm kinh nghiệm
                  </span>
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                  {matchResult.candidate.summary}
                </div>
                <div>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                    Kỹ năng phát hiện theo Taxonomy ({matchResult.candidate.detected_skills.length}):
                  </span>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {matchResult.candidate.detected_skills.map((skill, i) => (
                      <span key={i} className="skill-tag matched" style={{ fontSize: '11px' }}>
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Cột phải: Danh sách việc làm phù hợp */}
          <div className="jobs-list">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <h2 style={{ fontSize: '18px', fontWeight: '700' }}>
                Top Việc Làm Phù Hợp Nhất ({matchResult?.top_matches?.length || 0})
              </h2>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                Xếp hạng qua RRF (Dense Vector Cosine + Sparse BM25)
              </span>
            </div>

            {!matchResult && !isLoading && (
              <div className="glass-panel" style={{ padding: '60px 20px', textAlign: 'center', color: 'var(--text-muted)' }}>
                <Briefcase size={48} style={{ opacity: 0.3, margin: '0 auto 16px' }} />
                <p>Hãy dán CV và nhấn <strong>"Phân Tích & So Khớp CV Bằng AI"</strong> để hệ thống tìm kiếm Top 10 việc làm sát nhất kèm lý do giải thích chi tiết.</p>
              </div>
            )}

            {matchResult?.top_matches?.map(({ job, match_score, matched_skills, missing_skills, reasoning }) => {
              const isExpanded = expandedJobId === job.id;
              const isHigh = match_score >= 80;

              return (
                <div key={job.id} className="job-card animate-fade-in">
                  <div className="job-header">
                    <div>
                      <h3 className="job-title">{job.title}</h3>
                      <div className="job-company">{job.company}</div>
                    </div>
                    <div className={`score-badge ${isHigh ? 'score-high' : 'score-med'}`}>
                      <div>{match_score}%</div>
                      <span className="score-label">Độ Khớp</span>
                    </div>
                  </div>

                  <div className="job-meta-row">
                    <span className="meta-chip">
                      <MapPin size={13} color="var(--accent-cyan)" />
                      {job.location}
                    </span>
                    <span className="meta-chip">
                      <DollarSign size={13} color="var(--accent-emerald)" />
                      {job.salary_range || 'Thỏa thuận'}
                    </span>
                    <span className="meta-chip">
                      <TrendingUp size={13} color="var(--accent-amber)" />
                      {job.experience_level}
                    </span>
                  </div>

                  {/* Nhãn kỹ năng: Xanh (Khớp), Vàng (Còn thiếu) */}
                  <div className="skills-container">
                    {matched_skills.map((s, idx) => (
                      <span key={idx} className="skill-tag matched" title="Kỹ năng bạn đã có">
                        <CheckCircle2 size={12} /> {s}
                      </span>
                    ))}
                    {missing_skills.map((s, idx) => (
                      <span key={idx} className="skill-tag missing" title="Kỹ năng JD yêu cầu nhưng CV chưa có">
                        <AlertCircle size={12} /> {s}
                      </span>
                    ))}
                  </div>

                  {/* Nút đóng/mở giải thích AI */}
                  <button
                    onClick={() => toggleExpand(job.id)}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      color: 'var(--accent-purple)',
                      fontSize: '13px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      padding: 0
                    }}
                  >
                    <span>Lý Do Phù Hợp & Phân Tích Lỗ Hổng Kỹ Năng (AI)</span>
                    {isExpanded ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
                  </button>

                  {/* Khối nội dung giải thích chi tiết */}
                  {isExpanded && (
                    <div className="reasoning-box animate-fade-in">
                      <div className="reasoning-heading">
                        <Sparkles size={14} />
                        <span>Điểm Mạnh Đáp Ứng Yêu Cầu:</span>
                      </div>
                      {reasoning.matched_strengths.map((point, pIdx) => (
                        <div key={pIdx} className="reasoning-point">{point}</div>
                      ))}

                      {reasoning.skill_gaps.length > 0 && (
                        <>
                          <div className="reasoning-heading" style={{ color: 'var(--accent-amber)', marginTop: '12px' }}>
                            <AlertCircle size={14} />
                            <span>Kỹ Năng Cần Chuẩn Bị Thêm:</span>
                          </div>
                          {reasoning.skill_gaps.map((point, pIdx) => (
                            <div key={pIdx} className="reasoning-point" style={{ color: '#fcd34d' }}>{point}</div>
                          ))}
                        </>
                      )}

                      <div className="advice-callout">
                        💡 <strong>Lời khuyên từ Cố vấn Tuyển dụng:</strong> {reasoning.career_advice}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 2: RADAR XU HƯỚNG KỸ NĂNG */}
      {activeTab === 'analytics' && (
        <div className="glass-panel" style={{ padding: '32px' }}>
          <div style={{ marginBottom: '24px' }}>
            <h2 style={{ fontSize: '20px', fontWeight: '800' }}>Radar Xu Hướng Kỹ Năng IT Thị Trường</h2>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
              Dữ liệu được trích xuất và chuẩn hóa theo thời gian thực từ kho tin tuyển dụng trong PostgreSQL.
            </p>
          </div>

          <div className="analytics-grid">
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', marginBottom: '16px', color: 'var(--accent-cyan)' }}>
                Top Công Nghệ Có Nhu Cầu Tuyển Dụng Cao Nhất
              </h3>
              {analyticsData?.top_skills?.map((item, idx) => {
                const max = analyticsData.top_skills[0]?.count || 20;
                const pct = Math.round((item.count / max) * 100);
                return (
                  <div key={idx} className="skill-bar-row">
                    <span className="skill-bar-label">{item.skill}</span>
                    <div className="skill-bar-track">
                      <div className="skill-bar-fill" style={{ width: `${pct}%` }}></div>
                    </div>
                    <span className="skill-bar-count">{item.count} tin</span>
                  </div>
                );
              })}
            </div>

            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', marginBottom: '16px', color: 'var(--accent-purple)' }}>
                Phân Bổ Nhu Cầu Theo Lĩnh Vực
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {analyticsData?.categories?.map((cat, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: 'rgba(255,255,255,0.03)',
                      padding: '14px 18px',
                      borderRadius: '8px',
                      border: '1px solid var(--border-color)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}
                  >
                    <span style={{ fontWeight: '600', fontSize: '14px' }}>{cat.category}</span>
                    <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-cyan)', fontWeight: '700' }}>
                      {cat.count} tin tuyển dụng
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: TRA CỨU KHO VIỆC LÀM */}
      {activeTab === 'explorer' && (
        <div className="glass-panel" style={{ padding: '28px' }}>
          <div style={{ display: 'flex', gap: '14px', marginBottom: '24px', flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: '280px', position: 'relative' }}>
              <input
                type="text"
                placeholder="Tìm việc làm bằng mô tả ngữ nghĩa hoặc từ khóa công nghệ (VD: 'Kubernetes AWS' hoặc 'FastAPI')..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  background: 'rgba(10, 15, 28, 0.8)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  color: 'white',
                  fontSize: '14px'
                }}
              />
            </div>
            <select
              value={selectedLevel}
              onChange={(e) => setSelectedLevel(e.target.value)}
              style={{
                padding: '12px 16px',
                background: 'rgba(10, 15, 28, 0.8)',
                border: '1px solid var(--border-color)',
                borderRadius: '8px',
                color: 'white',
                fontSize: '14px'
              }}
            >
              <option value="">Tất Cả Cấp Bậc Kinh Nghiệm</option>
              <option value="Junior">Mới Đi Làm (Junior)</option>
              <option value="Mid-Level">Trung Cấp (Mid-Level)</option>
              <option value="Senior">Chuyên Viên Cao Cấp (Senior)</option>
            </select>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {jobsList
              .filter(j => !selectedLevel || j.experience_level === selectedLevel)
              .filter(j => !searchQuery || j.title.toLowerCase().includes(searchQuery.toLowerCase()) || j.requirements_clean.toLowerCase().includes(searchQuery.toLowerCase()))
              .map((job) => (
                <div key={job.id} className="job-card" style={{ padding: '20px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                      <h4 style={{ fontSize: '17px', fontWeight: '700', color: '#fff' }}>{job.title}</h4>
                      <span style={{ color: 'var(--accent-cyan)', fontSize: '14px', fontWeight: '600' }}>{job.company}</span>
                    </div>
                    <span className="meta-chip">{job.experience_level}</span>
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: '10px 0' }}>
                    {job.requirements_clean}
                  </p>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {job.skills?.map((s, idx) => (
                      <span key={idx} className="skill-tag matched" style={{ fontSize: '11px' }}>
                        {s.name}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
