import os
import csv
import glob


def extract_events_and_messages(asc_path):
    base_name = os.path.splitext(os.path.basename(asc_path))[0]
    output_dir = os.path.dirname(asc_path)
    events_csv = os.path.join(output_dir, base_name + "_events.csv")
    messages_csv = os.path.join(output_dir, base_name + "_messages.csv")

    events = []
    messages = []

    print(f"🔎 מעבדת קובץ: {asc_path}")

    with open(asc_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split()

            # אם זו הודעת MSG
            if len(parts) > 2 and parts[0] == "MSG":
                time = parts[1]
                message_text = " ".join(parts[2:])
                messages.append([time, message_text])

            # אם זה סוג אירוע
            if parts and parts[0] in {"EFIX", "SFIX", "ESACC", "SSACC", "SBLINK", "EBLINK"}:
                events.append(parts)

    # שמירת הודעות ל־CSV
    if messages:
        with open(messages_csv, "w", newline="") as f_out:
            writer = csv.writer(f_out)
            writer.writerow(["TIME", "MESSAGE"])
            writer.writerows(messages)
        print(f"✅ נשמרו הודעות ל־: {messages_csv}")
    else:
        print("⚠️ לא נמצאו הודעות בקובץ: {base_name}")

    # שמירת אירועים ל־CSV
    if events:
        with open(events_csv, "w", newline="") as f_out:
            writer = csv.writer(f_out)
            num_cols = len(events[0])
            header = ["EVENT_TYPE"] + [f"col_{i}" for i in range(1, num_cols)]
            writer.writerow(header)
            writer.writerows(events)
        print(f"✅ נשמרו אירועים ל־: {events_csv}")
    else:
        print(f"⚠️ לא נמצאו אירועים בקובץ: {base_name}")


def process_all_asc_files(folder_path):
    asc_files = glob.glob(os.path.join(folder_path, "*.asc"))

    if not asc_files:
        print("❌ לא נמצאו קבצי ASC בתיקייה")
        return

    print(f"📂 נמצאו {len(asc_files)} קבצים בתיקייה: {folder_path}")

    for asc_file in asc_files:
        extract_events_and_messages(asc_file)


# 🧪 דוגמה לשימוש:
folder_path = "/Users/tahelhasson/Desktop/ascFiles"  # ❗ כאן תכתבי את הנתיב לתיקייה שלך
process_all_asc_files(folder_path)
