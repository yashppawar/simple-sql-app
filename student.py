from pydantic import BaseModel

SUBJECTS = ["Maths", "Science", "English", "Social Studies", "Information Technology", "Art"]

class Student(BaseModel):
    _id: int
    fname: str
    lname: str
    marks: dict[str, int]
    email: str = ""

    @classmethod
    def from_list(cls, data: list):
        _id = data[0]
        fname = data[1]
        lname = data[2]
        marks = {SUBJECTS[i]: data[i + 3] for i in range(len(data) - 4)}
        email = data[-1]
        
        return cls(_id = _id, fname=fname, lname=lname, marks=marks, email=email)

    @property
    def name(self):
        return f"{self.fname} {self.lname}".title()

