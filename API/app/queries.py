from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app import models
from app import schemas

def get_units(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UnitModel).offset(skip).limit(limit).all()

def get_stringmaps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StringMapModel).offset(skip).limit(limit).all()

def get_measurements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MeasurementModel).offset(skip).limit(limit).all()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DeviceModel).offset(skip).limit(limit).all()

def get_labs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LaboratoryModel).offset(skip).limit(limit).all()

def get_values(db: Session, filters: dict = {}, skip: int = 0, limit: int = 100):

    query = db.query(models.ValueModel)

    if filters.get('from'):
        ts = datetime.fromtimestamp(int(filters.get('from')))
        query = query.filter(models.ValueModel.time >= ts)
    
    if filters.get('to'):
        ts = datetime.fromtimestamp(int(filters.get('to')))
        query = query.filter(models.ValueModel.time <= ts)

    return query.offset(skip).limit(limit).all()

def get_yesterday_values(db: Session, filters: dict = {}, skip: int = 0, limit: int = 100):
    
        query = db.query(models.ValueModel)

        from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        to_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        from_str = from_date.strftime("%Y-%m-%d %H:%M:%S")
        to_str = to_date.strftime("%Y-%m-%d %H:%M:%S")

        bucket = 15

        if filters.get('bucket') and int(filters.get('bucket')) > 5:
            bucket = int(filters.get('bucket'))

        query = db.execute(f'''
        SELECT value, bucket as time, lab_id, device_id, measurement_id
        FROM (
        SELECT time_bucket('{bucket} minute', time) as bucket,
            lab_id,
            device_id,
            measurement_id,
            avg(value) as value
        FROM value_model
        WHERE time >= '{from_str}' and time <= '{to_str}'
        GROUP BY bucket,
            lab_id,
            device_id,
            measurement_id
        ) buckets
        ''')
    
        return query.all()

def get_unit(db: Session, unit_id: int):
    return db.query(models.UnitModel).filter(models.UnitModel.id == unit_id).first()

def get_measurement(db: Session, measurement_id: int):
    return db.query(models.MeasurementModel).filter(models.MeasurementModel.id == measurement_id).first()

def get_device(db: Session, device_id: int):
    return db.query(models.DeviceModel).filter(models.DeviceModel.id == device_id).first()

def get_lab(db: Session, lab_id: int):
    return db.query(models.LaboratoryModel).filter(models.LaboratoryModel.id == lab_id).first()

def get_value(db: Session, value_id: int):
    return db.query(models.ValueModel).filter(models.ValueModel.id == value_id).first()