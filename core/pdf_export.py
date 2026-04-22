import os
from fpdf import FPDF
from typing import Dict, Any

class ExamPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load custom font for Vietnamese support
        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts", "DejaVuSans.ttf")
        if os.path.exists(font_path):
            self.add_font("DejaVu", "", font_path, uni=True)
        else:
            print(f"Warning: Font file not found at {font_path}. PDF might not render Vietnamese correctly.")
            # Fallback to default font, but it won't support VN well.
            
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Set font
        try:
            self.set_font("DejaVu", "", 10)
        except Exception:
            self.set_font("Arial", "I", 10)
        # Centered text
        self.cell(0, 10, "Bản quyền của Đỗ Khắc Gia Khoa - FPT Aptech", align="C")

def generate_pdf(exam_data: Dict[str, Any], score_dist: Dict[str, float], output_path: str = "exam_output.pdf"):
    """
    Generates a PDF from the exam data.
    """
    pdf = ExamPDF()
    pdf.add_page()
    
    try:
        pdf.set_font("DejaVu", size=16)
    except Exception:
        pdf.set_font("Arial", size=16)
        
    grade = exam_data.get("grade", "")
    test_type = exam_data.get("test_type", "")
    
    # Title
    pdf.cell(0, 10, f"ĐỀ THI TIẾNG ANH - {grade.upper()}", ln=True, align="C")
    pdf.set_font(size=12)
    pdf.cell(0, 10, f"Loại bài thi: {test_type}", ln=True, align="C")
    pdf.ln(10)
    
    questions = exam_data.get("questions", [])
    
    for q in questions:
        q_type = q.get("type")
        q_text = q.get("question", "")
        
        if q_type == "mcq":
            points = score_dist.get("mcq_points", 0)
            pdf.multi_cell(0, 8, f"{q_text} ({points} điểm)")
            
            options = q.get("options", [])
            for opt in options:
                pdf.set_x(20)
                pdf.multi_cell(0, 8, opt)
            pdf.ln(5)
            
        elif q_type == "essay":
            points = score_dist.get("essay_points", 0)
            pdf.multi_cell(0, 8, f"{q_text} ({points} điểm)")
            # Add blank lines for essay answer (approx 5 lines spacing)
            for _ in range(5):
                pdf.ln(8)
                # Optional: draw dotted lines for writing
                # pdf.cell(0, 8, "." * 100) 
            pdf.ln(5)
            
    pdf.output(output_path)
    return output_path
