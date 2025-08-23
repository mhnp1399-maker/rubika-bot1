import requests
import time

# توکن ربات روبیکا
TOKEN = "CEDDI0KLKMIYAKROUHTSYXETTQJWBSCVXKCFWRFZIIUGIZVALEZFVQNEBWOMUFFS"

# لیست کلمات ممنوع
bad_words = ["کیر", "کص", "کس", "کسکش", "کصکش", "کثکش", "کسخل", "کصخل", "کثخل", "کیرم", "کیرت", "کیرش", "کون", "کونت", "کونم", "کونکش", "گاییدن", "گاییدم", "گایید", "جنده", "مادرسگ", "پدرسگ", "گوه", "رید", "ریدم", "ریدی", "ریدین"]
warning_data = {}

def get_updates():
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/getUpdates"
    return requests.post(url).json()

def send_message(chat_id, text):
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def delete_message(chat_id, message_id):
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/deleteMessage"
    requests.post(url, json={"chat_id": chat_id, "message_id": message_id})

def kick_user(chat_id, user_guid):
    url = f"https://botapi.rubika.ir/v3/{TOKEN}/kickGroupMember"
    requests.post(url, json={"chat_id": chat_id, "user_guid": user_guid})

def check_bad_words(text):
    return any(word in text.lower() for word in bad_words)

def check_link(text):
    return "http://" in text or "https://" in text or "rubika.ir/" in text

# حلقه بی‌پایان برای دریافت پیام‌ها
last_update_id = None

while True:
    try:
        updates = get_updates()
        for update in updates.get("updates", []):
            if last_update_id == update.get("update_id"):
                continue
            last_update_id = update.get("update_id")

            chat_id = update["chat"]["chat_id"]
            text = update.get("message", {}).get("text", "")
            message_id = update.get("message", {}).get("message_id", "")
            user_guid = update.get("message", {}).get("author_object_guid", "")
            user_id = update.get("message", {}).get("author_user_id", "")

            if update.get("type") == "GroupMemberAdded":
                send_message(chat_id, f"🎉 خوش آمدی {update['user']['first_name']}!")

            elif text == "/start" and update["chat"]["type"] == "Private":
                send_message(chat_id, "سلام! چه کاری می‌تونم برات انجام بدم؟\n1. دریافت آهنگ\n2. راهنما\n3. تماس با ادمین")

            elif check_bad_words(text):
                delete_message(chat_id, message_id)
                warning_data[user_guid] = warning_data.get(user_guid, 0) + 1
                count = warning_data[user_guid]
                send_message(chat_id, f"⚠️ کاربر @{user_id} اخطار {count}/5")
                if count >= 5:
                    kick_user(chat_id, user_guid)
                    send_message(chat_id, f"❌ کاربر @{user_id} به دلیل دریافت 5 اخطار از گروه حذف شد.")

            elif check_link(text):
                delete_message(chat_id, message_id)
                send_message(chat_id, f"⚠️ ارسال لینک ممنوعه! اخطار برای @{user_id}")

        time.sleep(1)

    except Exception as e:
        print(f"خطا: {e}")
        time.sleep(2)
