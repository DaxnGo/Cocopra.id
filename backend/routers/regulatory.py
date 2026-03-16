from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List

router = APIRouter()

@router.get("/search", response_model=List[schemas.PesticideResponse])
def search_pesticide(
    q: str = Query(..., min_length=2, description="Kata kunci pencarian nama pestisida"),
    db: Session = Depends(get_db)
):
    """
    Fitur Regulatory Check: Mencari data pestisida resmi dari Kementan.
    Hanya mengembalikan maksimal 10 hasil teratas agar respon super cepat.
    Pencarian menggunakan ILIKE (case-insensitive & partial match).
    """
    search_keyword = f"%{q}%"
    
    # Query ke database dengan batas 10 hasil
    results = db.query(models.PesticideRegistry).filter(
        models.PesticideRegistry.nama_pestisida.ilike(search_keyword)
    ).limit(10).all()
    
    return results
