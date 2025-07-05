import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# الحالة 1: نحاول نقرأ JSON من Streamlit secrets
firebase_json = os.environ.get("SERVICE_ACCOUNT_KEY")

if firebase_json:
    # لو موجود (يعني شغال على Streamlit Cloud)، نحمّله من النص
    firebase_dict = json.loads(firebase_json)
    cred = credentials.Certificate(firebase_dict)
else:
    # لو مش موجود (يعني شغال محليًا)، نقرأ الملف مباشرة
    with open("serviceAccountKey.json") as f:
        cred = credentials.Certificate(json.load(f))

# تهيئة Firebase
firebase_admin.initialize_app(cred)

# قاعدة البيانات
db = firestore.client()
