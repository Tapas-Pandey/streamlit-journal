import streamlit as st
from datetime import datetime
import random
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit_authenticator as stauth
import os
import hashlib

import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def init_firestore():
    firebase_config = dict(st.secrets["firebase"])  # convert from Config to dict
    cred = credentials.Certificate(firebase_config)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firestore()


db = init_firestore()

class FirebaseAuthenticator:
    def __init__(self, db):
        self.db = db

    def check_user_exists(self, username):
        user_ref = self.db.collection("users").document(username)
        return user_ref.get().exists

    def add_user(self, username, name, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Store hashed password
        self.db.collection("users").document(username).set({
            "name": name,
            "password": hashed_password
        })

    def authenticate(self, username, password):
        user_ref = self.db.collection("users").document(username)
        user = user_ref.get()

        if user.exists:
            user_data = user.to_dict()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user_data["password"] == hashed_password:
                return True
        return False

authenticator = FirebaseAuthenticator(db)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:
    tab = st.sidebar.radio("🔑 Choose Option", ["Login", "Register"])

    if tab == "Register":
        st.title("📝 Register")
        username = st.text_input("Username")
        name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if password != confirm_password:
                st.error("Passwords do not match!")
            elif username and name and password:
                if authenticator.check_user_exists(username):
                    st.error("User already exists!")
                else:
                    authenticator.add_user(username, name, password)
                    st.success("✅ Registration successful! Please log in from the Login tab.")
            else:
                st.error("Please fill all fields!")

    elif tab == "Login":
        st.markdown("### 🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                if authenticator.authenticate(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.name = username
                    st.success(f"Welcome {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
            else:
                st.error("Please enter both username and password.")
else:
    
    st.sidebar.title(f"Welcome, {st.session_state.name} 👋")
    st.sidebar.markdown("---")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    st.title("📓 Daily Journal")
    today = datetime.now().strftime("%Y-%m-%d")

    
    st.markdown("### ✍️ New Entry")
    title = st.text_input("📌 Title")
    entry = st.text_area("📝 Your thoughts", height=200)

    if st.button("💾 Save Entry"):
        if title and entry:
            db.collection("journal").add({
                "user": st.session_state.username,
                "title": title,
                "entry": entry,
                "date": today,
                "timestamp": datetime.now().isoformat()
            })
            st.success("✅ Journal entry saved!")
        else:
            st.warning("Please enter both a title and entry.")

    
    st.markdown("---")
    st.markdown("### 🔍 Search Entries")
    search_query = st.text_input("Search by title, date, or content").lower().strip()

    
    st.markdown("### 📖 Your Entries")

    docs = db.collection("journal") \
            .where("user", "==", st.session_state.username) \
            .order_by("timestamp", direction=firestore.Query.DESCENDING) \
            .stream()

    found = 0
    for doc in docs:
        doc_id = doc.id
        data = doc.to_dict()
        date = data.get("date", "Unknown Date")
        title = data.get("title", "Untitled")
        entry = data.get("entry", "")

        if search_query:
            if (search_query not in title.lower() and
                search_query not in date.lower() and
                search_query not in entry.lower()):
                continue

        found += 1

        with st.expander(f"🗓️ {date} — {title}"):
            st.markdown(entry)

            col1, col2 = st.columns([1, 1])

            # --- Edit Entry ---
            with col1:
                if st.button("✏️ Edit", key=f"edit_{doc_id}"):
                    st.session_state[f"edit_mode_{doc_id}"] = True

                if st.session_state.get(f"edit_mode_{doc_id}", False):
                    with st.form(f"edit_form_{doc_id}"):
                        new_title = st.text_input("Edit Title", value=title)
                        new_entry = st.text_area("Edit Entry", value=entry)
                        submitted = st.form_submit_button("Save Changes")
                        if submitted:
                            db.collection("journal").document(doc_id).update({
                                "title": new_title,
                                "entry": new_entry,
                                "timestamp": datetime.now().isoformat()
                            })
                            st.success("✅ Entry updated.")
                            st.session_state[f"edit_mode_{doc_id}"] = False
                            st.rerun()

            with col2:
                if st.button("🗑️ Delete", key=f"delete_{doc_id}"):
                    db.collection("journal").document(doc_id).delete()
                    st.warning("🗑️ Entry deleted.")
                    st.rerun()

    if search_query and found == 0:
        st.warning("🔎 No entries found matching your search.")
