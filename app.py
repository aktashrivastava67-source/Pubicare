import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Pubicare | Your Personal Health Companion",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path("data")
PHOTO_DIR = DATA_DIR / "acne_photos"
DATA_DIR.mkdir(exist_ok=True)
PHOTO_DIR.mkdir(exist_ok=True)

PERIOD_FILE = DATA_DIR / "period_records.csv"
HABIT_FILE = DATA_DIR / "habit_records.csv"

# =========================================================
# STYLING
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: linear-gradient(145deg, #fffaff 0%, #ffffff 52%, #f9f6ff 100%);
        color: #20284f;
    }
    [data-testid="stHeader"] { background: rgba(255,255,255,.75); }
    .block-container { max-width: 1450px; padding-top: 1.6rem; padding-bottom: 2rem; }
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
    h1, h2, h3 { color: #20284f !important; font-family: 'Poppins', sans-serif !important; }
    p, li { color: #64708e; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff0f8 0%, #f5efff 100%);
        border-right: 1px solid #f1ddec;
    }
    [data-testid="stSidebar"] .stRadio label { font-weight: 700; color: #35365e !important; }
    .brand { display:flex; gap:12px; align-items:center; padding:8px 4px 4px; }
    .brand-icon {
        font-size:2.3rem; background:white; width:58px; height:58px; display:flex;
        align-items:center; justify-content:center; border-radius:19px;
        box-shadow:0 5px 18px #e8cce5;
    }
    .brand-title { font-family:'Poppins',sans-serif; font-size:1.08rem; font-weight:800; line-height:1.25; color:#7d3f8c; }
    .brand-subtitle { text-align:center; color:#b05b9d; font-size:.82rem; font-weight:700; padding:8px 0 15px; }
    .hero {
        display:flex; justify-content:space-between; align-items:center; gap:22px;
        padding:28px 32px; border-radius:24px; border:1px solid #f5d9eb;
        background:linear-gradient(115deg,#fff0f8 0%,#f7efff 100%);
        box-shadow:0 8px 28px rgba(193,133,182,.09); margin-bottom:24px;
    }
    .hero-copy { flex:1; min-width:0; }
    .hero h1 { font-size:clamp(1.5rem,2.5vw,2.25rem); margin:0 0 12px; line-height:1.3; }
    .hero p { font-size:1rem; margin:0 0 17px; max-width:760px; line-height:1.65; }
    .hero-art { font-size:5.5rem; min-width:100px; text-align:center; }
    .notice { padding:12px 15px; border-radius:13px; background:rgba(255,255,255,.7); border:1px solid #efc7df; color:#805274; font-size:.9rem; line-height:1.5; }
    .section-heading { font-family:'Poppins',sans-serif; font-size:1.4rem; font-weight:800; color:#20284f; margin:24px 0 16px; }
    .stat-card { min-height:118px; padding:17px; border-radius:18px; border:1px solid #e8e0f0; display:flex; gap:12px; align-items:flex-start; box-shadow:0 5px 16px rgba(68,55,100,.035); }
    .stat-pink { background:linear-gradient(135deg,#fff0f8,#fceaf5); }
    .stat-mint { background:linear-gradient(135deg,#edfff7,#eaf8f3); }
    .stat-purple { background:linear-gradient(135deg,#f3f0ff,#eeedff); }
    .stat-blue { background:linear-gradient(135deg,#eef7ff,#e9f3ff); }
    .stat-icon { width:43px;height:43px;flex-shrink:0;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.35rem; }
    .stat-label { font-size:.82rem;color:#6b6487;font-weight:800; }
    .stat-number { font-family:'Poppins',sans-serif;font-size:1.6rem;font-weight:800;color:#20284f;line-height:1.4; }
    .stat-caption { font-size:.78rem;color:#77809a; }
    .module-card { min-height:205px; padding:19px; border-radius:19px; border:1px solid #eee2f4; box-shadow:0 6px 20px rgba(60,48,90,.04); margin-bottom:8px; }
    .module-pink { background:linear-gradient(145deg,#fff3fa,#fff8fc);border-color:#f8d9eb; }
    .module-purple { background:linear-gradient(145deg,#f4f0ff,#fbf9ff);border-color:#e5ddff; }
    .module-mint { background:linear-gradient(145deg,#effff8,#f8fffc);border-color:#d5f4e7; }
    .module-blue { background:linear-gradient(145deg,#eef7ff,#f7fbff);border-color:#d7eaff; }
    .module-yellow { background:linear-gradient(145deg,#fff9eb,#fffdf7);border-color:#f9e9c5; }
    .module-icon { display:flex;align-items:center;justify-content:center;width:45px;height:45px;border-radius:50%;background:white;font-size:1.4rem;margin-bottom:11px; }
    .module-title { color:#20284f;font-family:'Poppins',sans-serif;font-weight:800;font-size:1rem;margin-bottom:7px; }
    .module-description { color:#63708f;font-size:.87rem;line-height:1.5;min-height:55px; }
    .module-link { display:inline-block;margin-top:8px;background:white;border-radius:50%;width:29px;height:29px;line-height:29px;text-align:center;color:#7e68d7;font-weight:900; }
    .encouragement { margin-top:16px;padding:15px 20px;text-align:center;border-radius:15px;background:linear-gradient(90deg,#f5eaff,#fff0f8);color:#8052aa;font-weight:800;font-style:italic; }
    div.stButton > button { border-radius:12px;border:1px solid #efcde4;background:linear-gradient(90deg,#e97cb5,#bb8be9);color:white;font-weight:800;min-height:41px; }
    div.stButton > button:hover { border-color:#d98ec2;color:white;box-shadow:0 5px 14px #e9d0e9; }
    div[data-testid="stMetric"] { background:white;padding:13px 15px;border:1px solid #f0e3f0;border-radius:16px; }
    div[data-testid="stForm"] { background:rgba(255,255,255,.78);border:1px solid #f0e0f0;border-radius:18px;padding:20px; }
    [data-testid="stFileUploader"] { background:white;border:1px dashed #d7b9e7;border-radius:16px;padding:12px; }
    .footer { color:#a08ba9;text-align:center;font-size:.82rem;padding:22px 0 4px; }
    @media (max-width:750px) { .hero{padding:20px}.hero-art{display:none}.block-container{padding-left:1rem;padding-right:1rem} }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HELPERS
# =========================================================
def load_csv(path, columns):
    if path.exists():
        try:
            df = pd.read_csv(path)
            for col in columns:
                if col not in df.columns:
                    df[col] = ""
            return df[columns]
        except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
            pass
    return pd.DataFrame(columns=columns)


def save_csv(df, path):
    df.to_csv(path, index=False)


def period_data():
    return load_csv(PERIOD_FILE, ["start_date", "notes"])


def habit_data():
    return load_csv(HABIT_FILE, ["record_date", "sleep", "water", "meals", "activity"])


def saved_photo_count():
    return len(list(PHOTO_DIR.glob("*.jpg"))) + len(list(PHOTO_DIR.glob("*.png")))


# =========================================================
# PROFILE SETUP: NAME + AGE
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-icon">🌸</div>
          <div class="brand-title">Pubicare</div>
        </div>
        <div class="brand-subtitle">Learn ✧ Track ✧ Stay Healthy</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### 👤 Your profile")
    profile_name = st.text_input(
        "Name or nickname",
        value=st.session_state.get("profile_name", ""),
        placeholder="e.g. Alex",
        max_chars=40,
    )
    profile_age = st.number_input(
        "Age (years)",
        min_value=5,
        max_value=100,
        value=int(st.session_state.get("profile_age", 18)),
        step=1,
    )
    if st.button("Save profile", use_container_width=True):
        st.session_state["profile_name"] = profile_name.strip()
        st.session_state["profile_age"] = int(profile_age)
        st.success("Profile saved for this session.")
    st.caption("Use a nickname if you prefer. Profile details are not saved to the CSV records.")

    page = st.radio(
        "Explore Your Health",
        [
            "Home",
            "Puberty Education",
            "Hormones & Symptoms",
            "BMI Calculator",
            "Period Tracker",
            "Acne Photo Journal",
            "Healthy Habits",
            "Doctor Guidance",
            "My Records",
        ],
        key="page",
    )
    st.markdown(
        """
        <div style="margin-top:28px;padding:20px 14px;border-radius:18px;
        background:linear-gradient(135deg,#ffe8f4,#f3eaff);text-align:center;">
          <div style="font-size:1.6rem;">💗</div>
          <div style="font-weight:800;color:#8b6198;">Your health matters.</div>
          <div style="color:#9b7aa5;font-size:.88rem;">Small steps count.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

display_name = st.session_state.get("profile_name", "").strip()
age = int(st.session_state.get("profile_age", profile_age))
greeting = f", {display_name}" if display_name else ""

def navigate_to(destination):
    """Change the sidebar page selection before Streamlit reruns the app."""
    st.session_state["page"] = destination


# =========================================================
# HOME
# =========================================================
if page == "Home":
    periods = period_data()
    habits = habit_data()
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-copy">
            <h1>Welcome{greeting} to Pubicare 💗</h1>
            <p>Your educational space for puberty, menstrual health, skincare and healthy habits.</p>
            <div class="notice">ⓘ &nbsp; <b>Educational use only.</b> This application does not diagnose medical conditions.</div>
          </div>
          <div class="hero-art">🌸</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(4)
    stats = [
        ("📅", "Period Records", len(periods), "Total entries", "stat-pink"),
        ("🌿", "Habit Check-ins", len(habits), "Total entries", "stat-mint"),
        ("📷", "Acne Photos", saved_photo_count(), "Saved photos", "stat-purple"),
        ("💗", "Your Age", age, "Years old", "stat-blue"),
    ]
    for col, item in zip(cols, stats):
        icon, label, number, caption, css = item
        with col:
            st.markdown(
                f'<div class="stat-card {css}"><div class="stat-icon">{icon}</div><div>'
                f'<div class="stat-label">{label}</div><div class="stat-number">{number}</div>'
                f'<div class="stat-caption">{caption}</div></div></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-heading">🌸 &nbsp; Explore Your Modules</div>', unsafe_allow_html=True)
    modules = [
        ("📖", "Puberty Education", "Understand physical and emotional changes.", "module-pink", "Puberty Education"),
        ("🧬", "Hormones & Symptoms", "Learn hormone basics and symptoms to discuss with a clinician.", "module-purple", "Hormones & Symptoms"),
        ("🧮", "BMI Calculator", "Calculate BMI with age-appropriate interpretation.", "module-mint", "BMI Calculator"),
        ("🗓️", "Period Tracker", "Record period dates and estimate the next start date.", "module-blue", "Period Tracker"),
        ("📷", "Acne Photo Journal", "Upload a photo and keep skincare notes.", "module-blue", "Acne Photo Journal"),
        ("🌿", "Healthy Habits", "Record rest, water, meals and enjoyable activity.", "module-yellow", "Healthy Habits"),
        ("🩺", "Doctor Guidance", "Learn when to seek professional advice.", "module-pink", "Doctor Guidance"),
        ("📁", "My Records", "Review your saved period and habit records.", "module-mint", "My Records"),
    ]
    for i in range(0, len(modules), 4):
        row = st.columns(4)
        for col, item in zip(row, modules[i:i+4]):
            icon, title, desc, css, destination = item
            with col:
                st.markdown(
                    f'<div class="module-card {css}"><div class="module-icon">{icon}</div>'
                    f'<div class="module-title">{title}</div><div class="module-description">{desc}</div>'
                    f'<div class="module-link">→</div></div>',
                    unsafe_allow_html=True,
                )
                st.button(
                    "Open module →",
                    key=f"nav_{destination}",
                    use_container_width=True,
                    on_click=navigate_to,
                    args=(destination,),
                )
    st.markdown('<div class="encouragement">✧ Small steps towards better health make a big difference 💕</div>', unsafe_allow_html=True)

# =========================================================
# PUBERTY EDUCATION
# =========================================================
elif page == "Puberty Education":
    st.title("📚 Puberty Education")
    st.write("Bodies develop at different rates. These are common changes, not a checklist everyone must follow.")
    with st.expander("🌱 Physical changes", expanded=True):
        st.write("Growth, body hair, sweat and skin changes, body development and menstruation may occur during puberty.")
    with st.expander("💗 Emotional wellbeing"):
        st.write("Hormones, sleep, stress and life changes can affect feelings. Talk to a trusted adult or clinician if mood changes persist or interfere with daily life.")
    with st.expander("🩸 Menstrual health"):
        st.write("Cycle length can vary, particularly in the first years after periods begin. A tracker records patterns but cannot guarantee the next date.")
    with st.expander("✨ Body image"):
        st.write("There is no single correct body shape during puberty. Avoid trying to change your body based on one number or comparison.")

# =========================================================
# HORMONES & SYMPTOMS
# =========================================================
elif page == "Hormones & Symptoms":
    st.title("🧬 Hormonal Knowledge")
    st.write("Hormones are chemical messengers. They help coordinate growth, puberty, the menstrual cycle, sleep, mood and many other body functions.")
    with st.expander("Estrogen and progesterone", expanded=True):
        st.write("These hormones are involved in menstrual-cycle changes and reproductive development. Their levels naturally change during the cycle.")
    with st.expander("Androgens"):
        st.write("Androgens are present in people of all sexes. They contribute to puberty-related changes and can influence oil production in the skin.")
    with st.expander("Insulin and thyroid hormones"):
        st.write("Insulin helps regulate blood glucose. Thyroid hormones influence energy use and many body processes. Symptoms alone cannot confirm a hormone problem.")
    st.subheader("Symptoms worth discussing with a clinician")
    st.markdown(
        "- Periods that repeatedly stop for several months after previously occurring, or major changes that worry you.\n"
        "- Very heavy bleeding, prolonged bleeding, or pain that disrupts everyday activities.\n"
        "- Persistent acne accompanied by other changes such as unexpectedly rapid hair growth or other concerning symptoms.\n"
        "- Unexplained, persistent fatigue, feeling unusually hot or cold, or significant changes in wellbeing.\n"
        "- Any symptom that is persistent, worsening, or worrying to you."
    )
    st.info("These symptoms can have many causes and do not automatically mean a hormone disorder. A healthcare professional can decide whether an assessment or tests are appropriate.")

# =========================================================
# BMI CALCULATOR
# =========================================================
elif page == "BMI Calculator":
    st.title("🧮 BMI Calculator")
    st.write("BMI is calculated from weight and height. It is a screening measure, not a diagnosis.")
    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=50.0, step=0.5)
    with c2:
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=160.0, step=0.5)

    if st.button("Calculate BMI", use_container_width=True):
        bmi = weight / ((height / 100) ** 2)
        st.session_state["last_bmi"] = round(bmi, 1)
        st.session_state["last_bmi_age"] = age

    if "last_bmi" in st.session_state:
        bmi = st.session_state["last_bmi"]
        st.metric("Calculated BMI", bmi)
        bmi_age = st.session_state.get("last_bmi_age", age)
        if bmi_age < 20:
            st.info(
                "Because the profile age is under 20, adult BMI cut-offs should not be used. "
                "For children and teens, a clinician interprets BMI using age- and sex-specific growth charts. "
                "This app cannot determine whether weight should increase or decrease."
            )
        else:
            st.info(
                "For adults aged 20 and above, common screening categories are: below 18.5 (underweight), "
                "18.5–24.9 (usual reference range), 25.0–29.9 (overweight range), and 30+ (obesity range). "
                "These are screening categories, not a diagnosis and not a direct instruction to change weight."
            )
            if bmi < 18.5:
                st.warning("This BMI falls below the common adult reference range. Consider discussing your health and nutrition with a healthcare professional rather than trying to change weight on your own.")
            elif bmi < 25:
                st.success("This BMI falls within the common adult reference range. BMI alone cannot tell the full picture of health.")
            elif bmi < 30:
                st.warning("This BMI falls in the common adult overweight screening range. It does not by itself establish a health problem or mean you must lose weight.")
            else:
                st.warning("This BMI falls in a higher adult screening category. Consider discussing overall health with a healthcare professional; BMI alone is not a diagnosis.")
    st.caption("This tool does not recommend gaining or losing fat. A clinician can consider growth, medical history, development and other factors.")

# =========================================================
# PERIOD TRACKER
# =========================================================
elif page == "Period Tracker":
    st.title("🗓️ Period Tracker")
    st.write("Enter the first day bleeding started. The app estimates a future date from your recorded cycle history.")
    with st.form("period_form", clear_on_submit=True):
        period_date = st.date_input("First day of period", value=date.today(), max_value=date.today())
        notes = st.text_input("Optional note (avoid identifying details)")
        save_period = st.form_submit_button("Save period record", use_container_width=True)

    if save_period:
        df = period_data()
        if str(period_date) in df["start_date"].astype(str).values:
            st.warning("That date is already recorded.")
        else:
            df = pd.concat([df, pd.DataFrame([{"start_date": str(period_date), "notes": notes}])], ignore_index=True)
            save_csv(df.sort_values("start_date"), PERIOD_FILE)
            st.success("Period record saved.")

    df = period_data()
    if not df.empty:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
        df = df.dropna(subset=["start_date"]).sort_values("start_date")
        display = df.copy()
        display["start_date"] = display["start_date"].dt.strftime("%d %b %Y")
        st.subheader("Period history")
        st.dataframe(display, use_container_width=True, hide_index=True)
        starts = sorted(set(ts.date() for ts in df["start_date"]))
        if len(starts) >= 2:
            intervals = [(starts[i] - starts[i-1]).days for i in range(1, len(starts))]
            valid = [n for n in intervals[-6:] if 15 <= n <= 60]
            if valid:
                avg_cycle = round(sum(valid) / len(valid))
                predicted = starts[-1] + timedelta(days=avg_cycle)
                st.metric("Estimated average cycle length", f"{avg_cycle} days")
                st.metric("Estimated next period start", predicted.strftime("%d %b %Y"))
                low = starts[-1] + timedelta(days=max(1, avg_cycle - 3))
                high = starts[-1] + timedelta(days=avg_cycle + 3)
                st.write(f"Approximate window: **{low.strftime('%d %b')} – {high.strftime('%d %b %Y')}**")
                st.caption("This is a calendar estimate based on up to six recent intervals, not a guarantee. It can be less accurate for irregular cycles, recent first periods, stress, illness or hormonal changes.")
            else:
                st.info("The recorded intervals do not provide a usable estimate yet.")
        else:
            st.info("Record at least two different period start dates to estimate your average cycle.")
    st.warning("Talk to a healthcare professional about very heavy bleeding, severe pain, or changes that concern you.")

# =========================================================
# ACNE PHOTO JOURNAL + RECOMMENDATIONS
# =========================================================
elif page == "Acne Photo Journal":
    st.title("📷 Acne Photo Journal & Skincare")
    st.write("Upload a photo to keep a local journal. This starter version does not classify acne with AI.")
    uploaded = st.file_uploader("Upload a JPG or PNG skin photo", type=["jpg", "jpeg", "png"])
    if uploaded:
        try:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Uploaded photo", use_container_width=True)
            note = st.text_area("Optional skincare notes")
            if st.button("Save photo and notes", use_container_width=True):
                filename = f"skin_{date.today().isoformat()}_{len(list(PHOTO_DIR.glob('*.jpg'))) + 1}.jpg"
                image.save(PHOTO_DIR / filename, "JPEG", quality=90)
                (PHOTO_DIR / f"{Path(filename).stem}.json").write_text(
                    json.dumps({"date": str(date.today()), "note": note}, indent=2), encoding="utf-8"
                )
                st.success("Photo journal entry saved locally.")
        except Exception:
            st.error("Could not open the image. Please try a JPG or PNG.")

    st.subheader("Gentle skincare recommendations")
    st.markdown(
        "**Simple routine**\n"
        "- Wash gently with a mild cleanser; avoid scrubbing.\n"
        "- Use a non-comedogenic moisturiser if your skin feels dry.\n"
        "- Use broad-spectrum SPF 30+ sunscreen during the day if available and suitable for you.\n"
        "- Avoid picking or squeezing spots.\n"
        "- Introduce one new product at a time and stop if it causes a significant reaction."
    )
    st.markdown(
        "**When to ask for help**\n"
        "- Painful deep spots, scarring, or acne that is worsening.\n"
        "- Acne that affects confidence or wellbeing.\n"
        "- A rash, swelling or severe irritation after a product."
    )
    st.info("A pharmacist or clinician can help select suitable acne treatment. This app does not diagnose skin conditions or prescribe medication.")
    st.caption("Photos are sensitive health information. Do not upload intimate images or anyone else's photo without permission.")

# =========================================================
# HEALTHY HABITS
# =========================================================
elif page == "Healthy Habits":
    st.title("🌿 Healthy Habits")
    st.write("Use this as a gentle reflection tool, not a score of your health or worth.")
    with st.form("habit_form", clear_on_submit=True):
        record_date = st.date_input("Date", value=date.today(), max_value=date.today())
        sleep = st.checkbox("I gave myself enough rest")
        water = st.checkbox("I drank water regularly")
        meals = st.checkbox("I ate regular, varied meals")
        activity = st.checkbox("I included enjoyable movement or breaks")
        submit = st.form_submit_button("Save check-in", use_container_width=True)
    if submit:
        df = habit_data()
        row = {"record_date": str(record_date), "sleep": sleep, "water": water, "meals": meals, "activity": activity}
        save_csv(pd.concat([df, pd.DataFrame([row])], ignore_index=True), HABIT_FILE)
        st.success("Check-in saved.")
    df = habit_data()
    if not df.empty:
        st.subheader("Recent check-ins")
        st.dataframe(df.tail(14), use_container_width=True, hide_index=True)

# =========================================================
# DOCTOR GUIDANCE
# =========================================================
elif page == "Doctor Guidance":
    st.title("🩺 When to Consult a Doctor")
    st.write("Consider professional advice for symptoms that are persistent, severe, worsening or worrying.")
    st.markdown(
        "- Period pain that repeatedly interrupts school, work or everyday activities.\n"
        "- Very heavy or prolonged bleeding, or periods that stop for several months after previously occurring.\n"
        "- Persistent acne that is painful, scarring or distressing.\n"
        "- Ongoing fatigue, feeling unusually hot or cold, or other persistent changes in wellbeing.\n"
        "- Unusual discharge with pain, fever or a strong unpleasant smell.\n"
        "- Any sudden or severe symptom."
    )
    st.warning("Seek urgent medical care for severe or sudden symptoms. These signs can have multiple causes and do not automatically mean a hormone disorder.")

# =========================================================
# MY RECORDS
# =========================================================
elif page == "My Records":
    st.title("📁 My Records")
    st.caption("Saved records are kept locally in this project folder.")
    st.subheader("Period records")
    st.dataframe(period_data(), use_container_width=True, hide_index=True)
    st.subheader("Habit records")
    st.dataframe(habit_data(), use_container_width=True, hide_index=True)
    photos = list(PHOTO_DIR.glob("*.jpg")) + list(PHOTO_DIR.glob("*.png"))
    st.subheader("Saved acne photos")
    st.write(f"{len(photos)} photo(s) saved locally.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Delete all period records"):
            save_csv(pd.DataFrame(columns=["start_date", "notes"]), PERIOD_FILE)
            st.success("Period records deleted.")
            st.rerun()
    with c2:
        if st.button("Delete all habit records"):
            save_csv(pd.DataFrame(columns=["record_date", "sleep", "water", "meals", "activity"]), HABIT_FILE)
            st.success("Habit records deleted.")
            st.rerun()
    st.warning("Keep the data folder private and excluded from GitHub. This is not a secure medical-record system.")

st.markdown(
    '<div class="footer">🌸 Pubicare · Educational use only · Not a substitute for professional care</div>',
    unsafe_allow_html=True,
)
