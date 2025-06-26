import os
import ctypes
import sys
import time
from datetime import datetime, timedelta
import random
from docx import Document

# Kiểm tra quyền admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Chạy lại script với quyền admin
def run_as_admin():
    script = sys.executable
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)

# Đọc câu hỏi từ file docx
def load_questions_from_docx(read_docx_file):
    try:
        doc = Document(read_docx_file)
    except Exception as e:
        print(f"❌ Không thể đọc file Word: {e}")
        sys.exit(1)

    questions = []
    buffer = {}
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if text.startswith("Câu "):
            if buffer:
                questions.append(buffer)
                buffer = {}
            buffer["question"] = text
            buffer["options"] = {}

        elif text.startswith("•") or text.startswith("-"):
            option_line = text[1:].strip()
            if '.' in option_line:
                key = option_line[0].upper()
                value = option_line[2:].strip()
                buffer["options"][key] = value

        elif text.lower().startswith("đáp án"):
            buffer["answer"] = text.strip()[-1].upper()

    if buffer:
        questions.append(buffer)

    return questions

# =========================== MAIN =============================

if __name__ == "__main__":
    if sys.platform != "win32":
        print("Chức năng này chỉ hỗ trợ trên Windows.")
        sys.exit(1)

    if not is_admin():
        print("🔒 Chương trình cần chạy với quyền Admin. Đang thử khởi chạy lại...")
        time.sleep(2)
        run_as_admin()
        sys.exit(0)

    print("✅ Đang chạy với quyền Admin...\n")

    # file_path = "D:\python_source\SOC_Exam\source\Splunk.docx"

    # Đọc câu hỏi
    questions = load_questions_from_docx(file_path)
    if not questions:
        print("❌ Không tìm thấy câu hỏi trong file.")
        sys.exit(1)

    # Shuffle câu hỏi và đáp án
    random.shuffle(questions)
    for q in questions:
        original_options = list(q["options"].items())
        random.shuffle(original_options)

        shuffled_options = {}
        correct_answer_text = q["options"][q["answer"]]
        new_answer_key = None

        for idx, (key, value) in enumerate(original_options):
            new_key = chr(65 + idx)
            shuffled_options[new_key] = value
            if value == correct_answer_text:
                new_answer_key = new_key

        q["options"] = shuffled_options
        q["answer"] = new_answer_key

    score = 0
    answers_log = []
    result_file = "ket_qua.txt"

    print("📝 Bắt đầu làm bài! Bạn có 20 phút. Trả lời nhanh!\n")

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=5)
    total_seconds = int((end_time - start_time).total_seconds())
    timer_start = time.time()

    for q in questions:
        elapsed = time.time() - timer_start
        remaining = total_seconds - int(elapsed)

        if remaining <= 0:
            print("\n⏰ Hết giờ! Tự động nộp bài.")
            break

        mins, secs = divmod(remaining, 60)
        print(f"\n⏳ {q['question']} (Còn lại: {mins:02d}:{secs:02d})")
        for key, value in q["options"].items():
            print(f"  {key}. {value}")

        while True:
            answer = input("Chọn đáp án (A/B/C/D/E): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D', 'E']:
                break
            else:
                print("Vui lòng nhập A, B, C hoặc D.")

        correct = answer == q["answer"]
        result = "[Đúng]" if correct else f"[Sai] (Đúng: {q['answer']})"
        print(f"{result}\n")
        answers_log.append(f"{q['question']}\nTrả lời: {answer} {result}\n")
        if correct:
            score += 1

    percent = (score / len(questions)) * 100
    summary = f"\n🎯 Số câu đúng: {score}/{len(questions)}\n📊 Tỷ lệ đúng: {percent:.2f}%\n🕒 Thời gian làm bài: {datetime.now() - start_time}\n"

    with open(result_file, "w", encoding="utf-8") as f:
        f.write("\n".join(answers_log))
        f.write(summary)

    print(summary)
