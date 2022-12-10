from fastapi import APIRouter, HTTPException, Path, Depends, Request
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import Response, RequestDevice, RequestLaboratory, RequestMeasurement, RequestUnit, RequestValue, DeviceSchema, LaboratorySchema, MeasurementSchema, UnitSchema, ValueSchema, StringMapSchema, ValueCompressedSchema
import queries

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/units", response_model=list[UnitSchema])
async def get_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    units = queries.get_units(db, skip, limit)
    return units

@router.get("/stringmaps", response_model=list[StringMapSchema])
async def get_stringmaps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stringmaps = queries.get_stringmaps(db, skip, limit)
    return stringmaps

@router.get("/measurements", response_model=list[MeasurementSchema])
async def get_measurements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    measurements = queries.get_measurements(db, skip, limit)
    return measurements

@router.get("/devices", response_model=list[DeviceSchema])
async def get_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = queries.get_devices(db, skip, limit)
    return devices

@router.get("/labs", response_model=list[LaboratorySchema])
async def get_labs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    labs = queries.get_labs(db, skip, limit)
    return labs

@router.get("/values", response_model=list[ValueSchema])
async def get_values(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    values = queries.get_values(db, request.query_params._dict, skip, limit)
    return values

@router.get("/values/yesterday", response_model=list[ValueCompressedSchema])
async def get_yesterday_values(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    values = queries.get_yesterday_values(db, request.query_params._dict, skip, limit)
    return values

@router.get("/units/{unit_id}", response_model=UnitSchema)
async def get_unit(unit_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    unit = queries.get_unit(db, unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit

@router.get("/measurements/{measurement_id}", response_model=MeasurementSchema)
async def get_measurement(measurement_id: str = Path(...), db: Session = Depends(get_db)):
    measurement = queries.get_measurement(db, measurement_id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement

@router.get("/devices/{device_id}", response_model=DeviceSchema)
async def get_device(device_id: str = Path(...), db: Session = Depends(get_db)):
    device = queries.get_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.get("/labs/{lab_id}", response_model=LaboratorySchema)
async def get_lab(lab_id: str = Path(...), db: Session = Depends(get_db)):
    lab = queries.get_lab(db, lab_id)
    if lab is None:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    return lab

@router.get("/values/{value_id}", response_model=ValueSchema)
async def get_value(value_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    value = queries.get_value(db, value_id)
    if value is None:
        raise HTTPException(status_code=404, detail="Value not found")
    return value