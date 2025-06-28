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
    },
    {
        "question": "31. What is the primary purpose of digital forensics?",
        "options": {
            "A": "To recover deleted files",
            "B": "To analyze digital information for legal evidence",
            "C": "To increase computer performance",
            "D": "To install software",
            "E": "To create backup copies"
        },
        "answer": "B"
    },
    {
        "question": "32. Which tool is commonly used for disk imaging in Windows forensic investigations?",
        "options": {
            "A": "WinRAR",
            "B": "FTK Imager",
            "C": "Microsoft Word",
            "D": "Adobe Reader",
            "E": "Notepad"
        },
        "answer": "B"
    },
    {
        "question": "33. In Linux, which command is used to create a bit-by-bit copy of a hard drive?",
        "options": {
            "A": "cp",
            "B": "dd",
            "C": "rsync",
            "D": "mv",
            "E": "tar"
        },
        "answer": "B"
    },
    {
        "question": "34. Which of the following is NOT a common file system used in forensics?",
        "options": {
            "A": "NTFS",
            "B": "FAT32",
            "C": "ext4",
            "D": "HFS+",
            "E": "JPEG"
        },
        "answer": "E"
    },
    {
        "question": "35. What is the significance of maintaining a chain of custody in digital forensics?",
        "options": {
            "A": "To ensure data recovery",
            "B": "To legally document the handling of evidence",
            "C": "To prevent computer viruses",
            "D": "To enhance system performance",
            "E": "To provide software updates"
        },
        "answer": "B"
    },
    {
        "question": "36. Which forensic tool is known for analyzing and recovering artifacts from mobile devices?",
        "options": {
            "A": "Autopsy",
            "B": "Cellebrite",
            "C": "Acronis",
            "D": "Paint.NET",
            "E": "GIMP"
        },
        "answer": "B"
    },
    {
        "question": "37. What file format is commonly used for storing forensic images?",
        "options": {
            "A": ".jpeg",
            "B": ".iso",
            "C": ".e01",
            "D": ".txt",
            "E": ".mp3"
        },
        "answer": "C"
    },
    {
        "question": "38. Which command in Windows can be used to verify the integrity of files?",
        "options": {
            "A": "ping",
            "B": "dir",
            "C": "certutil",
            "D": "format",
            "E": "ipconfig"
        },
        "answer": "C"
    },
    {
        "question": "39. In Linux forensics, which file contains information about user accounts and their hashes?",
        "options": {
            "A": "/etc/passwd",
            "B": "/etc/group",
            "C": "/var/log/syslog",
            "D": "/home/user",
            "E": "/root/root"
        },
        "answer": "A"
    },
    {
        "question": "40. What does the term 'forensic duplication' refer to in digital forensics?",
        "options": {
            "A": "Copying files to the cloud",
            "B": "Creating a legally admissible exact copy of data for analysis",
            "C": "Backing up important documents",
            "D": "Reducing file sizes for easier transfer",
            "E": "Updating software installations"
        },
        "answer": "B"
    },
    {
        "question": "41. What is the primary purpose of digital forensics in a Windows environment?",
        "options": {
            "A": "Data recovery",
            "B": "Malware analysis",
            "C": "Incident response",
            "D": "Network security",
            "E": "System optimization"
        },
        "answer": "C"
    },
    {
        "question": "42. Which tool is commonly used for forensic analysis on Windows systems?",
        "options": {
            "A": "Autopsy",
            "B": "FTK Imager",
            "C": "Wireshark",
            "D": "Nmap",
            "E": "Metasploit"
        },
        "answer": "B"
    },
    {
        "question": "43. In Linux forensics, what is the command to create a disk image using dd?",
        "options": {
            "A": "dd if=/dev/sda of=/path/to/image.img",
            "B": "dd /dev/sda > /path/to/image.img",
            "C": "dd image=/dev/sda of=/path/to/image.img",
            "D": "dd path=/dev/sda to=/path/to/image.img",
            "E": "dd create /dev/sda > /path/to/image.img"
        },
        "answer": "A"
    },
    {
        "question": "44. What file system is commonly analyzed in Windows forensics?",
        "options": {
            "A": "ext4",
            "B": "NTFS",
            "C": "HFS+",
            "D": "Btrfs",
            "E": "FAT32"
        },
        "answer": "B"
    },
    {
        "question": "45. Which command is used to analyze running processes in a Linux forensic investigation?",
        "options": {
            "A": "vmstat",
            "B": "ps aux",
            "C": "netstat -a",
            "D": "top -u",
            "E": "lsof"
        },
        "answer": "B"
    },
    {
        "question": "46. What is a notable feature of the Registry in Windows forensics?",
        "options": {
            "A": "It shows real-time CPU usage",
            "B": "It contains user and system configuration settings",
            "C": "It is a form of file encryption",
            "D": "It stores network traffic logs",
            "E": "It doesn't store application data"
        },
        "answer": "B"
    },
    {
        "question": "47. Which of the following is a popular open-source forensic tool for Linux?",
        "options": {
            "A": "Encase",
            "B": "X1 Social Discovery",
            "C": "Sleuth Kit",
            "D": "Helix",
            "E": "FTK Imager"
        },
        "answer": "C"
    },
    {
        "question": "48. What is the significance of a hash value in digital forensics?",
        "options": {
            "A": "It encrypts the data",
            "B": "It verifies the integrity of the data",
            "C": "It compresses the data",
            "D": "It stores the location of the data",
            "E": "It helps in data recovery"
        },
        "answer": "B"
    },
    {
        "question": "49. Which type of evidence can be found in volatile memory during a forensic examination?",
        "options": {
            "A": "Installed applications",
            "B": "Previous user logins",
            "C": "Running processes and network connections",
            "D": "Disk partition information",
            "E": "Archived emails"
        },
        "answer": "C"
    },
    {
        "question": "50. What is the primary file system for Linux?",
        "options": {
            "A": "NTFS",
            "B": "FAT32",
            "C": "ext4",
            "D": "HFS+",
            "E": "exFAT"
        },
        "answer": "C"
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

