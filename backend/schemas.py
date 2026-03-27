from pydantic import BaseModel
from datetime import datetime

class StudentRegisterReq(BaseModel):
    student_id: str

class RegistrationDeleteReq(BaseModel):
    class_date: datetime 

# Định nghĩa các schema cơ bản để tạo mới
class ParentCreate(BaseModel):
    name: str; phone: str; email: str

class StudentCreate(BaseModel):
    name: str; dob: datetime; gender: str; current_grade: str; parent_id: str

class ClassCreate(BaseModel):
    name: str; subject: str; day_of_week: int; time_slot: str; teacher_name: str; max_students: int

class SubscriptionCreate(BaseModel):
    student_id: str; package_name: str; start_date: datetime; end_date: datetime; total_sessions: int