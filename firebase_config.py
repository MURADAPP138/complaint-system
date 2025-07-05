import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage

# جلب بيانات مفتاح الخدمة من secrets كـ JSON
service_account_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])

# تهيئة التطبيق إذا لم يتم تهيئته بالفعل
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'online-db369.firebasestorage.app'  # عدل حسب bucket الخاص بك
    })

# الوصول إلى قاعدة البيانات و التخزين
db = firestore.client()
bucket = storage.bucket()
