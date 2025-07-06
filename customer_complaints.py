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
#     cred = credentials.Certificate(SERVICE_Account_KEY_PATH)
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
        "shipping_response_time_input": "وقت الرد من الشحن" # New translation for input field
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

# --- Firebase functions for data handling ---

def load_complaints_from_firestore():
    """
    Loads complaints from Firestore.
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
                st.success(t['response_saved'])
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


# Load data when the app starts
# This will be called once per session or when the script reruns
st.session_state.complaints = load_complaints_from_firestore()


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
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
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


    /* Specific colors for KPI cards */
    .kpi-card.total .icon { color: #3B82F6; } /* Blue */
    .kpi-card.total .value { color: #1D4ED8; }

    .kpi-card.closed .icon { color: #10B981; } /* Green */
    .kpi-card.closed .value { color: #047857; }

    .kpi-card.in-progress .icon { color: #F59E0B; } /* Orange */
    .kpi-card.in-progress .value { color: #B45309; }

    .kpi-card.avg-time .icon { color: #8B5CF6; } /* Purple */
    .kpi-card.avg-time .value { color: #6D28D9; }

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
                # Display shipping media links
                if found_complaint.get('shipping_media_links'):
                    st.markdown(f"**{t['shipping_media_links']}:**")
                    display_media_from_links(found_complaint['shipping_media_links'])
            else:
                st.info(t['no_shipping_response'])
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
                    "shipping_response_employee_name": ""
                }
                # --- Call Firestore function to add complaint ---
                add_complaint_to_firestore(new_complaint_data)
                # --- Reload data from Firestore ---
                st.session_state.complaints = load_complaints_from_firestore()
                st.rerun()
            else:
                st.warning("الرجاء ملء جميع الحقول المطلوبة (رقم الشكوى، اسم العميل، هاتف العميل، تفاصيل الشكوى، اسم الموظف، نوع الشكوى).")

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
        for col in ['shipping_response_date', 'shipping_response_time', 'shipping_media_links', 'shipping_response_employee_name']:
            if col in display_df.columns:
                display_df = display_df.drop(columns=[col])

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
            "shipping_response": t['shipping_response']
        }), use_container_width=True, hide_index=True)
    else:
        st.info(t['no_complaints'])

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
    new_and_in_progress_complaints = [c for c in all_complaints if c['status'] in ["جديد", "قيد المعالجة", "جاري المتابعة"]]
    resolved_and_closed_complaints = [c for c in all_complaints if c['status'] in ["تم الحل", "مغلق"]]

    # --- Split page into two columns ---
    col_new_complaints, col_old_complaints = st.columns([0.6, 0.4])

    with col_new_complaints:
        # --- New and In-Progress Complaints Section ---
        st.subheader(f"**{t['current_complaints']}** (الشكاوى الجديدة وقيد المعالجة)")
        if new_and_in_progress_complaints:
            for complaint in new_and_in_progress_complaints:
                doc_id = complaint.get('doc_id')
                if not doc_id:
                    st.warning(f"Complaint without document ID (doc_id): {complaint.get('complaint_number', 'Unknown')}. It will not be updated in Firestore.")
                    continue

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
                    
                    # Display previous shipping media links
                    if complaint.get('shipping_media_links'):
                        st.markdown(f"**{t['shipping_media_links']}:** (المرفقات السابقة)")
                        display_media_from_links(complaint['shipping_media_links'])

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
        else:
            st.info("لا توجد شكاوى جديدة أو قيد المعالجة حالياً.")

    with col_old_complaints:
        # --- Old Complaints Section (with search and delete option) ---
        st.subheader(f"**{t['old_complaints']}** (الشكاوى التي تم حلها أو إغلاقها)")

        search_old_complaint_number = st.text_input(f"**{t['search_old_complaints']}**", placeholder=t['complaint_number'], key="shipping_old_search_number")
        
        old_complaint_types = [t['all']] + list(set(c['complaint_type'] for c in resolved_and_closed_complaints)) if resolved_and_closed_complaints else [t['all']]
        filter_old_complaint_type = st.selectbox(f"**{t['filter_by_complaint_type']}**", options=old_complaint_types, key="shipping_old_filter_type")

        filtered_old_complaints = resolved_and_closed_complaints
        if search_old_complaint_number:
            filtered_old_complaints = [c for c in filtered_old_complaints if c['complaint_number'] == search_old_complaint_number]
        
        if filter_old_complaint_type != t['all']:
            filtered_old_complaints = [c for c in filtered_old_complaints if c['complaint_type'] == filter_old_complaint_type]


        if filtered_old_complaints:
            df_old_complaints_display = pd.DataFrame(filtered_old_complaints).sort_values(by=['date', 'time'], ascending=[False, False])
            
            df_old_complaints_display['اختر للحذف'] = False
            
            edited_df = st.data_editor(
                df_old_complaints_display.rename(columns={
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
                    "doc_id": "معرف المستند"
                }),
                column_config={
                    "اختر للحذف": st.column_config.CheckboxColumn(
                        "اختر للحذف",
                        help="اختر الشكاوى التي تريد حذفها",
                        default=False,
                    ),
                    "معرف المستند": st.column_config.TextColumn("معرف المستند", disabled=True),
                    t['shipping_response_date_kpi']: st.column_config.TextColumn(t['shipping_response_date_kpi'], disabled=True),
                    t['shipping_response_time_kpi']: st.column_config.TextColumn(t['shipping_response_time_kpi'], disabled=True),
                    t['cs_media_links']: st.column_config.ListColumn(t['cs_media_links'], width="medium"), # Display as list
                    t['shipping_media_links']: st.column_config.ListColumn(t['shipping_media_links'], width="medium") # Display as list
                },
                hide_index=True,
                use_container_width=True,
                key="old_complaints_editor"
            )

            if not edited_df.empty:
                df_to_download = edited_df.drop(columns=['اختر للحذف', 'معرف المستند'], errors='ignore')
                
                excel_buffer = io.BytesIO()
                df_to_download.to_excel(excel_buffer, index=False, engine='xlsxwriter')
                excel_buffer.seek(0)
                st.download_button(
                    label=t['download_excel'],
                    data=excel_buffer,
                    file_name="old_complaints.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_old_complaints_excel"
                )

            selected_for_deletion_docs = edited_df[edited_df['اختر للحذف'] == True]['معرف المستند'].tolist()

            if selected_for_deletion_docs:
                st.warning(t['confirm_delete'])
                if st.button(f"**{t['delete_complaint']}**", key="delete_old_complaints_btn"):
                    for doc_id_to_delete in selected_for_deletion_docs:
                        # --- Call Firestore function to delete complaint ---
                        delete_complaint_from_firestore(doc_id_to_delete)
                    # --- Reload data from Firestore after all deletions ---
                    st.session_state.complaints = load_complaints_from_firestore()
                    st.rerun()
            else:
                st.info("اختر شكاوى من الجدول أعلاه لحذفها.")
        else:
            st.info(t['no_old_complaints'])

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
            end_date = today   # Set to today to prevent further errors
        
        # Ensure start_date and end_date are always date objects
        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()
        
    with col_filter2:
        complaint_types = [t['all']] + list(df_complaints['complaint_type'].unique()) if not df_complaints.empty else [t['all']]
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
        display_cols = [
            "complaint_number", "customer_name", "customer_phone", "employee_name", # Added customer_phone
            "complaint_type", "issue_description", "date", "time", "status", 
            "cs_media_links", # Add Customer Service links
            "shipping_response", "shipping_response_employee_name",
            "shipping_response_date", "shipping_response_time", # Add shipping response date/time
            "shipping_media_links" # Add Shipping links
        ]
        
        existing_display_cols = [col for col in display_cols if col in filtered_df.columns]
        
        df_to_display = filtered_df[existing_display_cols].copy()
        
        st.dataframe(
            df_to_display.rename(columns={
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
                "shipping_media_links": t['shipping_media_links']
            }),
            column_config={
                t['cs_media_links']: st.column_config.ListColumn(t['cs_media_links'], width="medium"),
                t['shipping_media_links']: st.column_config.ListColumn(t['shipping_media_links'], width="medium")
            },
            use_container_width=True,
            hide_index=True
        )

        excel_buffer = io.BytesIO()
        df_to_display.to_excel(excel_buffer, index=False, engine='xlsxwriter')
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
