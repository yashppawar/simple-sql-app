from student import Student
from data import StudentDB
import streamlit as st
import matplotlib.pyplot as plt

st.write("Hello")
home, add_student = st.tabs(["Home", "➕ Add Student"])

db = StudentDB()
db.create()

with home:
    id_ = st.text_input("ID", "2106306")
    student = db.get(id_)

    if not student:
        st.warning(f"Student with {id_} Not Found. Please go to ➕ Add Student to add the student")
    else:
        marks = student.marks.values()      
        marks_data = { "Subject": student.marks.keys(), "Marks": marks }

        st.write(f"## Student: {student.name}")
        st.write(f"#### Email: {student.email}")

        _, c2, c3, _  = st.columns([25, 25, 25, 25])

        total = sum(marks)

        c2.metric("Total", f"{total}", f"out of {100 * len(marks)}", delta_color="off")
        c3.metric("Percentage", f"{total/len(marks):2} %", "out of 100 %", delta_color="off")

        table, chart = st.tabs(["Table", "Chart"])

        with chart, plt.xkcd():
            fig, ax = plt.subplots()

            ax.bar(marks_data["Subject"], marks_data["Marks"])

            ax.set_ylabel('Marks Obtained...')
            ax.set_title('Courses/Subjects')
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)

            st.pyplot(fig)

        with table:
            st.table(marks_data)

    if st.button("Celebrate"):
        st.balloons()
        st.snow()
        
with add_student, st.form("Add Student", True):
    c1, c2 = st.columns([30, 70])
    id_ = c1.text_input("Enrollment No./ID")
    email = c2.text_input("Email:")

    c1, c2 = st.columns([50, 50])

    fname = c1.text_input("First Name")
    lname = c2.text_input("Last Name")

    c1, c2, c3 = st.columns([33, 34, 33])
    math = c1.number_input("Maths", 0, 100, format = "%d")
    sci = c2.number_input("Science", 0, 100, format = "%d")
    eng = c3.number_input("English", 0, 100, format = "%d")
    
    sst = c1.number_input("Social Studies", 0, 100, format = "%d")
    it = c2.number_input("Information Technology", 0, 100, format = "%d")

    _, cm, _ = st.columns([40, 20, 40])
    submit = cm.form_submit_button("Submit")

    if submit:
        ins = db.insert(id_, fname, lname, math, sci, eng, sst, it, email)
        if ins:
            st.success(f"Student with ID {id_} Added Successfully")
        else:
            st.error(f"Student with ID {id_} Already Exists, try a different one")
