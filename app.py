import streamlit as st
from datetime import datetime
import uuid
import os

st.set_page_config(page_title="FixSync", layout="wide")

# Fake DB (in production use Firebase/Supabase)
if "jobs" not in st.session_state:
    st.session_state.jobs = {}

# ---------- HOME ----------
if "job_id" not in st.query_params:
    st.title("🔧 FixSync – Universal Service Portal")
    st.markdown("Customers upload photos → techs collaborate live → quotes in seconds")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 I'm a Customer – Start New Job", use_container_width=True):
            job_id = str(uuid.uuid4())[:8]
            st.query_params["job_id"] = job_id
            st.session_state.jobs[job_id] = {
                "created": datetime.now().isoformat(),
                "photos": [],
                "messages": [],
                "quote": "",
                "status": "open"
            }
            st.rerun()
    with col2:
        job_id = st.text_input("Already have a job ID?")
        if st.button("Join Existing Job"):
            if job_id in st.session_state.jobs:
                st.query_params["job_id"] = job_id
                st.rerun()
            else:
                st.error("Job not found")

else:
    # ---------- INSIDE JOB ROOM ----------
    job_id = st.query_params["job_id"]
    job = st.session_state.jobs[job_id]

    st.title(f"Job #{job_id[:8]}")
    role = st.radio("You are:", ["Customer", "Technician"], horizontal=True, key="role")

    # Upload photos (customer or tech)
    uploaded = st.file_uploader("Drag photos of the problem here", accept_multiple_files=True, type=["png","jpg","jpeg"])
    if uploaded:
        for file in uploaded:
            job["photos"].append(file.getvalue())
        st.success(f"{len(uploaded)} photo(s) added!")

    # Show photos
    if job["photos"]:
        cols = st.columns(4)
        for i, img_bytes in enumerate(job["photos"][-8:]):  # last 8
            cols[i%4].image(img_bytes, use_column_width=True)

    # Real-time chat + quote
    st.subheader("Live Collaboration")
    chat = st.chat_input("Type message or quote...")

    if chat:
        msg = {
            "role": role,
            "text": chat,
            "time": datetime.now().strftime("%I:%M %p")
        }
        job["messages"].append(msg)

    # Display messages
    for m in job["messages"]:
        with st.chat_message(m["role"].lower()):
            st.write(f"**{m['role']}** – {m['time']}")
            st.write(m["text"])

    # Quote box
    if role == "Technician":
        quote = st.text_input("Final Quote", placeholder="e.g. $485 – replace water heater + labor")
        if st.button("Send Official Quote"):
            job["quote"] = quote
            st.success("Quote locked and sent!")

    if job.get("quote"):
        st.success(f"OFFICIAL QUOTE: {job['quote']}")

    st.caption(f"Share this link → {st.experimental_get_query_params()['job_id'][0]}")
