import os
import fitz  # PyMuPDF
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

# --- Job keywords dictionary (extendable to 30 roles) ---
job_keywords = {
    "Software Engineer": ["python", "java", "c++", "algorithms", "data structures", "api", "git"],
    "Data Analyst": ["excel", "sql", "tableau", "statistics", "python", "power bi", "data visualization"],
    "Graphic Designer": ["photoshop", "illustrator", "indesign", "figma", "creativity", "branding"],
    "Marketing Associate": ["seo", "content", "campaign", "social media", "google ads", "branding"],
    "Sales Representative": ["sales", "negotiation", "crm", "pipeline", "closing", "customer"],
    "Product Manager": ["roadmap", "agile", "scrum", "strategy", "stakeholders", "kpis"],
    "HR Coordinator": ["recruitment", "employee", "onboarding", "payroll", "compliance"],
    "Customer Support": ["customer", "support", "ticketing", "communication", "troubleshooting"],
    "Business Analyst": ["requirements", "workflow", "process", "excel", "sql", "reporting"],
    "Content Writer": ["writing", "seo", "editing", "copywriting", "blog", "articles"],

    # New roles
    "Web Developer": ["html", "css", "javascript", "react", "node", "php", "api", "git"],
    "Data Scientist": ["python", "machine learning", "deep learning", "statistics", "pandas", "numpy", "modeling"],
    "AI Engineer": ["neural networks", "tensorflow", "pytorch", "nlp", "computer vision", "ai"],
    "Cloud Engineer": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "cloud"],
    "Cybersecurity Analyst": ["security", "firewall", "penetration testing", "encryption", "network", "threats"],
    "Network Engineer": ["network", "tcp/ip", "routing", "switching", "firewall", "vpn"],
    "Database Administrator": ["sql", "oracle", "postgresql", "backup", "performance tuning", "security"],
    "DevOps Engineer": ["ci/cd", "docker", "kubernetes", "jenkins", "monitoring", "cloud"],
    "UI/UX Designer": ["figma", "wireframe", "prototype", "user research", "adobe xd", "accessibility"],
    "Mobile App Developer": ["android", "ios", "flutter", "react native", "swift", "kotlin"],

    "Financial Analyst": ["excel", "valuation", "forecasting", "financial modeling", "reporting", "budgeting"],
    "Accountant": ["accounting", "tax", "audit", "bookkeeping", "excel", "compliance"],
    "Project Manager": ["project plan", "agile", "scrum", "kanban", "timeline", "stakeholders"],
    "Operations Manager": ["operations", "efficiency", "logistics", "kpis", "process improvement"],
    "Healthcare Administrator": ["healthcare", "patient", "records", "compliance", "policy", "coordination"],
    "Teacher": ["teaching", "curriculum", "lesson plan", "classroom", "assessment", "communication"],
    "Lawyer": ["legal", "contracts", "litigation", "compliance", "negotiation", "advice"],
    "Research Scientist": ["research", "experiments", "data analysis", "publication", "hypothesis", "lab"],
    "Mechanical Engineer": ["cad", "solidworks", "manufacturing", "mechanical", "design", "analysis"],
    "Civil Engineer": ["autocad", "construction", "surveying", "estimation", "project", "structural"]
}

# --- Extract text from PDF ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.lower()

# --- Analyze resume ---
def analyze_resume(resume_text, job_title):
    if job_title not in job_keywords:
        return 50, "Job title not recognized. Please select a valid one."

    keywords = job_keywords[job_title]
    found = [kw for kw in keywords if kw in resume_text]

    score = int((len(found) / len(keywords)) * 100)

    if score > 80:
        feedback = f"Excellent! Your resume is highly relevant for {job_title}. Keywords matched: {', '.join(found)}."
    elif score > 50:
        feedback = f"Good resume, but you can improve it for {job_title}. Missing some keywords: {', '.join(set(keywords) - set(found))}."
    else:
        feedback = f"Needs improvement. Your resume lacks many important {job_title} skills. Try adding: {', '.join(set(keywords) - set(found))}."

    return score, feedback

# --- Routes ---
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        job_title = request.form['job_title']
        file = request.files['resume']

        if file and file.filename.endswith('.pdf'):
            pdf_path = os.path.join("uploads", file.filename)
            file.save(pdf_path)

            resume_text = extract_text_from_pdf(pdf_path)
            score, feedback, matched, missing = analyze_resume(resume_text, job_title)

            return render_template(
                "result.html",
                score=score,
                feedback=feedback,
                job_title=job_title,
                matched=matched,
                missing=missing
            )

    return render_template("upload.html", job_titles=list(job_keywords.keys()))


def analyze_resume(resume_text, job_title):
    if job_title not in job_keywords:
        return 50, "Job title not recognized. Please select a valid one.", [], []

    keywords = job_keywords[job_title]
    found = [kw for kw in keywords if kw in resume_text]
    missing = list(set(keywords) - set(found))

    score = int((len(found) / len(keywords)) * 100)

    if score > 80:
        feedback = f"Excellent! Your resume is highly relevant for {job_title}."
    elif score > 50:
        feedback = f"Good resume, but you can improve it for {job_title}."
    else:
        feedback = f"Needs improvement. Your resume lacks many important {job_title} skills."

    return score, feedback, found, missing


@app.route('/download_report')
def download_report():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    job_title = request.args.get("job_title", "Unknown Job")
    score = request.args.get("score", 0, type=int)
    feedback = request.args.get("feedback", "No feedback provided")
    matched = request.args.get("matched", "").split(",") if request.args.get("matched") else []
    missing = request.args.get("missing", "").split(",") if request.args.get("missing") else []

    file_path = f"report_{job_title}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "📄 Resume Analysis Report")

    # Job details
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Job Title: {job_title}")
    c.drawString(100, 700, f"Score: {score}%")

    # Feedback
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 670, "Feedback:")
    c.setFont("Helvetica", 11)
    c.drawString(120, 650, feedback)

    # Matched keywords
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 620, "✅ Matched Keywords:")
    text_obj = c.beginText(120, 600)
    text_obj.setFont("Helvetica", 11)
    text_obj.textLines(", ".join(matched) if matched else "None")
    c.drawText(text_obj)

    # Missing keywords
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 570, "❌ Missing Keywords:")
    text_obj = c.beginText(120, 550)
    text_obj.setFont("Helvetica", 11)
    text_obj.textLines(", ".join(missing) if missing else "None")
    c.drawText(text_obj)

    c.save()
    return send_file(file_path, as_attachment=True)



if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
