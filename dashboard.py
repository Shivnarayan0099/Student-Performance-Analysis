
import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("Student Performance Analysis Dashboard")
st.write("Analyze student marks, attendance and study habits.")

uri = "mongodb+srv://shiv******8_db_user:*******@cluster0.oyu5ybe.mongodb.net/"

@st.cache_data(ttl=60)
def load_data():
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    try:
        client.admin.command("ping")
        db = client["StudentPerformanceDB"]
        collection = db["students"]
        data = list(collection.find({}, {"_id": 0}))
        return pd.DataFrame(data)
    finally:
        client.close()

try:
    df = load_data()

    if df.empty:
        st.warning("No student records found in MongoDB.")
        st.stop()

    df["Exam_Score"] = pd.to_numeric(
        df["Exam_Score"], errors="coerce"
    )
    df["Attendance"] = pd.to_numeric(
        df["Attendance"], errors="coerce"
    )
    df["Hours_Studied"] = pd.to_numeric(
        df["Hours_Studied"], errors="coerce"
    )

    total_students = len(df)
    average_score = df["Exam_Score"].mean()
    highest_score = df["Exam_Score"].max()
    average_attendance = df["Attendance"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", f"{total_students:,}")
    col2.metric("Average Exam Score", f"{average_score:.2f}")
    col3.metric("Highest Exam Score", f"{highest_score:.0f}")
    col4.metric("Average Attendance", f"{average_attendance:.1f}%")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Study Hours vs Exam Score")
        fig1 = px.scatter(
            df,
            x="Hours_Studied",
            y="Exam_Score",
            title="Study Hours and Marks"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with right:
        st.subheader("Attendance vs Exam Score")
        fig2 = px.scatter(
            df,
            x="Attendance",
            y="Exam_Score",
            title="Attendance and Marks"
        )
        st.plotly_chart(fig2, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.subheader("Exam Score Distribution")
        fig3 = px.histogram(
            df,
            x="Exam_Score",
            nbins=20,
            title="Distribution of Exam Scores"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with right:
        st.subheader("Average Score by Gender")
        gender_data = df.groupby("Gender", as_index=False)[
            "Exam_Score"
        ].mean()

        fig4 = px.bar(
            gender_data,
            x="Gender",
            y="Exam_Score",
            title="Gender-wise Average Exam Score"
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Student Records")
    st.dataframe(df.head(100), use_container_width=True)

except Exception as e:
    st.error(f"Unable to load dashboard data: {e}")
