import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta, date, time

# --- Import db from firebase_config.py ---
# This assumes you have a firebase_config.py file in the same directory
# that initializes Firebase Admin SDK and exports 'db'.
#
# Example firebase_config.py content:
#
# import firebase_admin
# from firebase_admin import credentials, firestore
# import os
#
# SERVICE_ACCOUNT_KEY_FILENAME = "serviceAccountKey.json"
# SERVICE_ACCOUNT_KEY_PATH = os.path.join(os.path.dirname(__file__), SERVICE_ACCOUNT_KEY_FILENAME)
#
# db = None # Initialize db as None
# try:
#     cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
#     if not firebase_admin._apps:
#         firebase_admin.initialize_app(cred)
#     db = firestore.client()
#     # You can add a Streamlit message here if you want to confirm initialization
#     # st.success("Firebase Admin SDK initialized successfully!")
# except Exception as e:
#     # Log the error, but don't stop the app from running if db is None
#     print(f"Failed to initialize Firebase Admin SDK. Check service account key path or permissions: {e}")
#     # st.error(f"Failed to initialize Firebase Admin SDK. Please check the service account key file.")
#
from firebase_config import db # Assuming db is initialized and exported from here

import os
import io

# --- Page settings and translations ---
st.set_page_config(
    page_title="لوحة تحكم أقسام الأونلاين",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Simple dictionary for translations
translations = {
    "ar": {
        "welcome_message": "قسم الأونلاين يرحب بك",
        "customer_service": "خدمة العملاء",
        "shipping_team": "الشحن",
        "manager": "المدير",
        "enter_password": "الرجاء إدخال كلمة المرور لـ",
        "login_button": "تسجيل الدخول",
        "incorrect_password": "كلمة المرور خاطئة. الرجاء المحاولة مرة أخرى.",
        "back_to_selection": "العودة لاختيار القسم",
        "logout": "تسجيل الخروج",
        "customer_service_dashboard_welcome": "أهلاً بك في لوحة تحكم خدمة العملاء!",
        "shipping_dashboard_welcome": "أهلاً بك في لوحة تحكم الشحن!",
        "manager_dashboard_welcome": "أهلاً بك في لوحة تحكم المدير!",
        "password_placeholder": "أدخل كلمة المرور هنا",
        "add_complaint": "إضافة شكوى جديدة",
        "complaint_number": "رقم الشكوى",
        "complaint_date": "تاريخ الشكوى",
        "complaint_time": "وقت الشكوى",
        "employee_name": "اسم موظف خدمة العملاء", # Customer Service employee name
        "customer_name": "اسم العميل",
        "customer_phone": "هاتف العميل", # New translation
        "issue_description": "تفاصيل الشكوى",
        "add_media_upload": "رفع صورة/فيديو (للمعاينة فقط)", # Text changed
        "add_media_link": "إضافة رابط صورة/فيديو (للحفظ الدائم)", # New text
        "submit_complaint": "إرسال الشكوى",
        "current_complaints": "الشكاوى الحالية",
        "no_complaints": "لا توجد شكاوى حالياً.",
        "status_options": ["جديد", "قيد المعالجة", "تم الحل", "مغلق"],
        "update_complaint": "تحديث حالة شكوى",
        "select_complaint": "اختر الشكوى",
        "new_status": "الحالة الجديدة",
        "update_button": "تحديث",
        "add_shipment": "إضافة شحنة جديدة",
        "shipment_id": "معرف الشحنة",
        "destination": "الوجهة",
        "current_shipments": "الشحنات الحالية",
        "no_shipments": "لا توجد شحنات حالياً.",
        "shipment_status_options": ["قيد الانتظار", "تم الشحن", "خارج للتوصيل", "تم التوصيل"],
        "update_shipment": "تحديث حالة شحنة",
        "select_shipment": "اختر الشحنة",
        "dashboard_overview": "نظرة عامة على لوحة التحكم",
        "total_complaints": "إجمالي الشكاوى",
        "open_complaints": "الشكاوى المفتوحة",
        "resolved_complaints": "الشكاوى التي تم حلها",
        "total_shipments": "إجمالي الشحنات",
        "delivered_shipments": "الشحنات التي تم توصيلها",
        "pending_shipments": "الشحنات المعلقة",
        "reports_and_analytics": "التقارير والتحليلات",
        "complaint_status_distribution": "توزيع حالات الشكاوى",
        "shipment_status_distribution": "توزيع حالات الشحنات",
        "total_users": "إجمالي المستخدمين",
        "active_users": "المستخدمون النشطون",
        "user_management": "إدارة المستخدمين (قريباً)",
        "admin_settings": "إعدادات المسؤول (قريباً)",
        "search_by_complaint_id": "بحث برقم الشكوى",
        "search_button": "بحث",
        "complaint_found": "تم العثور على الشكوى:",
        "shipping_response": "رد قسم الشحن:",
        "no_shipping_response": "لم يتم الرد من قسم الشحن بعد.",
        "complaint_not_found": "لم يتم العثور على شكوى بهذا الرقم.",
        "add_shipping_response": "إضافة/تعديل رد الشحن",
        "response_text": "نص الرد",
        "save_response": "حفظ الرد",
        "response_saved": "تم حفظ رد الشحن بنجاح!",
        "status": "الحالة",
        "complaint_type": "نوع الشكوى",
        "complaint_type_options": ["ارجاع لقيمة الطلب", "الغاء الطلب", "تاخير & استعجال", "منتجات تالفه & ناقصه","تحديث معلومات الطلب", "تذكير","طلب توصيل سريع"],
        "old_complaints": "الشكاوى القديمة",
        "delete_complaint": "حذف الشكوى",
        "confirm_delete": "هل أنت متأكد من حذف هذه الشكوى؟ هذا الإجراء لا يمكن التراجع عنه.",
        "complaint_deleted": "تم حذف الشكوى بنجاح!",
        "no_old_complaints": "لا توجد شكاوى قديمة حالياً.",
        "in_progress_complaints": "الشكاوى قيد المعالجة",
        "closed_complaints": "الشكاوى المغلقة",
        "avg_response_time": "متوسط وقت الرد",
        "days": "أيام",
        "hours": "ساعات",
        "minutes": "دقائق",
        "seconds": "ثواني",
        "filter_by_date": "اختر الفترة",
        "filter_by_type": "نوع الشكوى",
        "all": "الكل",
        "complaint_table_title": "الشكاوى التفصيلية",
        "media_attachments": "مرفقات الشحن (روابط)", # Text changed
        "shipping_status_options": ["جاري المتابعة", "تم الحل"],
        "search_old_complaints": "بحث في الشكاوى القديمة",
        "filter_by_complaint_type": "تصفية حسب نوع الشكوى",
        "download_excel": "تحميل كملف Excel",
        "shipping_employee_name": "اسم موظف الشحن",
        "cs_media_links": "روابط مرفقات خدمة العملاء", # New translation
        "shipping_media_links": "روابط مرفقات الشحن", # New translation
        "search_specific_complaint": "بحث عن شكوى محددة",
        "complaint_recorded_date": "تاريخ تسجيل الشكوى", # New translation
        "complaint_recorded_time": "وقت تسجيل الشكوى", # New translation
        "shipping_response_date_kpi": "تاريخ رد الشحن", # New translation
        "shipping_response_time_kpi": "وقت رد الشحن", # New translation
        "not_responded_yet": "لم يتم الرد بعد",
        "no_complaint_selected": "الرجاء إدخال رقم شكوى للبحث",
        "shipping_response_date_input": "تاريخ الرد من الشحن", # New translation for input field
        "shipping_response_time_input": "وقت الرد من الشحن", # New translation for input field
        "add_cs_comment": "إضافة تعليق إضافي", # NEW
        "cs_comment_text": "التعليق الإضافي", # NEW
        "submit_comment": "إرسال التعليق", # NEW
        "comment_added_successfully": "تم إضافة التعليق بنجاح!", # NEW
        "cs_comments_section": "سجل تعليقات خدمة العملاء", # NEW
        "complaints_with_new_cs_comments": "شكاوى عليها تعليقات جديدة من خدمة العملاء", # NEW
        "no_new_cs_comments": "لا توجد شكاوى عليها تعليقات جديدة من خدمة العملاء حالياً.", # NEW
        "view_cs_comments": "عرض التعليقات", # NEW
        "cs_comment_employee": "موظف خدمة العملاء", # NEW
        "cs_comment_timestamp": "التاريخ والوقت", # NEW
        "comment_content": "التعليق", # NEW
        "new_comment_from_cs": "تعليق جديد من خدمة العملاء", # NEW
        "shipping_comments_section": "سجل ردود الشحن", # NEW
        "shipping_comment_text": "الرد من الشحن", # NEW
        "submit_shipping_comment": "إرسال رد الشحن", # NEW
        "shipping_comment_added_successfully": "تم إرسال رد الشحن بنجاح!", # NEW
        "shipping_comment_employee": "موظف الشحن", # NEW
        "shipping_comment_timestamp": "التاريخ والوقت", # NEW
        "latest_comment_label": "آخر تعليق جديد", # NEW Translation for label
        "admin_action_request": "اعتماد إجراء إداري", # NEW
        "request_date": "تاريخ الطلب", # NEW
        "customer_receipt_date": "تاريخ استلام العميل للطلب", # NEW
        "shipping_company": "شركة الشحن", # NEW
        "order_status": "حالة الطلب", # NEW
        "request_details": "تفاصيل الطلب/الإجراء المطلوب", # NEW
        "request_media_link": "رابط صورة/فيديو (للطلب)", # NEW
        "request_employee_name": "اسم موظف الشحن مقدم الطلب", # NEW
        "submit_request": "إرسال طلب الإجراء الإداري", # NEW
        "request_submitted_successfully": "تم إرسال طلب الإجراء الإداري بنجاح!", # NEW
        "new_admin_actions_needed": "شكاوى جديدة تحتاج اعتماد إجراء إداري", # NEW
        "admin_action_approved": "الإجراء الإداري المعتمد", # NEW - used for form label
        "approved_by": "معتمد الإجراء", # NEW
        "submit_approval": "إرسال الاعتماد", # NEW
        "approval_saved_successfully": "تم حفظ الاعتماد بنجاح!", # NEW
        "approval_status": "حالة الاعتماد الإداري", # NEW
        "approval_date": "تاريخ الاعتماد", # NEW
        "approval_time": "وقت الاعتماد", # NEW
        "pending_approval": "بانتظار الاعتماد", # NEW
        "approved": "تم الاعتماد", # NEW
        "rejected": "تم الرفض", # NEW
        "no_admin_actions_needed": "لا توجد طلبات اعتماد إجراء إداري جديدة حالياً.", # NEW
        "no_admin_action_selected": "الرجاء اختيار طلب إجراء إداري للمراجعة.", # NEW
        "action_details": "تفاصيل الإجراء الإداري", # NEW
        "action_employee": "اسم موظف الشحن", # NEW
        "action_status": "حالة طلب الإجراء", # NEW
        "view_request_details": "عرض تفاصيل الطلب", # NEW
        "admin_request_id": "معرف طلب الإجراء", # NEW - this will be hidden in display
        "approved_rejected_requests": "طلبات الإجراء الإداري التي تم التعامل معها", # NEW
        "request_status_summary": "شكوى تم الرد عليها رقم", # NEW
        "approved_request_details": "تفاصيل طلب الإجراء المعتمد", # NEW
        "rejected_request_details": "تفاصيل الرفض", # NEW - Added this translation
        "approved_by_label": "معتمد الإجراء", # NEW
        "approval_date_label": "تاريخ الاعتماد", # NEW
        "approval_time_label": "وقت الاعتماد", # NEW
        "admin_requests_table_title": "جميع طلبات الإجراء الإداري", # NEW
        "download_admin_requests_excel": "تحميل طلبات الإجراء الإداري (Excel)", # NEW
        "delete_selected_requests": "حذف الطلبات المحددة", # NEW
        "confirm_delete_requests": "هل أنت متأكد من حذف هذه الطلبات؟ هذا الإجراء لا يمكن التراجع عنه.", # NEW
        "requests_deleted_successfully": "تم حذف الطلبات بنجاح!", # NEW
        "select_requests_to_delete": "اختر طلبات من الجدول أعلاه لحذفها.", # NEW
    }
}

# Use Arabic by default
t = translations["ar"]

# --- Passwords (for testing only - do not use in production) ---
PASSWORDS = {
    t['customer_service']: "123456",
    t['shipping_team']: "987456",
    t['manager']: "5723"
}

# --- Session State Management ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "role_selection"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_role" not in st.session_state:
    st.session_state.selected_role = None
if "complaints" not in st.session_state:
    st.session_state.complaints = []
if "admin_requests" not in st.session_state: # NEW: To store admin requests
    st.session_state.admin_requests = []

# --- Firebase functions for data handling ---

def load_complaints_from_firestore():
    """
    Loads complaints from Firestore.
    Ensures all loaded complaints have necessary fields with default values if missing.
    """
    if db: # Check if db is initialized from firebase_config
        try:
            with st.spinner("جاري تحميل الشكاوى..."): # Added spinner
                complaints_ref = db.collection('complaints')
                docs = complaints_ref.stream()
                complaints_list = []
                for doc in docs:
                    data = doc.to_dict()
                    data['doc_id'] = doc.id # Store document ID for updates/deletes
                    
                    # Ensure all new fields exist, even if missing in old documents
                    data.setdefault('cs_comments', [])
                    data.setdefault('has_new_cs_comment', False)
                    data.setdefault('customer_phone', 'N/A') # Ensure customer_phone exists
                    data.setdefault('shipping_response_date', None)
                    data.setdefault('shipping_response_time', None)
                    data.setdefault('shipping_media_links', [])
                    data.setdefault('shipping_response_employee_name', '')
                    data.setdefault('shipping_comments', []) 

                    complaints_list.append(data)
                return complaints_list
        except Exception as e:
            st.error(f"فشل تحميل الشكاوى من Firestore: {e}")
            return []
    st.warning("قاعدة البيانات غير جاهزة. لن يتم تحميل الشكاوى.")
    return []

def add_complaint_to_firestore(complaint_data):
    """
    Adds a new complaint to Firestore.
    """
    if db:
        try:
            with st.spinner("جاري إرسال الشكوى..."): # Added spinner
                # Use complaint_number as document ID for easy lookup and uniqueness
                doc_ref = db.collection('complaints').document(complaint_data['complaint_number'])
                doc_ref.set(complaint_data)
                st.success("تم إرسال الشكوى بنجاح وحفظها في قاعدة البيانات!")
        except Exception as e:
            st.error(f"حدث خطأ أثناء حفظ الشكوى: {e}")
    else:
        st.warning("قاعدة البيانات غير جاهزة. لن يتم حفظ الشكوى بشكل دائم.")

def update_complaint_in_firestore(doc_id, update_data):
    """
    Updates an existing complaint in Firestore.
    """
    if db:
        try:
            with st.spinner("جاري تحديث الشكوى..."): # Added spinner
                complaint_doc_ref = db.collection('complaints').document(doc_id)
                complaint_doc_ref.update(update_data)
                st.success(t['response_saved']) # This message is generic for updates now
        except Exception as e:
            st.error(f"حدث خطأ أثناء تحديث الشكوى: {e}")
    else:
        st.warning("قاعدة البيانات غير جاهزة. لن يتم تحديث الرد بشكل دائم.")

def delete_complaint_from_firestore(doc_id):
    """
    Deletes a complaint from Firestore.
    """
    if db:
        try:
            with st.spinner("جاري حذف الشكوى..."): # Added spinner
                complaint_doc_ref = db.collection('complaints').document(doc_id)
                complaint_doc_ref.delete()
                st.success(t['complaint_deleted'])
        except Exception as e:
            st.error(f"حدث خطأ أثناء حذف الشكوى: {e}")
    else:
        st.warning("قاعدة البيانات غير جاهزة. لن يتم حذف الشكوى.")

# NEW: Firebase functions for admin requests
def load_admin_requests_from_firestore():
    """
    Loads admin action requests from Firestore.
    """
    if db:
        try:
            requests_ref = db.collection('admin_requests')
            docs = requests_ref.stream()
            requests_list = []
            for doc in docs:
                data = doc.to_dict()
                data['request_id'] = doc.id # Store document ID for updates
                
                # Ensure all necessary fields exist for old requests
                data.setdefault('status', t['pending_approval'])
                data.setdefault('approval_action', '')
                data.setdefault('approved_by_employee', '')
                data.setdefault('approval_date', None)
                data.setdefault('approval_time', None)
                
                requests_list.append(data)
            return requests_list
        except Exception as e:
            st.error(f"فشل تحميل طلبات الإجراء الإداري من Firestore: {e}")
            return []
    return []

def add_admin_request_to_firestore(request_data):
    """
    Adds a new admin action request to Firestore.
    """
    if db:
        try:
            doc_id = str(uuid.uuid4()) # Generate unique ID for the request
            db.collection('admin_requests').document(doc_id).set(request_data)
            st.success(t['request_submitted_successfully'])
        except Exception as e:
            st.error(f"حدث خطأ أثناء حفظ طلب الإجراء الإداري: {e}")

def update_admin_request_in_firestore(request_id, update_data):
    """
    Updates an existing admin action request in Firestore.
    """
    if db:
        try:
            request_doc_ref = db.collection('admin_requests').document(request_id)
            request_doc_ref.update(update_data)
            st.success(t['approval_saved_successfully'])
        except Exception as e:
            st.error(f"حدث خطأ أثناء تحديث طلب الإجراء الإداري: {e}")

def delete_admin_request_from_firestore(request_id): # NEW: Function to delete admin requests
    """
    Deletes an admin action request from Firestore.
    """
    if db:
        try:
            request_doc_ref = db.collection('admin_requests').document(request_id)
            request_doc_ref.delete()
            st.success(t['requests_deleted_successfully'])
        except Exception as e:
            st.error(f"حدث خطأ أثناء حذف طلب الإجراء الإداري: {e}")
    else:
        st.warning("قاعدة البيانات غير جاهزة. لن يتم حذف الطلب.")


# Load data when the app starts
# This will be called once per session or when the script reruns
st.session_state.complaints = load_complaints_from_firestore()
st.session_state.admin_requests = load_admin_requests_from_firestore() # NEW: Load admin requests


# --- Custom CSS for overall appearance ---
custom_css = """
<style>
    /* Basic fonts */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f0f2f6; /* Light background */
        color: #333;
    }

    /* Page titles */
    h1, h2, h3, h4, h5, h6 {
        color: #1a202c;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Streamlit buttons */
    .stButton>button {
        background-color: #4CAF50; /* Primary green */
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #45a049; /* Darker green on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Login and role selection buttons */
    .stButton[key*="btn_"] > button {
        background-color: #3B82F6; /* Blue */
        color: white;
        font-size: 1.2em;
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
    }
    .stButton[key*="btn_"] > button:hover {
        background-color: #2563EB;
        transform: translateY(-3px);
    }

    /* Colored input containers */
    .stTextInput>div>div>input, .stDateInput>div>div>input, .stTimeInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 8px 12px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        transition: border-color 0.2s;
    }
    .stTextInput>div>div>input:focus, .stDateInput>div>div>input:focus, .stTimeInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 0.2rem rgba(59, 130, 246, 0.25);
    }

    /* st.expander containers */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        transition: background-color 0.2s ease;
    }
    .streamlit-expanderHeader:hover {
        background-color: #e9ecef;
    }
    .streamlit-expanderContent {
        background-color: #ffffff;
        border-radius: 0 0 8px 8px;
        border-top: 1px solid #eee;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* KPI cards in Manager dashboard */
    .kpi-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    .kpi-card .icon {
        font-size: 3.5em;
        margin-bottom: 10px;
    }
    .kpi-card .title {
        font-weight: bold;
        font-size: 1.1em;
        color: #555;
        margin-bottom: 5px;
    }
    .kpi-card .value {
        font-size: 2.5em;
        font-weight: bolder;
        color: #1a202c;
    }
    .kpi-card.small-value .value { /* For smaller KPI values like time strings */
        font-size: 1.8em;
    }
    /* Admin Request Status Badges */
    .badge {
        display: inline-block;
        padding: 0.3em 0.7em;
        border-radius: 0.8em;
        font-size: 0.9em;
        font-weight: bold;
        text-align: center;
        vertical-align: middle;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .badge.pending { background-color: #ffeb3b; color: #795548; } /* Amber */
    .badge.approved { background-color: #c8e6c9; color: #2E7D32; } /* Light Green */
    .badge.rejected { background-color: #ffcdd2; color: #D32F2F; } /* Light Red */


    /* Specific colors for KPI cards */
    .kpi-card.total .icon { color: #3B82F6; } /* Blue */
    .kpi-card.total .value { color: #1D4ED8; }

    .kpi-card.closed .icon { color: #10B981; } /* Green */
    .kpi-card.closed .value { color: #047857; }

    .kpi-card.in-progress .icon { color: #F59E0B; } /* Orange */
    .kpi-card.in-progress .value { color: #B45309; }

    .kpi-card.avg-time .icon { color: #8B5CF6; } /* Purple */
    .kpi-card.avg-time .value { color: #6D28D9; }
    
    /* Highlighted complaints for new CS comments */
    .cs-comment-highlight {
        background-color: #FFFDE7; /* Light yellow */
        border-left: 5px solid #FFC107; /* Amber border */
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .cs-comment-highlight h4 {
        color: #FF8F00; /* Darker amber */
    }

    /* Custom headers for complaint types */
    .complaint-type-header {
        background-color: #e0f7fa; /* Default light blue */
        padding: 10px 15px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 15px;
        font-size: 1.3em;
        font-weight: bold;
        color: #00796B;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: right;
    }
    /* Specific colors for headers based on type */
    .complaint-type-header.ارجاع-لقيمة-الطلب { background-color: #FFECB3; color: #E65100; } /* Light Orange */
    .complaint-type-header.الغاء-الطلب { background-color: #FFCDD2; color: #B71C1C; } /* Light Red */
    .complaint-type-header.تاخير-استعجال { background-color: #DCEDC8; color: #33691E; } /* Light Green */
    .complaint-type-header.منتجات-تالفه-ناقصه { background-color: #BBDEFB; color: #1565C0; } /* Light Blue */
    .complaint-type-header.تحديث-معلومات-الطلب { background-color: #E1BEE7; color: #4A148C; } /* Light Purple */
    .complaint-type-header.تذكير { background-color: #FFE0B2; color: #BF360C; } /* Light Brown */
    .complaint-type-header.طلب-توصيل-سريع { background-color: #C8E6C9; color: #2E7D32; } /* A bit darker green */

    /* Style for the latest comment in CS comments section */
    .latest-cs-comment-container {
        background-color: #E8F5E9; /* Very light green, or another subtle highlight color */
        border-left: 4px solid #4CAF50; /* Green border */
        padding: 8px;
        border-radius: 5px;
        margin-top: 5px;
        margin-bottom: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .latest-cs-comment-label {
        font-weight: bold;
        color: #2E7D32; /* Darker green */
        margin-bottom: 5px;
        display: block;
        text-align: right; /* Align label to the right */
        font-size: 0.9em; /* Smaller font for label */
    }


    /* Data table improvements */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stDataFrame table {
        width: 100%;
        border-collapse: collapse;
    }
    .stDataFrame th {
        background-color: #f0f2f6;
        color: #333;
        font-weight: bold;
        padding: 12px 15px;
        text-align: right; /* Right alignment for Arabic */
        border-bottom: 2px solid #ddd;
    }
    .stDataFrame td {
        padding: 10px 15px;
        border-bottom: 1px solid #eee;
        text-align: right; /* Right alignment for Arabic */
    }
    .stDataFrame tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .stDataFrame tr:hover {
        background-color: #f2f2f2;
    }

    /* Chart improvements */
    .stPlotlyChart {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 15px;
        background-color: #ffffff;
    }

    /* Section spacing */
    .section-separator {
        margin-top: 30px;
        margin-bottom: 30px;
        border-top: 1px solid #eee;
    }

    /* Success, error, info messages */
    .stAlert {
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        font-weight: 500;
    }
    .stAlert.success { background-color: #e6ffe6; border-left: 5px solid #4CAF50; color: #2E7D32; }
    .stAlert.error { background-color: #ffe6e6; border-left: 5px solid #f44336; color: #D32F2F; }
    .stAlert.warning { background-color: #fff3e0; border-left: 5px solid #ff9800; color: #EF6C00; }
    .stAlert.info { background-color: #e0f7fa; border-left: 5px solid #00BCD4; color: #00796B; }

    /* General spacing */
    .stBlock {
        padding: 10px 0;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Helper function for colored input containers ---
def colored_input_container(label, color_hex, key_suffix, input_type="text", options=None, default_value=None, placeholder=""):
    st.markdown(
        f"""
        <div style="
            background-color: {color_hex};
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <label style="font-weight: bold; color: #333; margin-bottom: 5px; display: block;">{label}</label>
        """,
        unsafe_allow_html=True
    )
    value = None
    if input_type == "text":
        value = st.text_input("", key=f"{key_suffix}_text", label_visibility="collapsed", value=default_value if default_value is not None else "", placeholder=placeholder)
    elif input_type == "date":
        value = st.date_input("", key=f"{key_suffix}_date", label_visibility="collapsed", value=default_value if default_value is not None else datetime.now().date())
    elif input_type == "time":
        value = st.time_input("", key=f"{key_suffix}_time", label_visibility="collapsed", value=default_value if default_value is not None else datetime.now().time())
    elif input_type == "selectbox":
        value = st.selectbox("", options, key=f"{key_suffix}_select", label_visibility="collapsed", index=options.index(default_value) if default_value in options else 0)
    
    st.markdown("</div>", unsafe_allow_html=True)
    return value

def display_media_from_links(media_links):
    """
    Displays images or videos from a list of URLs.
    """
    if media_links:
        for i, link in enumerate(media_links):
            if not link: # Skip empty links
                continue
            # Basic check for image/video extension
            lower_link = link.lower()
            if lower_link.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                st.image(link, caption=f"صورة {i+1}", use_container_width=False)
            elif lower_link.endswith(('.mp4', '.mov', '.avi', '.webm')):
                st.video(link, caption=f"فيديو {i+1}", format="video/mp4", start_time=0)
            else:
                st.warning(f"نوع ملف غير مدعوم أو رابط غير صالح: {link}")
                st.markdown(f"**الرابط:** [{link}]({link})")

def format_timedelta_to_string(td: timedelta, lang_dict: dict) -> str:
    """Formats a timedelta object into a human-readable string."""
    if td is None:
        return lang_dict['not_responded_yet']

    total_seconds = int(td.total_seconds())
    if total_seconds < 0: # Handle cases where response is before complaint (shouldn't happen with correct data)
        return "N/A"

    days = total_seconds // (24 * 3600)
    total_seconds %= (24 * 3600)
    hours = total_seconds // 3600
    total_seconds %= 3600
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    parts = []
    if days > 0:
        parts.append(f"{days} {lang_dict['days']}")
    if hours > 0:
        parts.append(f"{hours} {lang_dict['hours']}")
    if minutes > 0:
        parts.append(f"{minutes} {lang_dict['minutes']}")
    if seconds > 0 or not parts: # If no other parts, show seconds
        parts.append(f"{seconds} {lang_dict['seconds']}")
    
    return " ".join(parts)

# Helper function to format comments/replies for DataFrame display
def format_comments_for_dataframe_display(comments_list):
    if not comments_list:
        return "لا توجد تعليقات/ردود"
    formatted_entries = []
    # Display up to 3 comments in the table, for brevity
    # You can adjust this number or show only the latest
    for i, entry in enumerate(comments_list):
        timestamp = entry.get('timestamp', 'N/A')
        employee = entry.get('employee_name', 'N/A')
        comment_text = entry.get('comment', '')
        formatted_entries.append(f"[{timestamp}] {employee}: {comment_text}")
    return "\n---\n".join(formatted_entries)


# --- Different page functions ---

def role_selection_page():
    """
    Main page for role selection.
    """
    st.markdown(f"<h2 style='text-align: center; color: #1f2937; margin-bottom: 30px;'>{t['welcome_message']}</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card" style="background-color: #E0F7FA;">
                <p class="icon">📞</p>
                <p class="title">{t['customer_service']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(t['customer_service'], key="btn_cs", use_container_width=True):
            st.session_state.selected_role = t['customer_service']
            st.session_state.current_page = "login"
            st.rerun()

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card" style="background-color: #E8F5E9;">
                <p class="icon">📦</p>
                <p class="title">{t['shipping_team']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(t['shipping_team'], key="btn_shipping", use_container_width=True):
            st.session_state.selected_role = t['shipping_team']
            st.session_state.current_page = "login"
            st.rerun()

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card" style="background-color: #F3E5F5;">
                <p class="icon">👑</p>
                <p class="title">{t['manager']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button(t['manager'], key="btn_manager", use_container_width=True):
            st.session_state.selected_role = t['manager']
            st.session_state.current_page = "login"
            st.rerun()

def login_page():
    """
    Password input page for each role.
    """
    role = st.session_state.selected_role
    expected_password = PASSWORDS.get(role)

    st.markdown(f"<h3 style='text-align: center; color: #1f2937; margin-bottom: 20px;'>{t['enter_password']} {role}</h3>", unsafe_allow_html=True)

    password = st.text_input(t['password_placeholder'], type="password", key="password_input")

    if st.button(t['login_button'], use_container_width=True):
        if password == expected_password:
            st.session_state.logged_in = True
            if role == t['customer_service']:
                st.session_state.current_page = "customer_service_dashboard"
            elif role == t['shipping_team']:
                st.session_state.current_page = "shipping_dashboard"
            elif role == t['manager']:
                st.session_state.current_page = "manager_dashboard"
            st.rerun()
        else:
            st.error(t['incorrect_password'])

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
    if st.button(t['back_to_selection'], key="back_to_role_selection"):
        st.session_state.current_page = "role_selection"
        st.session_state.selected_role = None
        st.session_state.logged_in = False
        st.rerun()

# --- Actual dashboard pages ---

def customer_service_dashboard():
    """
    Customer Service dashboard.
    Allows adding, viewing, and updating complaints.
    """
    st.markdown(f"<h2 style='text-align: center; color: #1f2937;'>{t['customer_service_dashboard_welcome']}</h2>", unsafe_allow_html=True)
    
    # --- Search by complaint ID ---
    st.markdown(f"<h3 style='text-align: right; color: #1f2937;'>{t['search_by_complaint_id']}</h3>", unsafe_allow_html=True)
    search_col, _ = st.columns([0.7, 0.3])
    with search_col:
        search_complaint_number = st.text_input("", placeholder=t['complaint_number'], key="cs_search_number")
    
    if st.button(t['search_button'], key="cs_search_btn"):
        found_complaint = next((c for c in st.session_state.complaints if c['complaint_number'] == search_complaint_number), None)
        if found_complaint:
            st.success(f"**{t['complaint_found']}**")
            st.write(f"**{t['complaint_number']}:** {found_complaint['complaint_number']}")
            st.write(f"**{t['complaint_date']}:** {found_complaint['date']}")
            st.write(f"**{t['complaint_time']}:** {found_complaint['time']}")
            st.write(f"**{t['employee_name']}:** {found_complaint['employee_name']}")
            st.write(f"**{t['customer_name']}:** {found_complaint['customer_name']}")
            st.write(f"**📞 {t['customer_phone']}:** {found_complaint.get('customer_phone', 'N/A')}") # Display customer phone
            st.write(f"**{t['complaint_type']}:** {found_complaint['complaint_type']}")
            st.write(f"**{t['issue_description']}:** {found_complaint['issue_description']}")
            st.write(f"**{t['status']}:** {found_complaint['status']}")
            
            # Display CS media links
            if found_complaint.get('cs_media_links'):
                st.markdown(f"**{t['cs_media_links']}:**")
                display_media_from_links(found_complaint['cs_media_links'])
            
            st.markdown(f"**{t['shipping_response']}**")
            if found_complaint['shipping_response']:
                st.info(found_complaint['shipping_response'])
                if found_complaint.get('shipping_response_employee_name'):
                    st.write(f"**{t['shipping_employee_name']}:** {found_complaint['shipping_response_employee_name']}")
                # Display shipping response date and time
                if found_complaint.get('shipping_response_date'):
                    st.write(f"**{t['shipping_response_date_kpi']}:** {found_complaint['shipping_response_date']}")
                if found_complaint.get('shipping_response_time'):
                    st.write(f"**{t['shipping_response_time_kpi']}:** {found_complaint['shipping_response_time']}")
                if found_complaint.get('shipping_media_links'):
                    st.markdown(f"**{t['shipping_media_links']}:**")
                    display_media_from_links(found_complaint['shipping_media_links'])
            else:
                st.info(t['no_shipping_response'])

            # --- Display CS Comments (if any) ---
            if found_complaint.get('cs_comments'):
                st.markdown(f"**{t['cs_comments_section']}**:")
                # Highlight the last CS comment
                for i, comment in enumerate(found_complaint['cs_comments']):
                    if i == len(found_complaint['cs_comments']) - 1: # Last comment
                        st.markdown(f"<p class='latest-cs-comment-label'>{t['latest_comment_label']}</p>", unsafe_allow_html=True) # Display the label
                        st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"cs_existing_comment_{uuid.uuid4()}")
                    else:
                        st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"cs_existing_comment_{uuid.uuid4()}")
            
            # --- Display Shipping Comments (if any) ---
            if found_complaint.get('shipping_comments'):
                st.markdown(f"**{t['shipping_comments_section']}:**")
                for comment in found_complaint['shipping_comments']:
                    st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"shipping_existing_comment_cs_{uuid.uuid4()}")
        else:
            st.error(f"**{t['complaint_not_found']}**")
    
    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # --- Add new complaint ---
    st.subheader(f"**{t['add_complaint']}**")
    with st.form("add_complaint_form", clear_on_submit=True):
        col_num, col_date, col_time, col_employee = st.columns(4)
        
        with col_num:
            complaint_number = colored_input_container(t['complaint_number'], "#e0f7fa", "cs_form_complaint_number", placeholder="أدخل رقم الشكوى")
        with col_date:
            complaint_date = colored_input_container(t['complaint_date'], "#e8f5e9", "cs_form_complaint_date", input_type="date")
        with col_time:
            complaint_time = colored_input_container(t['complaint_time'], "#fff3e0", "cs_form_complaint_time", input_type="time")
        with col_employee:
            employee_name = colored_input_container(t['employee_name'], "#f3e5f5", "cs_form_employee_name", default_value=st.session_state.get('employee_name_default', ''))
            st.session_state.employee_name_default = employee_name

        col_type, col_customer, col_phone = st.columns(3) # Added a column for phone
        with col_type:
            complaint_type = colored_input_container(
                t['complaint_type'], 
                "#e6ffe6",
                "cs_form_complaint_type", 
                input_type="selectbox", 
                options=t['complaint_type_options']
            )
        with col_customer:
            customer_name = colored_input_container(t['customer_name'], "#ffe0b2", "cs_form_customer_name", placeholder="أدخل اسم العميل")
        with col_phone: # New phone input
            customer_phone = colored_input_container(t['customer_phone'], "#d1e7dd", "cs_form_customer_phone", placeholder="أدخل رقم هاتف العميل")


        issue_description = st.text_area(f"**{t['issue_description']}**", key="cs_new_issue_description", height=150)
        
        # --- Add field for media links ---
        cs_media_links_input = st.text_area(
            f"**{t['add_media_link']}** (ضع كل رابط في سطر جديد)",
            key="cs_media_links_input",
            height=100,
            placeholder="مثال:\nhttps://example.com/image.jpg\nhttps://example.com/video.mp4"
        )
        
        # --- File uploader (for preview only) ---
        uploaded_file = st.file_uploader(f"**{t['add_media_upload']}**", type=["jpg", "jpeg", "png", "mp4", "mov"], key="cs_file_uploader")
        if uploaded_file:
            st.info("تم رفع الملف للمعاينة. لكي يتم حفظه بشكل دائم، يرجى وضع رابط الملف في خانة 'إضافة رابط صورة/فيديو'.")
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption="معاينة الصورة المرفوعة", use_container_width=False)
            elif uploaded_file.type.startswith('video'):
                st.video(uploaded_file, caption="معاينة الفيديو المرفوع", format=uploaded_file.type, start_time=0)

        if st.form_submit_button(f"**{t['submit_complaint']}**"):
            if complaint_number and customer_name and issue_description and employee_name and complaint_type and customer_phone: # Added customer_phone to validation
                # Split links by newline and filter out empty strings
                parsed_cs_media_links = [link.strip() for link in cs_media_links_input.split('\n') if link.strip()]

                new_complaint_data = {
                    "complaint_number": complaint_number,
                    "date": str(complaint_date),
                    "time": str(complaint_time),
                    "employee_name": employee_name,
                    "customer_name": customer_name,
                    "customer_phone": customer_phone, # Save customer phone
                    "complaint_type": complaint_type,
                    "issue_description": issue_description,
                    "cs_media_links": parsed_cs_media_links, # Save media links
                    "status": t['status_options'][0],
                    "shipping_response": "",
                    "shipping_response_date": None, # Initialize as None
                    "shipping_response_time": None, # Initialize as None
                    "shipping_media_links": [], # Use media links for shipping
                    "shipping_response_employee_name": "",
                    "cs_comments": [], # Initialize cs_comments as an empty list
                    "has_new_cs_comment": False, # Initialize new flag
                    "shipping_comments": [] # Initialize shipping comments
                }
                # --- Call Firestore function to add complaint ---
                add_complaint_to_firestore(new_complaint_data)
                # --- Reload data from Firestore ---
                st.session_state.complaints = load_complaints_from_firestore()
                st.rerun()
            else:
                st.warning("الرجاء ملء جميع الحقول المطلوبة (رقم الشكوى، اسم العميل، هاتف العميل، تفاصيل الشكوى، اسم الموظف، نوع الشكوى).")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # --- Add New Comment to Existing Complaint ---
    st.subheader(f"**{t['add_cs_comment']}**")
    # Filter for complaints that have a shipping response or are "تم الحل" or "مغلق"
    commentable_complaints = [c for c in st.session_state.complaints if c.get('shipping_response') or c['status'] in ["تم الحل", "مغلق"]]

    if commentable_complaints:
        # Create a list of display strings for the selectbox, including complaint number, customer name, and status
        complaint_display_options = [
            f"{c['complaint_number']} - {c['customer_name']} ({c['status']})"
            for c in commentable_complaints
        ]
        selected_complaint_display = st.selectbox(
            f"**{t['select_complaint']}**",
            options=complaint_display_options,
            key="cs_select_complaint_for_comment"
        )
        
        # Find the actual complaint object based on the selected display string
        selected_complaint_data = next(
            (c for c in commentable_complaints if f"{c['complaint_number']} - {c['customer_name']} ({c['status']})" == selected_complaint_display),
            None
        )

        if selected_complaint_data:
            selected_doc_id_for_comment = selected_complaint_data['doc_id']
            st.write(f"**{t['complaint_number']}:** {selected_complaint_data['complaint_number']}")
            st.write(f"**{t['customer_name']}:** {selected_complaint_data['customer_name']}")
            st.write(f"**{t['status']}:** {selected_complaint_data['status']}")
            if selected_complaint_data.get('shipping_response'):
                st.info(f"**{t['shipping_response']}**: {selected_complaint_data['shipping_response']}")
            
            # Display existing CS comments
            if selected_complaint_data.get('cs_comments'):
                st.markdown(f"**{t['cs_comments_section']}**:")
                # Highlight the last CS comment
                for i, comment in enumerate(selected_complaint_data['cs_comments']):
                    if i == len(selected_complaint_data['cs_comments']) - 1: # Last comment
                        st.markdown(f"<p class='latest-cs-comment-label'>{t['latest_comment_label']}</p>", unsafe_allow_html=True) # Display the label
                        st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"cs_existing_comment_{uuid.uuid4()}")
                    else:
                        st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"cs_existing_comment_{uuid.uuid4()}")

            # Display existing Shipping comments (for CS to see their replies)
            if selected_complaint_data.get('shipping_comments'):
                st.markdown(f"**{t['shipping_comments_section']}**:")
                for comment in selected_complaint_data['shipping_comments']:
                    st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"shipping_existing_comment_cs_view_{uuid.uuid4()}")


            with st.form("add_cs_comment_form", clear_on_submit=True):
                comment_text = st.text_area(f"**{t['cs_comment_text']}**", key="cs_comment_input", height=100)
                comment_employee_name = colored_input_container(t['employee_name'], "#f3e5f5", "cs_comment_employee_name", default_value=st.session_state.get('employee_name_default', ''))

                if st.form_submit_button(f"**{t['submit_comment']}**"):
                    if comment_text and comment_employee_name:
                        current_time = datetime.now()
                        new_comment = {
                            "comment": comment_text,
                            "employee_name": comment_employee_name,
                            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        # Fetch the latest complaint data before updating to append comments safely
                        current_complaint_from_db = db.collection('complaints').document(selected_doc_id_for_comment).get().to_dict()
                        if current_complaint_from_db:
                            existing_comments = current_complaint_from_db.get('cs_comments', [])
                            existing_comments.append(new_comment)
                            
                            # Also set a flag to indicate new CS comment for shipping team
                            update_data = {
                                "cs_comments": existing_comments,
                                "has_new_cs_comment": True # Flag for shipping team
                            }
                            update_complaint_in_firestore(selected_doc_id_for_comment, update_data)
                            st.session_state.complaints = load_complaints_from_firestore()
                            st.rerun()
                        else:
                            st.error("لم يتم العثور على الشكوى لتحديثها.")
                    else:
                        st.warning("الرجاء إدخال التعليق واسم الموظف.")
    else:
        st.info("لا توجد شكاوى يمكن إضافة تعليقات عليها حالياً (يجب أن تكون الشكوى قد تلقت رد الشحن أو تم حلها/إغلاقها).")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # --- Display current complaints (for Customer Service) ---
    st.subheader(f"**{t['current_complaints']}**")
    if st.session_state.complaints:
        # Ensure 'complaint_number' is used as index for sorting if it's the doc_id
        # For display, sort by date and time
        df_complaints = pd.DataFrame(st.session_state.complaints).sort_values(by=['date', 'time'], ascending=[False, False])
        
        display_df = df_complaints.copy()
        # Hide doc_id as it's an internal Firestore ID
        if 'doc_id' in display_df.columns:
            display_df = display_df.drop(columns=['doc_id'])
        # Hide shipping-related fields from CS view
        for col in ['shipping_response_date', 'shipping_response_time', 'shipping_media_links', 'shipping_response_employee_name', 'has_new_cs_comment']: # Hide new flag too
            if col in display_df.columns:
                display_df = display_df.drop(columns=[col])

        # Custom display for cs_comments list and shipping_comments list
        # Ensure these columns exist before applying format_comments_for_dataframe_display
        for col_name in ['cs_comments', 'shipping_comments']:
            if col_name not in display_df.columns:
                display_df[col_name] = [[] for _ in range(len(display_df))]

        display_df['cs_comments_display'] = display_df['cs_comments'].apply(format_comments_for_dataframe_display)
        display_df['shipping_comments_display'] = display_df['shipping_comments'].apply(format_comments_for_dataframe_display)
        
        # Now drop the original list columns
        display_df = display_df.drop(columns=['cs_comments', 'shipping_comments'])


        st.dataframe(display_df.rename(columns={
            "complaint_number": t['complaint_number'],
            "date": t['complaint_date'],
            "time": t['complaint_time'],
            "employee_name": t['employee_name'],
            "customer_name": t['customer_name'],
            "customer_phone": f"📞 {t['customer_phone']}", # Display customer phone with icon
            "complaint_type": t['complaint_type'],
            "issue_description": t['issue_description'],
            "cs_media_links": t['cs_media_links'], # Display media links
            "status": t['status'],
            "shipping_response": t['shipping_response'],
            "cs_comments_display": t['cs_comments_section'], # Display formatted CS comments
            "shipping_comments_display": t['shipping_comments_section'] # Display formatted shipping comments
        }), use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد شكاوى حالياً.")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    if st.button(f"**{t['logout']}**", key="cs_logout_btn"):
        st.session_state.logged_in = False
        st.session_state.selected_role = None
        st.session_state.current_page = "role_selection"
        st.rerun()

def shipping_dashboard():
    """
    Shipping dashboard.
    Allows viewing complaints from Customer Service and adding responses.
    """
    st.markdown(f"<h2 style='text-align: center; color: #1f2937;'>{t['shipping_dashboard_welcome']}</h2>", unsafe_allow_html=True)

    # Filter complaints
    all_complaints = st.session_state.complaints
    
    # Complaints that have 'has_new_cs_comment' flag set to True
    # This section will now show ALL complaints with new CS comments, regardless of current status.
    # This is to ensure no new CS comments are missed by the shipping team.
    new_cs_comments_to_review = [
        c for c in all_complaints
        if c.get('has_new_cs_comment', False)
    ]
    
    # New and In-Progress Complaints (primary workflow for shipping).
    # These should NOT include complaints already highlighted in 'new_cs_comments_to_review'
    # to avoid duplication in display.
    new_and_in_progress_complaints_filtered = [ 
        c for c in all_complaints
        if c['status'] in ["جديد", "قيد المعالجة", "جاري المتابعة"] and c not in new_cs_comments_to_review
    ]
    
    # Complaints that are resolved/closed and DO NOT have new CS comments.
    # Also ensure they are not in new_cs_comments_to_review
    resolved_and_closed_complaints_for_old_section = [
        c for c in all_complaints
        if c['status'] in ["تم الحل", "مغلق"] and not c.get('has_new_cs_comment', False)
    ]

    # --- Complaints with New CS Comments Section (for ALL complaints with new follow-ups) ---
    st.subheader(f"**{t['complaints_with_new_cs_comments']}**")
    if new_cs_comments_to_review: # Changed from new_cs_comments_on_resolved
        for complaint in new_cs_comments_to_review: # Changed from new_cs_comments_on_resolved
            doc_id = complaint.get('doc_id')
            if not doc_id:
                st.warning(f"Complaint without document ID (doc_id): {complaint.get('complaint_number', 'Unknown')}. It will not be updated in Firestore.")
                continue

            # Display title using st.markdown outside of expander for HTML
            expander_title_html = (
                f"🔴 **{t['new_comment_from_cs']}**: شكوى رقم: {complaint['complaint_number']} - العميل: {complaint['customer_name']} - الحالة: {complaint['status']} - النوع: {complaint.get('complaint_type', 'N/A')}"
            )
            st.markdown(expander_title_html, unsafe_allow_html=True) # Display the HTML title
            with st.expander(" ", expanded=True): # Removed key as requested
                st.markdown(f'<div class="cs-comment-highlight">', unsafe_allow_html=True)
                st.markdown(f"<h4>{t['new_comment_from_cs']}</h4>", unsafe_allow_html=True)
                st.write(f"**{t['complaint_date']}:** {complaint['date']}")
                st.write(f"**{t['complaint_time']}:** {complaint['time']}")
                st.write(f"**{t['employee_name']}:** {complaint['employee_name']}")
                st.write(f"**{t['customer_name']}:** {complaint['customer_name']}")
                st.write(f"**📞 {t['customer_phone']}:** {complaint.get('customer_phone', 'N/A')}")
                st.write(f"**{t['complaint_type']}:** {complaint['complaint_type']}")
                st.write(f"**{t['issue_description']}:** {complaint['issue_description']}")

                if complaint.get('cs_media_links'):
                    st.markdown(f"**{t['cs_media_links']}:** (مرفقات خدمة العملاء)")
                    display_media_from_links(complaint['cs_media_links'])
                
                # Display existing CS comments
                if complaint.get('cs_comments'):
                    st.markdown(f"**{t['cs_comments_section']}:**")
                    # Highlight the last CS comment with a label
                    for i, comment in enumerate(complaint['cs_comments']):
                        if i == len(complaint['cs_comments']) - 1: # Last comment
                            st.markdown(f"<p class='latest-cs-comment-label'>{t['latest_comment_label']}</p>", unsafe_allow_html=True) # Display the label
                            st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"shipping_view_cs_comment_{complaint['complaint_number']}_{uuid.uuid4()}") # Unique key
                        else:
                            st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"shipping_view_cs_comment_{complaint['complaint_number']}_{uuid.uuid4()}") # Unique key

                # Display existing Shipping comments (if any)
                if complaint.get('shipping_comments'):
                    st.markdown(f"**{t['shipping_comments_section']}:**")
                    for comment in complaint['shipping_comments']:
                        st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"shipping_view_shipping_comment_{complaint['complaint_number']}_{uuid.uuid4()}")

                # Section for Shipping to reply to CS comments
                st.subheader(f"**{t['shipping_comment_text']}**")
                shipping_comment_input = st.text_area(f"أدخل ردك هنا على تعليق خدمة العملاء:", key=f"shipping_reply_input_{complaint['complaint_number']}", height=100)
                shipping_comment_employee_name = colored_input_container(t['shipping_employee_name'], "#f3e5f5", f"shipping_reply_employee_name_{complaint['complaint_number']}", default_value=st.session_state.get('shipping_employee_name_default', ''))
                st.session_state.shipping_employee_name_default = shipping_comment_employee_name # Save for next time

                if st.button(f"**{t['submit_shipping_comment']}**", key=f"submit_shipping_reply_btn_{complaint['complaint_number']}"):
                    if shipping_comment_input and shipping_comment_employee_name:
                        current_time = datetime.now()
                        new_shipping_comment = {
                            "comment": shipping_comment_input,
                            "employee_name": shipping_comment_employee_name,
                            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
                        }

                        current_complaint_from_db = db.collection('complaints').document(doc_id).get().to_dict()
                        if current_complaint_from_db:
                            existing_shipping_comments = current_complaint_from_db.get('shipping_comments', [])
                            existing_shipping_comments.append(new_shipping_comment)

                            update_data = {
                                "shipping_comments": existing_shipping_comments,
                                "has_new_cs_comment": False # Mark the CS comment as reviewed when replying
                            }
                            update_complaint_in_firestore(doc_id, update_data)
                            st.success(t['shipping_comment_added_successfully'])
                            st.session_state.complaints = load_complaints_from_firestore()
                            st.rerun()
                        else:
                            st.error("لم يتم العثور على الشكوى لتحديثها.")
                    else:
                        st.warning("الرجاء إدخال الرد واسم الموظف.")

                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info(t['no_new_cs_comments'])

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)


    # --- Split page into two columns for New/In-Progress and Old Complaints ---
    col_new_complaints, col_old_complaints = st.columns([0.6, 0.4])

    with col_new_complaints:
        # --- New and In-Progress Complaints Section ---
        st.subheader(f"**{t['current_complaints']}** (الشكاوى الجديدة وقيد المعالجة)")
        
        # Group complaints by type and sort them
        complaints_by_type = {}
        for complaint in new_and_in_progress_complaints_filtered: # Use the filtered list for this section
            c_type = complaint.get('complaint_type', 'غير محدد')
            if c_type not in complaints_by_type:
                complaints_by_type[c_type] = []
            complaints_by_type[c_type].append(complaint)

        if complaints_by_type:
            # Define colors for each complaint type (you can expand this as needed)
            type_colors = {
                "ارجاع لقيمة الطلب": "#FFECB3", # Light Orange
                "الغاء الطلب": "#FFCDD2",      # Light Red
                "تاخير & استعجال": "#DCEDC8",  # Light Green
                "منتجات تالفه & ناقصه": "#BBDEFB", # Light Blue
                "تحديث معلومات الطلب": "#E1BEE7", # Light Purple
                "تذكير": "#FFE0B2",            # Light Brown
                "طلب توصيل سريع": "#C8E6C9",   # A bit darker green
                "غير محدد": "#f0f0f0",         # Grey for undefined
            }

            for c_type in sorted(complaints_by_type.keys()):
                # Create a clean CSS class name from the type
                # Handle cases where characters might not be valid in CSS class names
                css_class = c_type.replace(" ", "-").replace("&", "").replace("أ", "ا").replace("إ", "ا").replace("ئ", "ي").replace("ؤ", "و").replace("ة", "ه").strip().lower()

                header_color = type_colors.get(c_type, '#e0f7fa') # Default light blue

                st.markdown(
                    f'<div class="complaint-type-header {css_class}" style="background-color: {header_color};">'
                    f'{t["complaint_type"]}: {c_type}'
                    f'</div>', unsafe_allow_html=True
                )
                for complaint in complaints_by_type[c_type]:
                    doc_id = complaint.get('doc_id')
                    if not doc_id:
                        st.warning(f"Complaint without document ID (doc_id): {complaint.get('complaint_number', 'Unknown')}. It will not be updated in Firestore.")
                        continue

                    # Expander Title (unchanged as type is in header above)
                    with st.expander(f"**شكوى رقم: {complaint['complaint_number']} - العميل: {complaint['customer_name']} - الحالة: {complaint['status']}**"):
                        st.write(f"**{t['complaint_date']}:** {complaint['date']}")
                        st.write(f"**{t['complaint_time']}:** {complaint['time']}")
                        st.write(f"**{t['employee_name']}:** {complaint['employee_name']}")
                        st.write(f"**{t['customer_name']}:** {complaint['customer_name']}")
                        st.write(f"**📞 {t['customer_phone']}:** {complaint.get('customer_phone', 'N/A')}") # Display customer phone
                        st.write(f"**{t['complaint_type']}:** {complaint['complaint_type']}")
                        st.write(f"**{t['issue_description']}:** {complaint['issue_description']}")
                        
                        if complaint.get('cs_media_links'):
                            st.markdown(f"**{t['cs_media_links']}:** (مرفقات خدمة العملاء)")
                            display_media_from_links(complaint['cs_media_links'])
                        
                        # Display existing CS comments
                        if complaint.get('cs_comments'):
                            st.markdown(f"**{t['cs_comments_section']}:**")
                            # Highlight the last CS comment
                            for i, comment in enumerate(complaint['cs_comments']):
                                if i == len(complaint['cs_comments']) - 1: # Last comment
                                    st.markdown(f"<p class='latest-cs-comment-label'>{t['latest_comment_label']}</p>", unsafe_allow_html=True) # Display the label
                                    st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"shipping_view_cs_comment_{complaint['complaint_number']}_{uuid.uuid4()}") # Unique key
                                else:
                                    st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"shipping_view_cs_comment_{complaint['complaint_number']}_{uuid.uuid4()}") # Unique key

                        # Display previous shipping media links
                        if complaint.get('shipping_media_links'):
                            st.markdown(f"**{t['shipping_media_links']}:** (المرفقات السابقة)")
                            display_media_from_links(complaint['shipping_media_links'])

                        # Display existing Shipping comments (if any)
                        if complaint.get('shipping_comments'):
                            st.markdown(f"**{t['shipping_comments_section']}:**")
                            for comment in complaint['shipping_comments']:
                                st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"shipping_view_shipping_comment_regular_{complaint['complaint_number']}_{uuid.uuid4()}")

                        st.subheader(f"**{t['add_shipping_response']}**")
                        current_response = complaint.get('shipping_response', '')
                        response_text = st.text_area(t['response_text'], value=current_response, key=f"shipping_response_{complaint['complaint_number']}", height=100)
                        
                        # --- Shipping employee name field ---
                        current_shipping_employee_name = complaint.get('shipping_response_employee_name', '')
                        shipping_employee_name_input = st.text_input(
                            f"**{t['shipping_employee_name']}**",
                            value=current_shipping_employee_name,
                            key=f"shipping_employee_name_input_{complaint['complaint_number']}",
                            placeholder="أدخل اسم موظف الشحن"
                        )

                        # --- New: Shipping Response Date and Time fields ---
                        col_resp_date, col_resp_time = st.columns(2)
                        with col_resp_date:
                            # Default to current date if no previous response date
                            default_resp_date = datetime.now().date()
                            if complaint.get('shipping_response_date'):
                                try:
                                    default_resp_date = datetime.strptime(complaint['shipping_response_date'], '%Y-%m-%d').date()
                                except ValueError:
                                    pass # Keep default if parsing fails
                            shipping_response_date_input = colored_input_container(
                                t['shipping_response_date_input'], 
                                "#e0f7fa", 
                                f"shipping_response_date_{complaint['complaint_number']}", 
                                input_type="date", 
                                default_value=default_resp_date
                            )
                        with col_resp_time:
                            # Default to current time if no previous response time
                            default_resp_time = datetime.now().time()
                            if complaint.get('shipping_response_time'):
                                try:
                                    default_resp_time = datetime.strptime(complaint['shipping_response_time'], '%H:%M:%S').time()
                                except ValueError:
                                    try: # Handle HH:MM format
                                        default_resp_time = datetime.strptime(complaint['shipping_response_time'], '%H:%M').time()
                                    except ValueError:
                                        pass # Keep default if parsing fails
                            shipping_response_time_input = colored_input_container(
                                t['shipping_response_time_input'], 
                                "#e8f5e9", 
                                f"shipping_response_time_{complaint['complaint_number']}", 
                                input_type="time", 
                                default_value=default_resp_time
                            )

                        # --- Add field for shipping media links ---
                        current_shipping_media_links_str = "\n".join(complaint.get('shipping_media_links', []))
                        shipping_media_links_input = st.text_area(
                            f"**{t['add_media_link']}** (ضع كل رابط في سطر جديد)",
                            value=current_shipping_media_links_str,
                            key=f"shipping_media_links_input_{complaint['complaint_number']}",
                            height=100,
                            placeholder="مثال:\nhttps://example.com/image.jpg\nhttps://example.com/video.mp4"
                        )
                        
                        # --- File uploader (for preview only) ---
                        uploaded_media = st.file_uploader(
                            f"**{t['add_media_upload']}**", 
                            type=["jpg", "png", "jpeg", "mp4"], 
                            accept_multiple_files=True,
                            key=f"shipping_media_uploader_{complaint['complaint_number']}"
                        )
                        if uploaded_media:
                            st.info("تم رفع الملفات للمعاينة. لكي يتم حفظها بشكل دائم، يرجى وضع روابط الملفات في خانة 'إضافة رابط صورة/فيديو'.")
                            for i, file in enumerate(uploaded_media):
                                if file.type.startswith('image'):
                                    st.image(file, caption=f"معاينة الصورة المرفوعة {i+1}", use_container_width=False)
                                elif file.type.startswith('video'):
                                    st.video(file, caption=f"معاينة الفيديو المرفوع {i+1}", format=file.type, start_time=0)

                        initial_shipping_status_index = 0
                        if complaint['status'] == "تم الحل":
                            initial_shipping_status_index = 1
                        elif complaint['status'] in ["قيد المعالجة", "جديد", "جاري المتابعة"]:
                            initial_shipping_status_index = 0
                        
                        selected_shipping_status = st.radio(
                            "**تحديث حالة الشكوى:**",
                            options=t['shipping_status_options'],
                            index=initial_shipping_status_index,
                            key=f"shipping_status_radio_{complaint['complaint_number']}"
                        )

                        if st.button(f"**{t['save_response']}**", key=f"save_response_btn_{complaint['complaint_number']}"):
                            new_status_for_db = selected_shipping_status
                            
                            # Parse shipping media links
                            parsed_shipping_media_links = [link.strip() for link in shipping_media_links_input.split('\n') if link.strip()]

                            update_data = {
                                "shipping_response": response_text,
                                "shipping_response_employee_name": shipping_employee_name_input,
                                "status": new_status_for_db,
                                "shipping_response_date": str(shipping_response_date_input), # Save as string
                                "shipping_response_time": str(shipping_response_time_input), # Save as string
                                "shipping_media_links": parsed_shipping_media_links # Save shipping media links
                            }
                            # --- Call Firestore function to update complaint ---
                            update_complaint_in_firestore(doc_id, update_data)
                            # --- Reload data from Firestore ---
                            st.session_state.complaints = load_complaints_from_firestore()
                            st.rerun()
                        st.markdown("---")
            st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True) # Separator after each type group
        else:
            st.info("لا توجد شكاوى جديدة أو قيد المعالجة حالياً.")

    with col_old_complaints:
        # --- NEW: Add Administrative Action Request Section (Form) ---
        st.subheader(f"**{t['admin_action_request']}**")
        with st.form("add_admin_action_request_form", clear_on_submit=True):
            req_col1, req_col2, req_col3 = st.columns(3)
            with req_col1:
                req_complaint_number = colored_input_container(t['complaint_number'], "#e0f7fa", "req_complaint_number", placeholder="أدخل رقم الشكوى")
            with req_col2:
                req_request_date = colored_input_container(t['request_date'], "#e8f5e9", "req_request_date", input_type="date")
            with req_col3:
                req_customer_receipt_date = colored_input_container(t['customer_receipt_date'], "#fff3e0", "req_customer_receipt_date", input_type="date")

            req_col4, req_col5, req_col6 = st.columns(3)
            with req_col4:
                req_shipping_company = colored_input_container(t['shipping_company'], "#f3e5f5", "req_shipping_company", placeholder="أدخل اسم شركة الشحن")
            with req_col5:
                req_order_status = colored_input_container(t['order_status'], "#e6ffe6", "req_order_status", placeholder="أدخل حالة الطلب")
            with req_col6:
                req_employee_name = colored_input_container(t['request_employee_name'], "#ffe0b2", "req_employee_name", default_value=st.session_state.get('shipping_employee_name_default', ''))
                st.session_state.shipping_employee_name_default = req_employee_name # Persist name

            req_details = st.text_area(f"**{t['request_details']}**", key="req_details_input", height=150)
            req_media_link = st.text_input(f"**{t['request_media_link']}** (رابط واحد فقط)", key="req_media_link_input", placeholder="مثال: https://example.com/proof.jpg")

            if st.form_submit_button(f"**{t['submit_request']}**"):
                if (req_complaint_number and req_request_date and req_customer_receipt_date and
                    req_shipping_company and req_order_status and req_details and req_employee_name):
                    
                    request_data = {
                        "complaint_number": req_complaint_number,
                        "request_date": str(req_request_date),
                        "customer_receipt_date": str(req_customer_receipt_date),
                        "shipping_company": req_shipping_company,
                        "order_status": req_order_status,
                        "request_details": req_details,
                        "media_link": req_media_link if req_media_link else None, # Store as None if empty
                        "employee_name": req_employee_name,
                        "status": t['pending_approval'], # Initial status
                        "approval_action": "",
                        "approved_by_employee": "",
                        "approval_date": None,
                        "approval_time": None
                    }
                    add_admin_request_to_firestore(request_data)
                    st.session_state.admin_requests = load_admin_requests_from_firestore() # Reload requests
                    st.rerun()
                else:
                    st.warning("الرجاء ملء جميع الخانات المطلوبة لطلب الإجراء الإداري.")
        
        st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
        # --- END NEW: Add Administrative Action Request Section (Form) ---


        # --- NEW: Approved/Rejected Administrative Actions Display for Shipping Team ---
        st.subheader(f"**{t['approved_rejected_requests']}**")
        processed_admin_requests = [req for req in st.session_state.admin_requests if req['status'] in [t['approved'], t['rejected']]]

        if processed_admin_requests:
            # Sort processed requests by approval date/time, newest first
            processed_admin_requests_sorted = sorted(processed_admin_requests, 
                                                     key=lambda x: datetime.strptime(f"{x.get('approval_date', '1900-01-01')} {x.get('approval_time', '00:00:00')}", '%Y-%m-%d %H:%M:%S') if x.get('approval_date') and x.get('approval_time') else datetime.min, 
                                                     reverse=True)
            
            for request in processed_admin_requests_sorted:
                expander_title = (
                    f"**{t['request_status_summary']}**: {request.get('complaint_number', 'N/A')} "
                    f"- الحالة: <span class='badge {request.get('status', '').lower()}'>{request.get('status', 'N/A')}</span>"
                )
                # Display the title first with markdown, then the expander
                st.markdown(expander_title, unsafe_allow_html=True) 
                with st.expander(" ", expanded=False): # Removed key as requested
                    # st.write(f"**{t['admin_request_id']}:** {request.get('request_id', 'N/A')}") # Hidden
                    st.write(f"**{t['complaint_number']}:** {request.get('complaint_number', 'N/A')}")
                    st.write(f"**{t['action_employee']}:** {request.get('employee_name', 'N/A')}")
                    st.write(f"**{t['request_date']}:** {request.get('request_date', 'N/A')}")
                    st.write(f"**{t['customer_receipt_date']}:** {request.get('customer_receipt_date', 'N/A')}")
                    st.write(f"**{t['shipping_company']}:** {request.get('shipping_company', 'N/A')}")
                    st.write(f"**{t['order_status']}:** {request.get('order_status', 'N/A')}")
                    st.write(f"**{t['request_details']}:** {request.get('request_details', 'N/A')}")

                    if request.get('media_link'):
                        st.markdown(f"**{t['request_media_link']}:**")
                        display_media_from_links([request['media_link']])

                    st.markdown("---")
                    # Display based on actual status (Approved or Rejected)
                    if request.get('status') == t['approved']:
                        st.markdown(f"**{t['approval_status']}:** <span class='badge approved'>{t['approved']}</span>", unsafe_allow_html=True)
                        if request.get('approval_action'):
                            st.write(f"**{t['approved_request_details']}:** {request['approval_action']}") # Corrected key
                    elif request.get('status') == t['rejected']:
                        st.markdown(f"**{t['approval_status']}:** <span class='badge rejected'>{t['rejected']}</span>", unsafe_allow_html=True)
                        if request.get('approval_action'):
                            st.write(f"**{t['rejected_request_details']}:** {request['approval_action']}") # Corrected key
                    else: # Fallback for other statuses
                        st.markdown(f"**{t['approval_status']}:** <span class='badge pending'>{request.get('status', 'N/A')}</span>", unsafe_allow_html=True)

                    if request.get('approved_by_employee'):
                        st.write(f"**{t['approved_by_label']}:** {request['approved_by_employee']}")
                    if request.get('approval_date'):
                        st.write(f"**{t['approval_date_label']}:** {request['approval_date']}")
                    if request.get('approval_time'):
                        st.write(f"**{t['approval_time_label']}:** {request['approval_time']}")
                    st.markdown("---")

        else:
            st.info("لا توجد طلبات إجراء إداري تم التعامل معها حالياً.")

        st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
        # --- END NEW: Approved/Rejected Administrative Actions Display ---


        # --- Old Complaints Section (with search and EXCLUDED DELETE OPTION) ---
        st.subheader(f"**{t['old_complaints']}** (الشكاوى التي تم حلها أو إغلاقها)")

        search_old_complaint_number = st.text_input(f"**{t['search_old_complaints']}**", placeholder=t['complaint_number'], key="shipping_old_search_number")
        
        if resolved_and_closed_complaints_for_old_section:
            old_complaint_types = [t['all']] + list(set(c['complaint_type'] for c in resolved_and_closed_complaints_for_old_section))
        else:
            old_complaint_types = [t['all']]

        filter_old_complaint_type = st.selectbox(f"**{t['filter_by_complaint_type']}**", options=old_complaint_types, key="shipping_old_filter_type")

        filtered_old_complaints_display = resolved_and_closed_complaints_for_old_section # Start with the filtered list
        if search_old_complaint_number:
            filtered_old_complaints_display = [c for c in filtered_old_complaints_display if c['complaint_number'] == search_old_complaint_number]
        
        if filter_old_complaint_type != t['all']:
            filtered_old_complaints_display = [c for c in filtered_old_complaints_display if c['complaint_type'] == filter_old_complaint_type]


        if filtered_old_complaints_display: # Check if there are complaints after all filters
            df_old_complaints_display_filtered = pd.DataFrame(filtered_old_complaints_display).sort_values(by=['date', 'time'], ascending=[False, False])
            
            # Ensure all comment columns exist and then format them
            for col_name in ['cs_comments', 'shipping_comments']:
                if col_name not in df_old_complaints_display_filtered.columns:
                    df_old_complaints_display_filtered[col_name] = [[] for _ in range(len(df_old_complaints_display_filtered))]

            df_old_complaints_display_filtered['cs_comments_formatted'] = df_old_complaints_display_filtered['cs_comments'].apply(format_comments_for_dataframe_display)
            df_old_complaints_display_filtered['shipping_comments_formatted'] = df_old_complaints_display_filtered['shipping_comments'].apply(format_comments_for_dataframe_display)

            # Drop original list columns before passing to data_editor
            df_old_complaints_display_filtered = df_old_complaints_display_filtered.drop(columns=['cs_comments', 'shipping_comments'])


            st.dataframe(
                df_old_complaints_display_filtered.rename(columns={
                    "complaint_number": t['complaint_number'],
                    "date": t['complaint_date'],
                    "time": t['complaint_time'],
                    "employee_name": t['employee_name'],
                    "customer_name": t['customer_name'],
                    "customer_phone": f"📞 {t['customer_phone']}", # Display customer phone with icon
                    "complaint_type": t['complaint_type'],
                    "issue_description": t['issue_description'],
                    "cs_media_links": t['cs_media_links'], # Display CS links
                    "status": t['status'],
                    "shipping_response": t['shipping_response'],
                    "shipping_response_date": t['shipping_response_date_kpi'], # Use new translation
                    "shipping_response_time": t['shipping_response_time_kpi'], # Use new translation
                    "shipping_media_links": t['shipping_media_links'], # Display shipping links
                    "shipping_response_employee_name": t['shipping_employee_name'],
                    "doc_id": "معرف المستند",
                    "cs_comments_formatted": t['cs_comments_section'], # Use formatted column
                    "has_new_cs_comment": "تعليق جديد من خدمة العملاء", # Add new flag column
                    "shipping_comments_formatted": t['shipping_comments_section'] # Use formatted shipping comments column
                }),
                column_config={
                    # REMOVED DELETE CHECKBOX FOR SHIPPING TEAM
                    "معرف المستند": st.column_config.TextColumn("معرف المستند", disabled=True),
                    t['shipping_response_date_kpi']: st.column_config.TextColumn(t['shipping_response_date_kpi'], disabled=True),
                    t['shipping_response_time_kpi']: st.column_config.TextColumn(t['shipping_response_time_kpi'], disabled=True),
                    t['cs_media_links']: st.column_config.ListColumn(t['cs_media_links'], width="medium"), # Display as list
                    t['shipping_media_links']: st.column_config.ListColumn(t['shipping_media_links'], width="medium"), # Display as list
                    t['cs_comments_section']: st.column_config.TextColumn(t['cs_comments_section'], width="large"), # Now it's text
                    "تعليق جديد من خدمة العملاء": st.column_config.CheckboxColumn("تعليق جديد من خدمة العملاء", disabled=True),
                    t['shipping_comments_section']: st.column_config.TextColumn(t['shipping_comments_section'], width="large") # Now it's text
                },
                hide_index=True,
                use_container_width=True,
                key="shipping_old_complaints_viewer" # Changed key to reflect it's just a viewer
            )

            # --- Excel Download for Shipping Old Complaints ---
            df_to_download_shipping_old = df_old_complaints_display_filtered.drop(columns=['doc_id', 'has_new_cs_comment'], errors='ignore')
            df_to_download_shipping_old = df_to_download_shipping_old.rename(columns={
                'cs_comments_formatted': t['cs_comments_section'],
                'shipping_comments_formatted': t['cs_comments_section']
            })

            excel_buffer = io.BytesIO()
            df_to_download_shipping_old.to_excel(excel_buffer, index=False, engine='xlsxwriter')
            excel_buffer.seek(0)
            st.download_button(
                label=t['download_excel'],
                data=excel_buffer,
                file_name="old_complaints.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_shipping_old_complaints_excel" # Unique key
            )
            # NO DELETE BUTTON OR MESSAGE FOR SHIPPING TEAM

        else:
            st.info("لا توجد شكاوى قديمة حالياً.")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    if st.button(f"**{t['logout']}**", key="shipping_logout_btn"):
        st.session_state.logged_in = False
        st.session_state.selected_role = None
        st.session_state.current_page = "role_selection"
        st.rerun()

def manager_dashboard():
    """
    Manager dashboard.
    Displays overview and reports.
    """
    st.markdown(f"<h2 style='text-align: center; color: #1f2937;'>{t['manager_dashboard_welcome']}</h2>", unsafe_allow_html=True)

    if st.session_state.complaints:
        df_complaints = pd.DataFrame(st.session_state.complaints)
        df_complaints['date'] = pd.to_datetime(df_complaints['date'])
        
        # Combine date and time to create datetime objects for proper calculation using pd.to_datetime
        # This will handle various time string formats gracefully
        df_complaints['complaint_datetime'] = df_complaints.apply(
            lambda row: pd.to_datetime(f"{row['date'].strftime('%Y-%m-%d')} {row['time']}") if isinstance(row['time'], str) and ':' in row['time'] else pd.NaT, axis=1
        )
        
        if 'shipping_response_date' in df_complaints.columns and 'shipping_response_time' in df_complaints.columns:
            # Create a combined shipping response datetime, handling potential None values using pd.to_datetime
            df_complaints['shipping_response_datetime'] = df_complaints.apply(
                lambda row: pd.to_datetime(f"{row['shipping_response_date']} {row['shipping_response_time']}") if pd.notna(row['shipping_response_date']) and pd.notna(row['shipping_response_time']) else pd.NaT, axis=1
            )
        else:
            df_complaints['shipping_response_datetime'] = pd.NaT # Use NaT for missing columns
    else:
        df_complaints = pd.DataFrame()

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
    
    # --- NEW: Admin Action Requests Section (Manager Approval) ---
    st.subheader(f"**{t['new_admin_actions_needed']}**")
    pending_admin_requests = [req for req in st.session_state.admin_requests if req['status'] == t['pending_approval']]

    if pending_admin_requests:
        # Sort requests by date (e.g., newest first)
        pending_admin_requests_sorted = sorted(pending_admin_requests, 
                                               key=lambda x: datetime.strptime(x.get('request_date', '1900-01-01'), '%Y-%m-%d'), 
                                               reverse=True)
        
        # Display each pending request in an expander for full details
        for req_data in pending_admin_requests_sorted:
            # Simplified Expander Title: "شكوى جديدة تحتاج اعتماد: رقم الشكوى: [رقم الشكوى] - الحالة: [الحالة]"
            expander_title_html = (
                f"**{t['new_admin_actions_needed'].split('جديدة')[0]}**" # "شكاوى "
                f"جديدة تحتاج اعتماد: رقم الشكوى: {req_data.get('complaint_number', 'N/A')} - "
                f"الحالة: <span class='badge pending'>{req_data.get('status', 'N/A')}</span>"
            )
            # Display the title first with markdown, then the expander
            st.markdown(expander_title_html, unsafe_allow_html=True) 
            with st.expander(" ", expanded=False): # Removed key as requested
                st.markdown(f"### {t['view_request_details']}") # Changed header to be more descriptive
                # st.write(f"**{t['admin_request_id']}:** {req_data.get('request_id', 'N/A')}") # Hiding this as requested
                st.write(f"**{t['complaint_number']}:** {req_data.get('complaint_number', 'N/A')}")
                st.write(f"**{t['request_employee_name']}:** {req_data.get('employee_name', 'N/A')}")
                st.write(f"**{t['request_date']}:** {req_data.get('request_date', 'N/A')}")
                st.write(f"**{t['customer_receipt_date']}:** {req_data.get('customer_receipt_date', 'N/A')}")
                st.write(f"**{t['shipping_company']}:** {req_data.get('shipping_company', 'N/A')}")
                st.write(f"**{t['order_status']}:** {req_data.get('order_status', 'N/A')}")
                st.write(f"**{t['request_details']}:** {req_data.get('request_details', 'N/A')}")

                if req_data.get('media_link'):
                    st.markdown(f"**{t['request_media_link']}:**")
                    display_media_from_links([req_data['media_link']])
                
                st.markdown("---")
                st.subheader(f"**{t['admin_action_approved']}**")
                with st.form(f"admin_approval_form_{req_data['request_id']}", clear_on_submit=True): # Unique key for form
                    approved_action_text_input = st.text_area(f"**{t['admin_action_approved']}**", key=f"approved_action_input_{req_data['request_id']}", height=150, value=req_data.get('approval_action', ''))
                    approved_by_name = colored_input_container(f"**{t['approved_by']}**", "#f3e5f5", f"approved_by_name_{req_data['request_id']}", default_value=st.session_state.get('manager_name_default', ''))
                    st.session_state.manager_name_default = approved_by_name

                    col_approve1, col_approve2 = st.columns(2)
                    with col_approve1:
                        approve_button = st.form_submit_button(f"**{t['approved']}**")
                    with col_approve2:
                        reject_button = st.form_submit_button(f"**{t['rejected']}**")

                    if approve_button or reject_button:
                        if approved_action_text_input and approved_by_name: # Use the local variable name here
                            current_datetime = datetime.now()
                            status_to_update = t['approved'] if approve_button else t['rejected']
                            update_data = {
                                "status": status_to_update,
                                "approval_action": approved_action_text_input, # Store the actual text from the input
                                "approved_by_employee": approved_by_name,
                                "approval_date": current_datetime.strftime("%Y-%m-%d"),
                                "approval_time": current_datetime.strftime("%H:%M:%S")
                            }
                            update_admin_request_in_firestore(req_data['request_id'], update_data) # Use request_id
                            st.session_state.admin_requests = load_admin_requests_from_firestore() # Reload requests
                            st.session_state.complaints = load_complaints_from_firestore() # Reload complaints as well for potential linking
                            st.rerun()
                        else:
                            st.warning("الرجاء ملء حقل الإجراء الإداري واسم معتمد الإجراء.")
            st.markdown("---") # Separator between request forms
    else:
        st.info(t['no_admin_actions_needed'])

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
    # --- END NEW: Admin Action Requests Section ---

    # --- NEW: Table of all Administrative Action Requests ---
    st.subheader(f"**{t['admin_requests_table_title']}**")
    if st.session_state.admin_requests:
        df_admin_requests = pd.DataFrame(st.session_state.admin_requests)
        
        # Add a checkbox column for deletion
        df_admin_requests['اختر للحذف'] = False 

        # Format dates/times for display
        df_admin_requests['request_date_display'] = df_admin_requests['request_date'].apply(lambda x: x if x else 'N/A')
        df_admin_requests['customer_receipt_date_display'] = df_admin_requests['customer_receipt_date'].apply(lambda x: x if x else 'N/A')
        df_admin_requests['approval_date_display'] = df_admin_requests['approval_date'].apply(lambda x: x if x else 'N/A')
        df_admin_requests['approval_time_display'] = df_admin_requests['approval_time'].apply(lambda x: x if x else 'N/A')

        edited_df_admin_requests = st.data_editor(
            df_admin_requests.rename(columns={
                "complaint_number": t['complaint_number'],
                "request_date_display": t['request_date'],
                "customer_receipt_date_display": t['customer_receipt_date'],
                "shipping_company": t['shipping_company'],
                "order_status": t['order_status'],
                "request_details": t['request_details'],
                "media_link": t['request_media_link'],
                "employee_name": t['request_employee_name'],
                "status": t['action_status'],
                "approval_action": t['approved_request_details'], # Use approved_request_details for column name
                "approved_by_employee": t['approved_by_label'],
                "approval_date_display": t['approval_date_label'],
                "approval_time_display": t['approval_time_label'],
                "request_id": t['admin_request_id'], # Keep request_id here for deletion logic
            }),
            column_config={
                "اختر للحذف": st.column_config.CheckboxColumn( # Checkbox for deletion
                    "اختر للحذف",
                    help="اختر الطلبات التي تريد حذفها",
                    default=False,
                ),
                t['admin_request_id']: st.column_config.TextColumn(t['admin_request_id'], disabled=True, width="small"),
                t['request_media_link']: st.column_config.LinkColumn(t['request_media_link'], help="رابط الصورة/الفيديو المرفق بالطلب"),
                # Make other columns read-only as this is just a display table
                t['complaint_number']: st.column_config.TextColumn(t['complaint_number'], disabled=True),
                t['request_date']: st.column_config.TextColumn(t['request_date'], disabled=True),
                t['customer_receipt_date']: st.column_config.TextColumn(t['customer_receipt_date'], disabled=True),
                t['shipping_company']: st.column_config.TextColumn(t['shipping_company'], disabled=True),
                t['order_status']: st.column_config.TextColumn(t['order_status'], disabled=True),
                t['request_details']: st.column_config.TextColumn(t['request_details'], disabled=True),
                t['request_employee_name']: st.column_config.TextColumn(t['request_employee_name'], disabled=True),
                t['action_status']: st.column_config.TextColumn(t['action_status'], disabled=True),
                t['approved_request_details']: st.column_config.TextColumn(t['approved_request_details'], disabled=True),
                t['approved_by_label']: st.column_config.TextColumn(t['approved_by_label'], disabled=True),
                t['approval_date_label']: st.column_config.TextColumn(t['approval_date_label'], disabled=True),
                t['approval_time_label']: st.column_config.TextColumn(t['approval_time_label'], disabled=True),
            },
            hide_index=True,
            use_container_width=True,
            key="manager_admin_requests_table" # Unique key
        )

        # Manager Delete Logic for Admin Requests
        selected_for_deletion_admin_requests = edited_df_admin_requests[edited_df_admin_requests['اختر للحذف'] == True][t['admin_request_id']].tolist()

        if selected_for_deletion_admin_requests:
            st.warning(t['confirm_delete_requests'])
            if st.button(f"**{t['delete_selected_requests']}**", key="manager_delete_admin_requests_btn"):
                for request_id_to_delete in selected_for_deletion_admin_requests:
                    delete_admin_request_from_firestore(request_id_to_delete)
                st.session_state.admin_requests = load_admin_requests_from_firestore() # Reload requests after deletion
                st.rerun()
        elif not df_admin_requests.empty:
            st.info(t['select_requests_to_delete'])


        excel_buffer_admin_requests = io.BytesIO()
        # Drop internal IDs and original unformatted date/time columns before export
        df_admin_requests_export = df_admin_requests.drop(columns=[
            'request_id', 'request_date', 'customer_receipt_date', 'approval_date', 'approval_time', 'اختر للحذف'
        ], errors='ignore').rename(columns={
            "request_date_display": t['request_date'],
            "customer_receipt_date_display": t['customer_receipt_date'],
            "approval_date_display": t['approval_date_label'],
            "approval_time_display": t['approval_time_label'],
            "approval_action": t['approved_request_details'], # Use new display text for Excel
        })
        df_admin_requests_export.to_excel(excel_buffer_admin_requests, index=False, engine='xlsxwriter')
        excel_buffer_admin_requests.seek(0)
        st.download_button(
            label=t['download_admin_requests_excel'],
            data=excel_buffer_admin_requests,
            file_name="admin_action_requests_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_admin_requests_excel_btn"
        )
    else:
        st.info("لا توجد طلبات إجراء إداري في النظام حالياً.")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)


    st.subheader(f"**{t['search_specific_complaint']}**")

    search_complaint_number_manager = st.text_input(f"**{t['complaint_number']}**", placeholder="أدخل رقم الشكوى للبحث", key="manager_search_complaint_number")
    
    found_complaint_manager = None
    if search_complaint_number_manager:
        found_complaint_manager = next((c for c in st.session_state.complaints if c['complaint_number'] == search_complaint_number_manager), None)

    if found_complaint_manager:
        st.success(f"**{t['complaint_found']}**")
        
        col_details, col_kpis = st.columns([0.6, 0.4])

        with col_details:
            st.markdown("### تفاصيل الشكوى")
            st.write(f"**{t['complaint_number']}:** {found_complaint_manager['complaint_number']}")
            st.write(f"**{t['complaint_date']}:** {found_complaint_manager['date']}")
            st.write(f"**{t['complaint_time']}:** {found_complaint_manager['time']}")
            st.write(f"**{t['employee_name']}:** {found_complaint_manager['employee_name']}")
            st.write(f"**{t['customer_name']}:** {found_complaint_manager['customer_name']}")
            st.write(f"**📞 {t['customer_phone']}:** {found_complaint_manager.get('customer_phone', 'N/A')}") # Display customer phone
            st.write(f"**{t['complaint_type']}:** {found_complaint_manager['complaint_type']}")
            st.write(f"**{t['issue_description']}:** {found_complaint_manager['issue_description']}")
            st.write(f"**{t['status']}:** {found_complaint_manager['status']}")
            
            if found_complaint_manager.get('cs_media_links'):
                st.markdown(f"**{t['cs_media_links']}:**")
                display_media_from_links(found_complaint_manager['cs_media_links'])
            
            st.markdown(f"**{t['shipping_response']}**")
            if found_complaint_manager['shipping_response']:
                st.info(found_complaint_manager['shipping_response'])
                if found_complaint_manager.get('shipping_response_employee_name'):
                    st.write(f"**{t['shipping_employee_name']}:** {found_complaint_manager['shipping_response_employee_name']}")
                # Display shipping response date and time
                if found_complaint_manager.get('shipping_response_date'):
                    st.write(f"**{t['shipping_response_date_kpi']}:** {found_complaint_manager['shipping_response_date']}")
                if found_complaint_manager.get('shipping_response_time'):
                    st.write(f"**{t['shipping_response_time_kpi']}:** {found_complaint_manager['shipping_response_time']}")
                if found_complaint_manager.get('shipping_media_links'):
                    st.markdown(f"**{t['shipping_media_links']}:**")
                    display_media_from_links(found_complaint_manager['shipping_media_links'])
            else:
                st.info(t['no_shipping_response'])

            # Display CS Comments (if any)
            if found_complaint_manager.get('cs_comments'):
                st.markdown(f"**{t['cs_comments_section']}:**")
                for comment in found_complaint_manager['cs_comments']:
                    st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"manager_view_cs_comment_{found_complaint_manager['complaint_number']}_{uuid.uuid4()}")

            # Display Shipping Comments (if any)
            if found_complaint_manager.get('shipping_comments'):
                st.markdown(f"**{t['shipping_comments_section']}:**")
                for comment in found_complaint_manager['shipping_comments']:
                    st.text_area(f"[{comment.get('timestamp', 'N/A')}] {comment.get('employee_name', 'N/A')}", value=comment.get('comment', ''), height=68, disabled=True, key=f"manager_view_shipping_comment_{found_complaint_manager['complaint_number']}_{uuid.uuid4()}")

        with col_kpis:
            st.markdown("### مؤشرات الأداء (KPIs)")
            
            # Display Complaint Recorded Date and Time
            st.markdown(
                f"""
                <div class="kpi-card avg-time small-value">
                    <p class="icon">🗓️</p>
                    <p class="title">{t['complaint_recorded_date']}</p>
                    <p class="value">{found_complaint_manager['date']}</p>
                </div>
                """, unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div class="kpi-card avg-time small-value">
                    <p class="icon">⏰</p>
                    <p class="title">{t['complaint_recorded_time']}</p>
                    <p class="value">{found_complaint_manager['time']}</p>
                </div>
                """, unsafe_allow_html=True
            )

            # Display Shipping Response Date and Time
            shipping_resp_date_display = found_complaint_manager.get('shipping_response_date', t['not_responded_yet'])
            shipping_resp_time_display = found_complaint_manager.get('shipping_response_time', t['not_responded_yet'])

            st.markdown(
                f"""
                <div class="kpi-card avg-time small-value">
                    <p class="icon">🗓️</p>
                    <p class="title">{t['shipping_response_date_kpi']}</p>
                    <p class="value">{shipping_resp_date_display}</p>
                </div>
                """, unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div class="kpi-card avg-time small-value">
                    <p class="icon">⏰</p>
                    <p class="title">{t['shipping_response_time_kpi']}</p>
                    <p class="value">{shipping_resp_time_display}</p>
                </div>
                """, unsafe_allow_html=True
            )
    elif search_complaint_number_manager:
        st.error(f"**{t['complaint_not_found']}**")
    else:
        st.info(f"**{t['no_complaint_selected']}**")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
    st.subheader(f"**{t['reports_and_analytics']}**")

    st.markdown("### 🔍 فلاتر البيانات", unsafe_allow_html=True)
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        today = datetime.today().date()
        date_range_input = st.date_input(f"📅 {t['filter_by_date']}", value=(today, today), key="manager_date_filter")
        
        if isinstance(date_range_input, tuple) and len(date_range_input) == 2:
            start_date, end_date = date_range_input
        elif isinstance(date_range_input, date):
            start_date = date_range_input
            end_date = date_range_input
        else: # Fallback for unexpected scenarios (e.g., empty or malformed input)
            st.warning("يرجى تحديد تاريخ البداية والنهاية من الفلتر بشكل صحيح لعرض البيانات.")
            start_date = today # Set to today to prevent further errors
            end_date = today    # Set to today to prevent further errors
        
        # Ensure start_date and end_date are always date objects
        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()
        
    with col_filter2:
        # Ensure df_complaints is not empty before attempting to get unique complaint types
        if not df_complaints.empty and 'complaint_type' in df_complaints.columns:
            complaint_types = [t['all']] + list(df_complaints['complaint_type'].unique())
        else:
            complaint_types = [t['all']] # Default if no data or column missing

        complaint_type_filter = st.selectbox(f"📂 {t['filter_by_type']}", options=complaint_types, key="manager_type_filter")

    filtered_df = df_complaints.copy()
    if not filtered_df.empty and (start_date and end_date): # Ensure dates are not None
        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date) & 
            (filtered_df["date"].dt.date <= end_date)
        ]
    
    if complaint_type_filter != t['all'] and not filtered_df.empty:
        filtered_df = filtered_df[filtered_df["complaint_type"] == complaint_type_filter]

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)
    st.subheader(f"**{t['dashboard_overview']}**")

    total_complaints = len(filtered_df)
    closed_complaints = sum(1 for c in filtered_df.to_dict('records') if c['status'] == "مغلق" or c['status'] == "تم الحل")
    in_progress_complaints = sum(1 for c in filtered_df.to_dict('records') if c['status'] == "قيد المعالجة" or c['status'] == "جاري المتابعة")

    response_times = []
    if not filtered_df.empty:
        # Filter out rows where complaint_datetime or shipping_response_datetime are NaT (Not a Time)
        valid_responses_df = filtered_df[
            pd.notna(filtered_df['shipping_response_datetime']) & 
            pd.notna(filtered_df['complaint_datetime'])
        ].copy() # Use .copy() to avoid SettingWithCopyWarning
        
        if not valid_responses_df.empty:
            durations = valid_responses_df['shipping_response_datetime'] - valid_responses_df['complaint_datetime']
            # Filter out negative durations (response before complaint)
            positive_durations = durations[durations.dt.total_seconds() >= 0]
            response_times = positive_durations.dt.total_seconds().tolist()

    avg_response_time_seconds = sum(response_times) / len(response_times) if response_times else 0
    avg_response_timedelta = timedelta(seconds=avg_response_time_seconds)

    avg_response_time_str = format_timedelta_to_string(avg_response_timedelta, t)


    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    with col_kpi1:
        st.markdown(
            f"""
            <div class="kpi-card total">
                <p class="icon">📊</p>
                <p class="title">{t['total_complaints']}</p>
                <p class="value">{total_complaints}</p>
            </div>
            """, unsafe_allow_html=True
        )

    with col_kpi2:
        st.markdown(
            f"""
            <div class="kpi-card closed">
                <p class="icon">✅</p>
                <p class="title">{t['closed_complaints']}</p>
                <p class="value">{closed_complaints}</p>
            </div>
            """, unsafe_allow_html=True
        )
    
    with col_kpi3:
        st.markdown(
            f"""
            <div class="kpi-card in-progress">
                <p class="icon">⏳</p>
                <p class="title">{t['in_progress_complaints']}</p>
                <p class="value">{in_progress_complaints}</p>
            </div>
            """, unsafe_allow_html=True
        )

    with col_kpi4:
        st.markdown(
            f"""
            <div class="kpi-card avg-time small-value">
                <p class="icon">⏱️</p>
                <p class="title">{t['avg_response_time']}</p>
                <p class="value">{avg_response_time_str}</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    # --- Detailed Table ---
    st.subheader(f"**{t['complaint_table_title']}**")
    if not filtered_df.empty:
        # Ensure all comment columns exist and then format them
        for col_name in ['cs_comments', 'shipping_comments']:
            if col_name not in filtered_df.columns:
                filtered_df[col_name] = [[] for _ in range(len(filtered_df))]

        # Format cs_comments and shipping_comments for display in dataframe
        filtered_df['cs_comments_display'] = filtered_df['cs_comments'].apply(format_comments_for_dataframe_display)
        filtered_df['shipping_comments_display'] = filtered_df['shipping_comments'].apply(format_comments_for_dataframe_display)

        # Drop original list columns before passing to data_editor
        df_for_editor = filtered_df.drop(columns=['cs_comments', 'shipping_comments']).copy()
        
        # Add 'اختر للحذف' column for the manager if not already present
        if 'اختر للحذف' not in df_for_editor.columns:
            df_for_editor['اختر للحذف'] = False


        edited_df_manager = st.data_editor( # Renamed to edited_df_manager to avoid conflict
            df_for_editor.rename(columns={
                "complaint_number": t['complaint_number'],
                "customer_name": t['customer_name'],
                "customer_phone": f"📞 {t['customer_phone']}", # Display customer phone with icon
                "employee_name": t['employee_name'],
                "complaint_type": t['complaint_type'],
                "issue_description": t['issue_description'],
                "date": t['complaint_date'],
                "time": t['complaint_time'],
                "status": t['status'],
                "cs_media_links": t['cs_media_links'],
                "shipping_response": t['shipping_response'],
                "shipping_response_employee_name": t['shipping_employee_name'],
                "shipping_response_date": t['shipping_response_date_kpi'],
                "shipping_response_time": t['shipping_response_time_kpi'],
                "shipping_media_links": t['shipping_media_links'],
                "cs_comments_display": t['cs_comments_section'], # Rename cs_comments to display formatted text
                "has_new_cs_comment": t['new_comment_from_cs'], # Rename new flag
                "shipping_comments_display": t['shipping_comments_section'], # Rename shipping comments to display formatted text
                "doc_id": "معرف المستند" # Display doc_id for manager to select for deletion
            }),
            column_config={
                "اختر للحذف": st.column_config.CheckboxColumn( # This checkbox is ONLY for manager
                    "اختر للحذف",
                    help="اختر الشكاوى التي تريد حذفها",
                    default=False,
                ),
                "معرف المستند": st.column_config.TextColumn("معرف المستند", disabled=True),
                t['cs_media_links']: st.column_config.ListColumn(t['cs_media_links'], width="medium"),
                t['shipping_media_links']: st.column_config.ListColumn(t['shipping_media_links'], width="medium"),
                t['cs_comments_section']: st.column_config.TextColumn(t['cs_comments_section'], width="large"), # Changed to TextColumn
                t['new_comment_from_cs']: st.column_config.CheckboxColumn(t['new_comment_from_cs'], disabled=True),
                t['shipping_comments_section']: st.column_config.TextColumn(t['shipping_comments_section'], width="large") # Changed to TextColumn
            },
            key="manager_complaints_table", # Unique key for manager table
            hide_index=True,
            use_container_width=True,
            
        )

        # Manager Delete Logic: Robustly check for the column before accessing
        if 'اختر للحذف' in edited_df_manager.columns:
            selected_for_deletion_docs = edited_df_manager[edited_df_manager['اختر للحذف'] == True]['معرف المستند'].tolist()

            if selected_for_deletion_docs:
                st.warning(t['confirm_delete'])
                if st.button(f"**{t['delete_complaint']}**", key="manager_delete_complaints_btn"):
                    for doc_id_to_delete in selected_for_deletion_docs:
                        delete_complaint_from_firestore(doc_id_to_delete)
                    st.session_state.complaints = load_complaints_from_firestore() # Reload after deletion
                    st.rerun()
            elif not filtered_df.empty: # Only show this message if there are complaints but none selected for deletion
                st.info("اختر شكاوى من الجدول أعلاه لحذفها.")
        else: # Fallback if 'اختر للحذف' column is unexpectedly missing
            st.info("لم يتم تفعيل خيار الحذف. يرجى التأكد من صلاحيات العرض.")


        excel_buffer = io.BytesIO()
        # Ensure to use the formatted columns for Excel download
        # Drop original list columns and the 'اختر للحذف' column
        # Make a copy to avoid SettingWithCopyWarning
        df_for_excel = edited_df_manager.copy() 
        
        # Drop columns that shouldn't be in Excel or are internal/temporary
        columns_to_drop_for_excel = [
            'اختر للحذف', # This is a UI checkbox
            'doc_id',     # Internal Firestore ID
            'cs_comments', # Original list
            'shipping_comments', # Original list
            'complaint_datetime', # Temporary for calculation
            'shipping_response_datetime' # Temporary for calculation
        ]
        # Filter out columns that might not exist to prevent errors
        columns_to_drop_for_excel = [col for col in columns_to_drop_for_excel if col in df_for_excel.columns]
        
        df_for_excel = df_for_excel.drop(columns=columns_to_drop_for_excel, errors='ignore')

        # Rename the formatted columns back to original names for cleaner Excel output
        df_for_excel = df_for_excel.rename(columns={
                "cs_comments_display": t['cs_comments_section'], # Use formatted name for Excel
                "shipping_comments_display": t['shipping_comments_section'] # Use formatted name for Excel
            })
        
        df_for_excel.to_excel(excel_buffer, index=False, engine='xlsxwriter')
        excel_buffer.seek(0)
        st.download_button(
            label=t['download_excel'],
            data=excel_buffer,
            file_name="detailed_complaints_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_detailed_complaints_excel"
        )
    else:
        st.info("لا توجد شكاوى لعرضها بناءً على الفلاتر المختارة.")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    st.markdown("### 📊 الرسوم البيانية", unsafe_allow_html=True)
    if not df_complaints.empty:
        complaint_statuses = [c['status'] for c in df_complaints.to_dict('records')]
        complaint_status_counts = pd.Series(complaint_statuses).value_counts().reset_index()
        complaint_status_counts.columns = [t['status'], 'العدد']
        st.write(f"#### **{t['complaint_status_distribution']}**")
        st.dataframe(complaint_status_counts, use_container_width=True, hide_index=True)

        excel_buffer_status = io.BytesIO()
        complaint_status_counts.to_excel(excel_buffer_status, index=False, engine='xlsxwriter')
        excel_buffer_status.seek(0)
        st.download_button(
            label=t['download_excel'],
            data=excel_buffer_status,
            file_name="complaint_status_distribution.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_status_distribution_excel"
        )

        st.bar_chart(complaint_status_counts.set_index(t['status']))
    else:
        st.info("لا توجد بيانات شكاوى لعرض التقارير.")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    st.subheader(f"**{t['user_management']}**")
    st.info("هنا سيتم إضافة وظائف إدارة المستخدمين لاحقاً.")

    st.subheader(f"**{t['admin_settings']}**")
    st.info("هنا سيتم إضافة إعدادات المسؤول لاحقاً.")

    st.markdown("<div class='section-separator'></div>", unsafe_allow_html=True)

    if st.button(f"**{t['logout']}**", key="manager_logout_btn"):
        st.session_state.logged_in = False
        st.session_state.selected_role = None
        st.session_state.current_page = "role_selection"
        st.rerun()

# --- Main page routing logic ---
if st.session_state.current_page == "role_selection":
    role_selection_page()
elif st.session_state.current_page == "login":
    login_page()
elif st.session_state.current_page == "customer_service_dashboard":
    if st.session_state.logged_in and st.session_state.selected_role == t['customer_service']:
        customer_service_dashboard()
    else:
        st.session_state.current_page = "role_selection"
        st.rerun()
elif st.session_state.current_page == "shipping_dashboard":
    if st.session_state.logged_in and st.session_state.selected_role == t['shipping_team']:
        shipping_dashboard()
    else:
        st.session_state.current_page = "role_selection"
        st.rerun()
elif st.session_state.current_page == "manager_dashboard":
    if st.session_state.logged_in and st.session_state.selected_role == t['manager']:
        manager_dashboard()
    else:
        st.session_state.current_page = "role_selection"
        st.rerun()