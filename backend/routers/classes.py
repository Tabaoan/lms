import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter()

def generate_id(): return str(uuid.uuid4())

@router.post("/classes")
def create_class(cls: schemas.ClassCreate, db: Session = Depends(get_db)):
    db_class = models.ClassModel(id=generate_id(), **cls.model_dump())
    db.add(db_class)
    db.commit()
    return db_class

@router.get("/classes")
def get_classes(day: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.ClassModel)
    if day is not None:
        query = query.filter(models.ClassModel.day_of_week == day)
    
    classes = query.all()
    result = []
    for c in classes:
        c_dict = {col.name: getattr(c, col.name) for col in c.__table__.columns}
        c_dict["_count"] = {"registrations": len(c.registrations)}
        result.append(c_dict)
    return result

@router.post("/classes/{class_id}/register")
def register_class(class_id: str, req: schemas.StudentRegisterReq, db: Session = Depends(get_db)):
    target_class = db.query(models.ClassModel).filter(models.ClassModel.id == class_id).first()
    if not target_class: raise HTTPException(status_code=404, detail="Lớp không tồn tại")
    
    if len(target_class.registrations) >= target_class.max_students:
        raise HTTPException(status_code=400, detail="Lớp đã đầy")

    now = datetime.utcnow()
    active_sub = db.query(models.Subscription).filter(
        models.Subscription.student_id == req.student_id,
        models.Subscription.end_date >= now,
        models.Subscription.used_sessions < models.Subscription.total_sessions
    ).first()
    
    if not active_sub: raise HTTPException(status_code=400, detail="Hết gói học hoặc gói hết hạn")

    student_regs = db.query(models.ClassRegistration).filter(models.ClassRegistration.student_id == req.student_id).all()
    if any(reg.class_.day_of_week == target_class.day_of_week and reg.class_.time_slot == target_class.time_slot for reg in student_regs):
        raise HTTPException(status_code=400, detail="Trùng lịch")

    try:
        new_reg = models.ClassRegistration(id=generate_id(), class_id=class_id, student_id=req.student_id)
        db.add(new_reg)
        active_sub.used_sessions += 1
        db.commit()
        return {"message": "Đăng ký thành công"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/registrations/{reg_id}")
def cancel_registration(reg_id: str, req: schemas.RegistrationDeleteReq, db: Session = Depends(get_db)):
    reg = db.query(models.ClassRegistration).filter(models.ClassRegistration.id == reg_id).first()
    if not reg: raise HTTPException(status_code=404, detail="Không tìm thấy")

    now = datetime.utcnow()
    diff_hours = (req.class_date.replace(tzinfo=None) - now).total_seconds() / 3600
    refunded = False

    try:
        if diff_hours > 24:
            sub = db.query(models.Subscription).filter(models.Subscription.student_id == reg.student_id).order_by(models.Subscription.end_date.desc()).first()
            if sub and sub.used_sessions > 0:
                sub.used_sessions -= 1
                refunded = True
        
        db.delete(reg)
        db.commit()
        return {"message": "Đã hủy" + (" và hoàn buổi." if refunded else " (Sát giờ, không hoàn buổi).")}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))