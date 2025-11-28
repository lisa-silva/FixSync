import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(page_title="FixSync", layout="wide")

if "jobs" not in st.session_state:
    st.session_state.jobs = {}

# ---------- HOME ----------
if "job_id" not in st.query_params:
    st.title("🔧 FixSync – Universal Service Portal")
    st.markdown("**Photos + Videos** → live tech collab → instant quotes")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("👤 Customer – Start New Job", use_container_width=True):
            job_id = str(uuid.uuid4())[:8]
            st.query_params["job_id"] = job_id
            st.session_state.jobs[job_id] = {
                "created": datetime.now().isoformat(),
                "media": [],        # unified list for photos + videos
                "messages": [],
                "quote": "",
                "status": "open"
            }
            st.rerun()
    with c2:
        job_id = st.text_input("Have a Job ID?")
        if st.button("Join Job"):
            if job_id in st.session_state.jobs:
                st.query_params["job_id"] = job_id
                st.rerun()
            else:
                st.error("Not found")

else:
    job_id = st.query_params["job_id"]
    job = st.session_state.jobs[job_id]

    st.title(f"Job #{job_id}")
    role = st.radio("You are:", ["Customer", "Technician"], horizontal=True)

    # ---------- MEDIA UPLOAD (PHOTO + VIDEO) ----------
    uploaded_files = st.file_uploader(
        "Drag photos or videos of the problem here",
        accept_multiple_files=True,
        type=["png","jpg","jpeg","mp4","mov","avi","webm"]
    )

    if uploaded_files:
        for f in uploaded_files:
            job["media"].append({
                "name": f.name,
                "bytes": f.read(),
                "type": f.type
            })
        st.success(f"{len(uploaded_files)} file(s) added!")

    # ---------- DISPLAY MEDIA ----------
    if job["media"]:
        st.subheader("Problem Media")
        cols = st.columns(4)
        for i, item in enumerate(job["media"][-12:]):  # last 12 items
            with cols[i % 4]:
                if item["type"].startswith("image"):
                    st.image(item
