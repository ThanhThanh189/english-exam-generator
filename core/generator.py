import random
from typing import List, Dict, Any, Set

def get_grade_group(grade_str: str) -> str:
    """Helper to categorize grades into groups"""
    try:
        grade_num = int(grade_str.split()[1])
    except Exception:
        grade_num = 1
        
    if 1 <= grade_num <= 3:
        return "1_3"
    elif 4 <= grade_num <= 5:
        return "4_5"
    elif 6 <= grade_num <= 8:
        return "6_8"
    else:
        return "9_10"

# Dữ liệu giả lập mô phỏng các format câu hỏi từ Study4
QUESTION_BANK = {
    "1_3": {
        "mcq": [
            ("mcq_1_001", "What color is an apple?", ["A. Blue", "B. Red", "C. Yellow", "D. Black"], "B"),
            ("mcq_1_002", "How many legs does a dog have?", ["A. Two", "B. Three", "C. Four", "D. Five"], "C"),
            ("mcq_1_003", "Choose the correct word: This ___ a cat.", ["A. am", "B. is", "C. are", "D. be"], "B"),
            ("mcq_1_004", "I ___ a boy.", ["A. is", "B. am", "C. are", "D. be"], "B"),
            ("mcq_1_005", "What is your ___? - My name is Tom.", ["A. age", "B. color", "C. name", "D. school"], "C"),
            ("mcq_1_006", "The sun is ___.", ["A. cold", "B. hot", "C. green", "D. small"], "B"),
            ("mcq_1_007", "I have two ___.", ["A. ear", "B. ears", "C. eares", "D. earing"], "B"),
            ("mcq_1_008", "She is my ___.", ["A. brother", "B. father", "C. sister", "D. uncle"], "C"),
            ("mcq_1_009", "There ___ an apple on the table.", ["A. is", "B. are", "C. am", "D. be"], "A"),
            ("mcq_1_010", "___ you like milk? - Yes, I do.", ["A. Does", "B. Do", "C. Are", "D. Is"], "B")
        ],
        "essay": [
            ("essay_1_001", "Write 2 sentences about your family."),
            ("essay_1_002", "What is your favorite animal? Why?"),
            ("essay_1_003", "Describe your school bag (color, items inside)."),
            ("essay_1_004", "Write about what you do in the morning.")
        ]
    },
    "4_5": {
        "mcq": [
            ("mcq_4_001", "He usually ___ up at 6 AM.", ["A. get", "B. gets", "C. getting", "D. got"], "B"),
            ("mcq_4_002", "They ___ playing football right now.", ["A. is", "B. am", "C. are", "D. be"], "C"),
            ("mcq_4_003", "___ did you go yesterday? - I went to the zoo.", ["A. What", "B. When", "C. Where", "D. Why"], "C"),
            ("mcq_4_004", "This book is ___ than that one.", ["A. thick", "B. thicker", "C. thickest", "D. more thick"], "B"),
            ("mcq_4_005", "I would like ___ orange juice.", ["A. some", "B. a", "C. an", "D. any"], "A"),
            ("mcq_4_006", "Did you ___ your homework?", ["A. do", "B. does", "C. doing", "D. did"], "A"),
            ("mcq_4_007", "The weather is very ___ today.", ["A. sun", "B. sunny", "C. sunning", "D. suns"], "B"),
            ("mcq_4_008", "She has ___ dog and two cats.", ["A. an", "B. some", "C. a", "D. the"], "C"),
            ("mcq_4_009", "My birthday is ___ May 5th.", ["A. in", "B. on", "C. at", "D. from"], "B"),
            ("mcq_4_010", "What time ___ it? - It's 10 o'clock.", ["A. are", "B. does", "C. do", "D. is"], "D")
        ],
        "essay": [
            ("essay_4_001", "Write a short paragraph about your best friend."),
            ("essay_4_002", "Describe a trip you went on with your family."),
            ("essay_4_003", "What do you want to be when you grow up?"),
            ("essay_4_004", "Write an email to a friend about your weekend.")
        ]
    },
    "6_8": {
        "mcq": [
            ("mcq_6_001", "If I ___ you, I would study harder.", ["A. am", "B. was", "C. were", "D. been"], "C"),
            ("mcq_6_002", "She is interested ___ reading books.", ["A. on", "B. in", "C. at", "D. about"], "B"),
            ("mcq_6_003", "The man ___ is standing there is my uncle.", ["A. which", "B. whom", "C. who", "D. whose"], "C"),
            ("mcq_6_004", "I have studied English ___ 5 years.", ["A. since", "B. for", "C. in", "D. at"], "B"),
            ("mcq_6_005", "Choose the synonym of 'Difficult':", ["A. Hard", "B. Easy", "C. Simple", "D. Quick"], "A"),
            ("mcq_6_006", "He told me that he ___ a new car the next day.", ["A. buys", "B. will buy", "C. would buy", "D. bought"], "C"),
            ("mcq_6_007", "Water boils ___ 100 degrees Celsius.", ["A. in", "B. on", "C. at", "D. from"], "C"),
            ("mcq_6_008", "You should give ___ smoking.", ["A. up", "B. in", "C. on", "D. out"], "A"),
            ("mcq_6_009", "The film was so ___ that we fell asleep.", ["A. bore", "B. boring", "C. bored", "D. boredom"], "B"),
            ("mcq_6_010", "He is the boy ___ bicycle was stolen.", ["A. who", "B. whom", "C. whose", "D. which"], "C")
        ],
        "essay": [
            ("essay_6_001", "Write a short essay on the benefits of reading."),
            ("essay_6_002", "Do you prefer living in the city or the countryside? Explain."),
            ("essay_6_003", "Describe a memorable event in your life."),
            ("essay_6_004", "How can students help protect the environment?")
        ]
    },
    "9_10": {
        "mcq": [
            ("mcq_9_001", "Despite ___, he went to work.", ["A. he was sick", "B. his sickness", "C. sick", "D. was sick"], "B"),
            ("mcq_9_002", "Not until I came back ___ that she had left.", ["A. I realized", "B. did I realize", "C. do I realize", "D. realized I"], "B"),
            ("mcq_9_003", "By the time you arrive, I ___ my work.", ["A. will finish", "B. have finished", "C. will have finished", "D. had finished"], "C"),
            ("mcq_9_004", "I'd rather you ___ here.", ["A. stay", "B. stayed", "C. staying", "D. to stay"], "B"),
            ("mcq_9_005", "It is essential that he ___ the meeting.", ["A. attend", "B. attends", "C. attended", "D. attending"], "A"),
            ("mcq_9_006", "The new policy will be implemented ___ January 1st.", ["A. in", "B. on", "C. at", "D. by"], "B"),
            ("mcq_9_007", "Scarcely had she entered the room ___ the phone rang.", ["A. than", "B. when", "C. then", "D. while"], "B"),
            ("mcq_9_008", "He was accused ___ stealing the money.", ["A. for", "B. with", "C. of", "D. about"], "C"),
            ("mcq_9_009", "Identify the error: She didn't wrote the letter.", ["A. She", "B. didn't", "C. wrote", "D. the letter"], "C"),
            ("mcq_9_010", "Choose the antonym of 'Abundant':", ["A. Plentiful", "B. Scarce", "C. Copious", "D. Ample"], "B")
        ],
        "essay": [
            ("essay_9_001", "Discuss the impact of technology on education."),
            ("essay_9_002", "What are the advantages and disadvantages of studying abroad?"),
            ("essay_9_003", "Write a letter of complaint about a defective product."),
            ("essay_9_004", "Some people think that university education should be free. To what extent do you agree?")
        ]
    }
}

def generate_exam_content(grade: str, test_type: str, mcq_count: int, essay_count: int, used_ids: Set[str] = None) -> Dict[str, Any]:
    if used_ids is None:
        used_ids = set()
        
    grade_group = get_grade_group(grade)
    bank_mcq = QUESTION_BANK[grade_group]["mcq"]
    bank_essay = QUESTION_BANK[grade_group]["essay"]
    
    questions = []
    generated_ids = []
    
    # Lọc các câu trắc nghiệm chưa dùng
    available_mcq = [q for q in bank_mcq if q[0] not in used_ids]
    
    for i in range(mcq_count):
        if not available_mcq:
            # Nếu ngân hàng cạn kiệt, reset bank cho lượt này và trộn lại
            available_mcq = list(bank_mcq)
            random.shuffle(available_mcq)
            
        selected_idx = random.randrange(len(available_mcq))
        selected = available_mcq.pop(selected_idx)
        q_id, q_text, opts, correct_ans = selected
        
        # Nếu ID đã có trong used_ids hoặc generated_ids tức là phải dùng lại
        # (Đã bỏ logic thêm marker Variant theo yêu cầu)
            
        generated_ids.append(q_id)
        
        questions.append({
            "id": q_id,
            "type": "mcq",
            "question": f"Question {i+1}: {q_text}",
            "options": opts,
            "correct_answer": correct_ans
        })

    # Lọc các câu tự luận chưa dùng
    available_essay = [q for q in bank_essay if q[0] not in used_ids]
    
    for i in range(essay_count):
        if not available_essay:
            available_essay = list(bank_essay)
            random.shuffle(available_essay)
            
        selected_idx = random.randrange(len(available_essay))
        selected = available_essay.pop(selected_idx)
        q_id, q_text = selected
        

            
        generated_ids.append(q_id)
        
        questions.append({
            "id": q_id,
            "type": "essay",
            "question": f"Question {i+1 + mcq_count}: {q_text}"
        })
        
    return {
        "grade": grade,
        "test_type": test_type,
        "questions": questions,
        "generated_ids": generated_ids
    }

def calculate_score_distribution(total_mcq: int, total_essay: int, hybrid_ratio: int = 100) -> Dict[str, float]:
    total_score = 100.0
    
    if total_mcq == 0 and total_essay > 0:
        return {"mcq_points": 0.0, "essay_points": total_score / total_essay}
    elif total_essay == 0 and total_mcq > 0:
        return {"mcq_points": total_score / total_mcq, "essay_points": 0.0}
    elif total_mcq > 0 and total_essay > 0:
        mcq_total_score = total_score * (hybrid_ratio / 100.0)
        essay_total_score = total_score - mcq_total_score
        
        mcq_points = mcq_total_score / total_mcq
        essay_points = essay_total_score / total_essay
        
        return {"mcq_points": round(mcq_points, 2), "essay_points": round(essay_points, 2)}
    
    return {"mcq_points": 0.0, "essay_points": 0.0}
