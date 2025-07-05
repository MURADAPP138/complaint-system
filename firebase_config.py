import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# احصل على نص JSON من secrets.toml ثم حوله لقاموس dict
firebase_config_str = st.secrets["FIREBASE"]["FIREBASE_SERVICE_ACCOUNT"]
firebase_config = json.loads(firebase_config_str)

# تأكد من تهيئة firebase مرة واحدة فقط
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

# تهيئة قاعدة البيانات
db = firestore.client()
