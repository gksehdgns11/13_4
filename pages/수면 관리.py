
import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta

FILE_NAME = "sleepy_data.json"

BG = "#11162E"
CARD = "#202747"
PURPLE = "#B8B9FF"
WHITE = "#FFFFFF"
MUTED = "#C6CAE8"
GREEN = "#A8E6CF"

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"bedtime": "23:00", "wake": "07:00", "records": []}

data = load_data()

root = tk.Tk()
root.title("Sleepy - 수면 관리")
root.geometry("420x720")
root.configure(bg=BG)
root.resizable(False, False)

def save_data():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def label(parent, text, size=12, color=WHITE, bold=False):
    return tk.Label(
        parent, text=text, bg=parent["bg"], fg=color,
        font=("맑은 고딕", size, "bold" if bold else "normal")
    )

def button(parent, text, command):
    return tk.Button(
        parent, text=text, command=command,
        bg=PURPLE, fg=BG, activebackground="#D6D7FF",
        font=("맑은 고딕", 11, "bold"),
        relief="flat", cursor="hand2", pady=9
    )

def card(parent):
    frame = tk.Frame(parent, bg=CARD, padx=16, pady=14)
    frame.pack(fill="x", padx=18, pady=8)
    return frame

def calculate_minutes(start, end):
    a = datetime.strptime(start, "%H:%M")
    b = datetime.strptime(end, "%H:%M")
    minutes = int((b - a).total_seconds() // 60)
    if minutes < 0:
        minutes += 24 * 60
    return minutes

def duration_text(minutes):
    return f"{minutes // 60}시간 {minutes % 60}분"

def save_goal():
    bedtime = bedtime_var.get()
    wake = wake_var.get()

    try:
        datetime.strptime(bedtime, "%H:%M")
        datetime.strptime(wake, "%H:%M")
    except ValueError:
        messagebox.showerror("입력 오류", "시간을 HH:MM 형식으로 입력해 주세요.")
        return

    data["bedtime"] = bedtime
    data["wake"] = wake
    save_data()
    goal_status.config(text=f"목표 저장 완료! 🌙\n취침 {bedtime} · 기상 {wake}")

def save_record():
    bedtime = actual_bed_var.get().strip()
    wake = actual_wake_var.get().strip()

    try:
        datetime.strptime(bedtime, "%H:%M")
        datetime.strptime(wake, "%H:%M")
    except ValueError:
        messagebox.showerror(
            "입력 오류",
            "취침 시간과 기상 시간을 HH:MM 형식으로 입력해 주세요."
        )
        return

    minutes = calculate_minutes(bedtime, wake)
    today = datetime.now().strftime("%Y-%m-%d")

    data["records"] = [
        r for r in data["records"] if r["date"] != today
    ]
    data["records"].append({
        "date": today,
        "bedtime": bedtime,
        "wake": wake,
        "minutes": minutes
    })
    data["records"].sort(key=lambda r: r["date"])

    save_data()
    update_history()

    record_status.config(
        text=f"오늘 수면 시간: {duration_text(minutes)}",
        fg=GREEN
    )

def update_history():
    records = data["records"][-7:]
    history_text.config(state="normal")
    history_text.delete("1.0", tk.END)

    if not records:
        history_text.insert(tk.END, "아직 기록이 없어요.\n오늘 수면을 기록해 보세요!")
    else:
        for record in reversed(records):
            history_text.insert(
                tk.END,
                f"📅 {record['date']}\n"
                f"   {record['bedtime']} 취침 → {record['wake']} 기상\n"
                f"   수면 시간: {duration_text(record['minutes'])}\n\n"
            )

        average = sum(r["minutes"] for r in records) // len(records)
        history_text.insert(
            tk.END, f"최근 {len(records)}회 평균: {duration_text(average)}"
        )

    history_text.config(state="disabled")

def clear_history():
    if messagebox.askyesno("기록 삭제", "모든 수면 기록을 삭제할까요?"):
        data["records"] = []
        save_data()
        update_history()
        record_status.config(text="기록을 삭제했어요.", fg=MUTED)

# 상단 제목
label(root, "🌙", 32).pack(pady=(15, 0))
label(root, "Sleepy", 27, PURPLE, True).pack()
label(root, "규칙적인 수면 습관 만들기", 11, MUTED).pack(pady=(0, 8))

# 수면 목표
goal_card = card(root)
label(goal_card, "⏰  나의 수면 목표", 14, PURPLE, True).pack(anchor="w")

goal_row = tk.Frame(goal_card, bg=CARD)
goal_row.pack(fill="x", pady=8)

bedtime_var = tk.StringVar(value=data["bedtime"])
wake_var = tk.StringVar(value=data["wake"])

for col, title, variable in [
    (0, "취침 시간", bedtime_var),
    (1, "기상 시간", wake_var)
]:
    box = tk.Frame(goal_row, bg=CARD)
    box.grid(row=0, column=col, sticky="ew", padx=(0, 8))
    label(box, title, 10, MUTED).pack(anchor="w")
    tk.Entry(
        box, textvariable=variable, width=12,
        font=("맑은 고딕", 13), justify="center"
    ).pack(pady=5)

goal_row.columnconfigure(0, weight=1)
goal_row.columnconfigure(1, weight=1)

button(goal_card, "목표 저장하기", save_goal).pack(fill="x")
goal_status = label(goal_card, "", 10, GREEN)
goal_status.pack(pady=(7, 0))

# 오늘의 수면 기록
record_card = card(root)
label(record_card, "📝  오늘의 수면 기록", 14, PURPLE, True).pack(anchor="w")

actual_bed_var = tk.StringVar()
actual_wake_var = tk.StringVar()

for title, variable in [
    ("실제 잠든 시간 (예: 23:15)", actual_bed_var),
    ("실제 일어난 시간 (예: 07:10)", actual_wake_var)
]:
    label(record_card, title, 10, MUTED).pack(anchor="w", pady=(8, 3))
    tk.Entry(
        record_card, textvariable=variable,
        font=("맑은 고딕", 12)
    ).pack(fill="x")

button(record_card, "오늘 기록 저장하기", save_record).pack(fill="x")
record_status = label(record_card, "", 11, GREEN)
record_status.pack(pady=(7, 0))

# 기록 목록
history_card = card(root)
label(history_card, "📊  최근 수면 기록", 14, PURPLE, True).pack(anchor="w")

history_text = tk.Text(
    history_card, height=7, wrap="word",
    bg=CARD, fg=WHITE, font=("맑은 고딕", 10),
    relief="flat", state="disabled"
)
history_text.pack(fill="x", pady=8)

button(history_card, "기록 전체 삭제", clear_history).pack(fill="x")

label(root, "작은 습관부터, 더 편안한 하루까지 ✨", 10, MUTED).pack(pady=10)

goal_status.config(text=f"취침 {data['bedtime']} · 기상 {data['wake']}")
update_history()

root.mainloop()
