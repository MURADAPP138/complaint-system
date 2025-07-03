import firebase_admin
from firebase_admin import credentials, firestore

# تحميل مفتاح الخدمة
cred = credentials.Certificate('serviceAccountKey.json')  # تأكد من المسار صحيح

# تهيئة تطبيق Firebase (يشتغل مرة وحدة فقط)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# إنشاء كائن Firestore client للتعامل مع قاعدة البيانات
db = firestore.client()
