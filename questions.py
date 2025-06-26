import os
import ctypes
import sys
import time
from datetime import datetime, timedelta
import random
from docx import Document
import subprocess
import keyboard
import threading
import signal
import tkinter as tk
time_up = False


questions = [
    {
        "question": "1. What is the primary purpose of digital forensics?",
        "options": {
            "A": "To enhance system performance",
            "B": "To recover lost data",
            "C": "To investigate cyber crimes",
            "D": "To install security updates",
            "E": "To increase hardware efficiency"
        },
        "answer": "C"
    },
    {
        "question": "2. Which tool is widely used for disk imaging in open-source forensic investigations on Linux?",
        "options": {
            "A": "EnCase",
            "B": "FTK Imager",
            "C": "dd",
            "D": "XWays Forensics",
            "E": "ProDiscover"
        },
        "answer": "C"
    },
    {
        "question": "3. In Windows forensics, which file system is commonly analyzed for recovery of deleted files?",
        "options": {
            "A": "FAT32",
            "B": "NTFS",
            "C": "HFS+",
            "D": "ext3",
            "E": "APFS"
        },
        "answer": "B"
    },
    {
        "question": "4. What does the term 'volatile data' refer to in a forensic context?",
        "options": {
            "A": "Data that is stored permanently",
            "B": "Data that is easily recoverable",
            "C": "Data that is lost when power is off",
            "D": "Data that is backed up regularly",
            "E": "Data that is encrypted"
        },
        "answer": "C"
    },
    {
        "question": "5. Which command in Linux can you use to analyze file access timestamps?",
        "options": {
            "A": "ls -l",
            "B": "stat",
            "C": "touch",
            "D": "cat",
            "E": "grep"
        },
        "answer": "B"
    },
    {
        "question": "6. In the context of forensic analysis, what is the main function of a write-blocker?",
        "options": {
            "A": "To enhance the evidence-gathering process",
            "B": "To prevent any modifications to the original data",
            "C": "To increase file recovery rates",
            "D": "To magnify data for better analysis",
            "E": "To compress data for storage"
        },
        "answer": "B"
    },
    {
        "question": "7. Which Windows feature can provide insights into a user’s actions through its logs?",
        "options": {
            "A": "Task Manager",
            "B": "Event Viewer",
            "C": "Control Panel",
            "D": "Registry Editor",
            "E": "Command Prompt"
        },
        "answer": "B"
    },
    {
        "question": "8. What is the main benefit of using file hashing in forensic investigations?",
        "options": {
            "A": "To compress files for storage",
            "B": "To ensure data integrity and authenticity",
            "C": "To speed up file transfers",
            "D": "To encrypt sensitive information",
            "E": "To categorize files quickly"
        },
        "answer": "B"
    },
    {
        "question": "9. Which Linux command can be used to view and extract log files for forensic analysis?",
        "options": {
            "A": "mv",
            "B": "cp",
            "C": "tail",
            "D": "rm",
            "E": "echo"
        },
        "answer": "C"
    },
    {
        "question": "10. In Windows, which of the following tools is a popular choice for malware analysis and forensic investigation?",
        "options": {
            "A": "Wireshark",
            "B": "Volatility",
            "C": "Oxygen Forensic Detective",
            "D": "Char Leslie",
            "E": "PowerShell"
        },
        "answer": "B"
    },
    {
        "question": "11. What is the primary purpose of digital forensics?",
        "options": {
            "A": "To secure networks",
            "B": "To recover lost files",
            "C": "To analyze and preserve digital evidence",
            "D": "To prevent cyber attacks",
            "E": "To create software updates"
        },
        "answer": "C"
    },
    {
        "question": "12. Which tool is commonly used for forensic analysis of Windows operating systems?",
        "options": {
            "A": "Autopsy",
            "B": "Sleuth Kit",
            "C": "EnCase",
            "D": "Wireshark",
            "E": "Nmap"
        },
        "answer": "C"
    },
    {
        "question": "13. Which filesystem analysis tool is specifically designed for Linux systems?",
        "options": {
            "A": "FTK Imager",
            "B": "XFS",
            "C": "Ext4",
            "D": "TSK",
            "E": "GIMP"
        },
        "answer": "D"
    },
    {
        "question": "14. What is the significance of a write blocker in forensic investigations?",
        "options": {
            "A": "It increases the speed of data retrieval",
            "B": "It prevents modification of original evidence",
            "C": "It allows for data encryption",
            "D": "It simplifies data transfer",
            "E": "It enhances data security"
        },
        "answer": "B"
    },
    {
        "question": "15. In Windows forensics, which artifact can provide insights into user activity?",
        "options": {
            "A": "Registry hives",
            "B": "Swap files",
            "C": "Log files",
            "D": "Page files",
            "E": "All of the above"
        },
        "answer": "E"
    },
    {
        "question": "16. Which of the following commands is essential for retrieving information on active processes in Linux?",
        "options": {
            "A": "ls",
            "B": "ps",
            "C": "df",
            "D": "top",
            "E": "pwd"
        },
        "answer": "B"
    },
    {
        "question": "17. What is the primary purpose of the fmemdump tool in Linux forensics?",
        "options": {
            "A": "To analyze network traffic",
            "B": "To recover deleted files",
            "C": "To create memory images",
            "D": "To perform disk imaging",
            "E": "To generate user activity logs"
        },
        "answer": "C"
    },
    {
        "question": "18. Which file extension typically indicates a file that contains system logs in Windows?",
        "options": {
            "A": ".log",
            "B": ".bin",
            "C": ".exe",
            "D": ".txt",
            "E": ".dll"
        },
        "answer": "A"
    },
    {
        "question": "19. In Linux forensics, what is the term for recovering data from a damaged file system?",
        "options": {
            "A": "Data carving",
            "B": "Data cloning",
            "C": "Data restoration",
            "D": "Data encryption",
            "E": "Data fragmentation"
        },
        "answer": "A"
    },
    {
        "question": "20. Which of the following is a common challenge faced by forensic investigators in both Windows and Linux environments?",
        "options": {
            "A": "Unexpected file formats",
            "B": "Encryption of data",
            "C": "Mobile device forensics",
            "D": "Cloud storage access",
            "E": "All of the above"
        },
        "answer": "E"
    },
    {
        "question": "21. What is the primary purpose of forensic analysis in computing?",
        "options": {
            "A": "To enhance system performance",
            "B": "To restore deleted files",
            "C": "To collect and analyze evidence from digital devices",
            "D": "To install software updates",
            "E": "To improve user interface design"
        },
        "answer": "C"
    },
    {
        "question": "22. Which tool is commonly used for disk imaging in both Windows and Linux environments?",
        "options": {
            "A": "WinRAR",
            "B": "DD",
            "C": "Notepad",
            "D": "MS Paint",
            "E": "VLC"
        },
        "answer": "B"
    },
    {
        "question": "23. What file system is primarily associated with Windows operating systems?",
        "options": {
            "A": "ext4",
            "B": "FAT32",
            "C": "Btrfs",
            "D": "NTFS",
            "E": "HFS+"
        },
        "answer": "D"
    },
    {
        "question": "24. In Linux forensic investigations, which command can be used to recover deleted files from ext3 or ext4 file systems?",
        "options": {
            "A": "rm",
            "B": "recover",
            "C": "extundelete",
            "D": "format",
            "E": "cp"
        },
        "answer": "C"
    },
    {
        "question": "25. Which Windows tool allows you to analyze system logs for forensic investigations?",
        "options": {
            "A": "Event Viewer",
            "B": "Disk Cleanup",
            "C": "Task Manager",
            "D": "Command Prompt",
            "E": "Control Panel"
        },
        "answer": "A"
    },
    {
        "question": "26. What is a common method of preserving volatile data in digital forensics?",
        "options": {
            "A": "Rebooting the system",
            "B": "Taking a screenshot",
            "C": "Using a memory dump tool",
            "D": "Copying to a USB stick",
            "E": "Running a virus scan"
        },
        "answer": "C"
    },
    {
        "question": "27. Which of the following is NOT a common file format for digital evidence?",
        "options": {
            "A": ".csv",
            "B": ".jpg",
            "C": ".e01",
            "D": ".exe",
            "E": ".txt"
        },
        "answer": "D"
    },
    {
        "question": "28. In the context of Linux forensics, what does the term 'live acquisition' refer to?",
        "options": {
            "A": "Analyzing data on a powered-off machine",
            "B": "Capturing data from a running system",
            "C": "Running a malware analysis tool",
            "D": "Streaming data over a network",
            "E": "Creating backup images of files"
        },
        "answer": "B"
    },
    {
        "question": "29. Which Windows artifact can provide details about recently accessed files and folders?",
        "options": {
            "A": "Recycle Bin",
            "B": "Prefetch",
            "C": "Firewall log",
            "D": "System32",
            "E": "Control Panel settings"
        },
        "answer": "B"
    },
    {
        "question": "30. What is a digital signature and how is it relevant to forensics?",
        "options": {
            "A": "A method to encrypt files",
            "B": "A way to verify the integrity of files",
            "C": "A tool to delete files permanently",
            "D": "A component of email spoofing",
            "E": "A technique for file compression"
        },
        "answer": "B"
    }
]


def countdown_window(seconds):
    def update():
        nonlocal seconds
        mins, secs = divmod(seconds, 60)
        label.config(text=f"{mins:02}:{secs:02}")
        if seconds > 0:
            seconds -= 1
            root.after(1000, update)
        else:
            global time_up
            time_up = True
            root.destroy() 

    root = tk.Tk()
    root.overrideredirect(True) 
    root.attributes("-topmost", True)  
    root.geometry("70x30+1400+80")  

    label = tk.Label(root, font=("Arial", 15), fg="red")
    label.pack()
    update()
    root.mainloop()

def run_quiz():
    global time_up
    score = 0
    random.shuffle(questions)

    timer_thread = threading.Thread(target=countdown_window, args=(1200,))
    timer_thread.daemon = True
    timer_thread.start()

    for q in questions:
        if time_up:
            print("\nHết thời gian!")
            break

        print(f"\n{q['question']}")
        for key, value in q["options"].items():
            print(f"  {key}. {value}")
        print("→ Chọn đáp án: ", end="", flush=True, )
        answer = None
        while not answer:
            if time_up:
                print("\nHết thời gian!")
                break
            for key in ['a', 'b', 'c', 'd', 'e']:
                if keyboard.is_pressed(key):
                    answer = key.upper()
                    print(f"{answer}")
                    time.sleep(3) 
                    break
            time.sleep(0.1)
            
        if time_up:
            break

        if answer == q["answer"]:
            print(q['answer'], "Đúng\n")
            score += 1
        else:
            print(q['answer'], "Đúng\n")

    percent = (score / len(questions)) * 100
    result_text = (
        "\n Kết quả của bạn:\n" +
        f"- Số câu đúng: {score}/{len(questions)}\n" +
        f"- Tỷ lệ chính xác: {percent:.2f}%\n" 
    )
    with open("ketqua02.txt", "w", encoding="utf-8") as f:
        f.write(result_text)
    print(result_text)

