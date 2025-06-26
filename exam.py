import os
import ctypes
import sys
import time
import random
from docx import Document
import subprocess
import keyboard
import threading
import signal
from questions import questions, run_quiz

exit_flag = False


# Check script Administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Run script with Administrator
def run_as_admin():
    script = sys.executable
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)

# Animation run
def type_print(text, delay=0.03):
    global exit_flag
    for char in text:
        if exit_flag:
            detect_alt_enter()
        if char == '\n':
            sys.stdout.write('\n')
            sys.stdout.flush()
            time.sleep(delay)
        elif char == '\t':
            sys.stdout.write('\t')
            sys.stdout.flush()
            time.sleep(delay)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
    print()

# Exit Exam
def block_ctrl_c(sig, frame):
    type_print("\nKhông được dùng Ctrl + C. Hành vi bị ghi nhận. Nhấn phím '1' để thoát.")
    signal.signal(signal.SIGINT, block_ctrl_c)
    try:
        while True:
            time.sleep(0.1)
            if keyboard.is_pressed('1'):
                print("Tạm biệt!")
                os._exit(0) 
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
    

def wait_to_exit():
    print("Nhấn phím '1' để thoát chương trình.")
    try:
        while True:
            time.sleep(0.1)
            if keyboard.is_pressed('1'):
                print("Tạm biệt!")
                os._exit(0) 
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

# Check action Alt + Enter
def detect_alt_enter():
    global exit_flag
    while True:
        if keyboard.is_pressed('alt') and keyboard.is_pressed('enter'):
            print("\nWARNING!")
            print("- Bạn đã cố tình nhấn Alt + Enter vi phạm ĐIỀU 2.")
            print("- Bài kiểm tra sẽ kết thúc sau vài giây, liên hệ với ADMIN hổ trợ. Cảm ơn!!!")
            exit_flag = True
            time.sleep(10)
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0) 
            sys.exit(0)
        time.sleep(0.1)


# Main
if __name__ == "__main__":
    if sys.platform != "win32":
        print("Chức năng này chỉ hỗ trợ trên Windows.")
        sys.exit(1)

    if not is_admin():
        print("🔒 Chương trình cần chạy với quyền Admin. Đang thử khởi chạy lại...")
        run_as_admin()
        sys.exit(0)
    try:
        keyboard.send('alt + enter')
    except Exception as e:
        print(f"(Không thể gửi phím: {e})")
    # Monitoring Alt + Enter
    threading.Thread(target=detect_alt_enter, daemon=True).start()

    print("\nXIN CHÀO CÁC BẠN - THD CYBER SECURITY")
    # type_print("\t-Tôi là Frederick Nguyễn (admin). Tool này tôi làm ra để hỗ trợ tôi đánh giá các bạn, không phô diễn kĩ năng gì ở đây, Tool sẽ có BUG nếu tìm ra các bạn là thiên tài :v")
    # type_print("\t-Liên hệ hỗ trợ: frederick.nguyen@thdcybersecurity.com\n")
    # print("ĐIỀU KHOẢN:")
    # type_print("\t1/ Nếu sử dụng Ctrl + C thì chương trình sẽ tự động kết thúc bài kiểm tra...")
    # type_print("\t2/ Nếu bạn cố tình sử dụng các tổ hợp phím khác để thoát ra ngoài bài kiểm tra. Chương trình sẽ kết thúc ngay lập tức!...")
    print("CHÚ Ý:")
    type_print("\t- Chỉ được chọn đáp án A | B | C | D | E")
    type_print("\t- Khi chọn đáp án xong, câu trả lời sẽ khóa và tự động chuyển sang câu tiếp theo...")
    type_print("\t- Khi hết thời gian, hệ thống sẽ tự động lưu kết quả và sẽ tự động thoát chương trình...")
    print("\n=======================================START - GOOD LUCK========================================")
    time.sleep(5)
    

    # Run Question
    # random_question()
    run_quiz()
    print("\n🎉 Đã hoàn thành bài kiểm tra. Cảm ơn bạn đã tham gia!")

    # Run "1" Exit
    # block_ctrl_c()
    wait_to_exit()
