import streamlit as st
import os
from core.generator import generate_exam_content, calculate_score_distribution
from core.pdf_export import generate_pdf

st.set_page_config(page_title="English Exam Generator", page_icon="📝", layout="centered")

st.title("📝 English Exam Generator")
st.markdown("Tạo đề thi Tiếng Anh nhanh chóng cho học sinh từ Lớp 1 đến Lớp 10.")

# Initialize global used questions set
if 'used_questions' not in st.session_state:
    st.session_state['used_questions'] = set()

with st.sidebar:
    st.header("⚙️ Cài đặt")
    st.markdown("Các câu hỏi đã sinh ra sẽ được lưu lại để tránh trùng lặp cho các đề thi tiếp theo.")
    if st.button("Làm mới Ngân hàng Câu hỏi"):
        st.session_state['used_questions'] = set()
        st.success("Đã làm mới!")

# --- UI Layout ---
col1, col2 = st.columns(2)

with col1:
    grade = st.selectbox(
        "Chọn Khối Lớp",
        [f"Lớp {i}" for i in range(1, 11)],
        help="Chọn lớp từ Lớp 1 đến Lớp 10"
    )
    
    test_type = st.selectbox(
        "Loại Bài Thi",
        ["Trắc nghiệm", "Tự luận", "Kết hợp"],
        help="Chọn hình thức của đề thi"
    )
    
with col2:
    duration_length_options = {
        "15 phút - 20 câu": (15, 20),
        "60 phút - 50 câu": (60, 50),
        "90 phút - 70 câu": (90, 70)
    }
    duration_choice = st.selectbox(
        "Thời gian & Số lượng câu hỏi",
        list(duration_length_options.keys())
    )

# Dynamic Hybrid Ratio
hybrid_ratio = 100
if test_type == "Kết hợp":
    hybrid_ratio = st.slider(
        "Tỉ lệ Trắc nghiệm / Tự luận (%)",
        min_value=0, max_value=100, value=70, step=5,
        help="Ví dụ: 70% Trắc nghiệm, 30% Tự luận."
    )
    st.caption(f"Chi tiết: {hybrid_ratio}% Trắc nghiệm - {100 - hybrid_ratio}% Tự luận")
elif test_type == "Trắc nghiệm":
    hybrid_ratio = 100
elif test_type == "Tự luận":
    hybrid_ratio = 0

st.write("---")

if st.button("Tạo Đề Thi", type="primary"):
    with st.spinner("Đang tạo đề thi..."):
        total_time, total_questions = duration_length_options[duration_choice]
        
        # Calculate question counts
        mcq_count = int(total_questions * (hybrid_ratio / 100.0))
        essay_count = total_questions - mcq_count
        
        # Calculate points
        score_dist = calculate_score_distribution(mcq_count, essay_count, hybrid_ratio)
        
        # Generate Content
        exam_data = generate_exam_content(grade, test_type, mcq_count, essay_count, st.session_state['used_questions'])
        
        # Update used questions
        st.session_state['used_questions'].update(exam_data['generated_ids'])
        
        # Save to Session State for persistence
        st.session_state['exam_data'] = exam_data
        st.session_state['score_dist'] = score_dist
        st.session_state['total_time'] = total_time
        st.session_state['total_questions'] = total_questions
        st.session_state['mcq_count'] = mcq_count
        st.session_state['essay_count'] = essay_count
        
        # Reset grading state
        if 'user_answers' in st.session_state:
            del st.session_state['user_answers']
        if 'show_results' in st.session_state:
            del st.session_state['show_results']

# Render the exam if it exists in session state
if 'exam_data' in st.session_state:
    exam_data = st.session_state['exam_data']
    score_dist = st.session_state['score_dist']
    
    st.success("Tạo đề thi thành công!")
    st.subheader("Thông tin đề thi")
    st.write(f"**{exam_data['grade']}** - **{exam_data['test_type']}**")
    st.write(f"**Phân bổ điểm:** Trắc nghiệm: {score_dist['mcq_points']} điểm/câu | Tự luận: {score_dist['essay_points']} điểm/câu")
    
    # Generate and provide PDF Download
    os.makedirs("output", exist_ok=True)
    pdf_filename = f"DeThi_{exam_data['grade'].replace(' ', '')}_{exam_data['test_type'].replace(' ', '')}.pdf"
    pdf_path = os.path.join("output", pdf_filename)
    generate_pdf(exam_data, score_dist, pdf_path)
    
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="📥 Xuất PDF",
            data=file,
            file_name=pdf_filename,
            mime="application/pdf"
        )
        
    st.write("---")
    st.subheader("Làm bài trực tuyến")
    
    if 'user_answers' not in st.session_state:
        st.session_state['user_answers'] = {}
        
    for idx, q in enumerate(exam_data['questions'], 1):
        st.markdown(f"**{q['question']}**")
        
        if q['type'] == 'mcq':
            # Store the selected option in session state via the key param
            selected = st.radio(
                label=f"Chọn đáp án cho câu {idx}",
                options=q['options'],
                key=f"q_{idx}",
                label_visibility="collapsed",
                index=None # No default selection
            )
            
            # Save the answer locally in our dict
            st.session_state['user_answers'][idx] = selected
            
            # Show grading feedback if submitted
            if st.session_state.get('show_results', False):
                correct_letter = q['correct_answer']
                user_letter = selected[0] if selected else ""
                
                if user_letter == correct_letter:
                    st.success(f"✅ Đúng! Đáp án là {correct_letter}")
                else:
                    st.error(f"❌ Sai. Đáp án đúng là {correct_letter}")
                    
        elif q['type'] == 'essay':
            st.text_area("Câu trả lời của bạn:", key=f"essay_{idx}")
            
        st.write("")
        
    # Grade Button
    if st.button("📝 Chấm Điểm", type="primary"):
        st.session_state['show_results'] = True
        st.rerun()

    # Show Final Score Panel
    if st.session_state.get('show_results', False):
        st.write("---")
        st.header("🏆 Kết quả bài làm (Phần Trắc Nghiệm)")
        
        total_mcq_score = 0.0
        correct_count = 0
        mcq_total = 0
        
        for idx, q in enumerate(exam_data['questions'], 1):
            if q['type'] == 'mcq':
                mcq_total += 1
                correct_letter = q['correct_answer']
                user_selected = st.session_state['user_answers'].get(idx, None)
                user_letter = user_selected[0] if user_selected else ""
                
                if user_letter == correct_letter:
                    total_mcq_score += score_dist['mcq_points']
                    correct_count += 1
                    
        st.metric(label="Số câu trắc nghiệm đúng", value=f"{correct_count} / {mcq_total}")
        st.metric(label="Điểm trắc nghiệm", value=f"{round(total_mcq_score, 2)} / {round(score_dist['mcq_points'] * mcq_total, 2)} điểm")
        
        if st.session_state['essay_count'] > 0:
            st.info("ℹ️ Phần tự luận sẽ do giáo viên chấm điểm thủ công.")
