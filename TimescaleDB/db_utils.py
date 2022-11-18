import db
import models
from datetime import datetime

def get_or_create_user(login, role=models.Role.VIEWER) -> models.UserModel:
    try:
        email = login + '@uniandes.edu.co'
        user = db.session.query(models.UserModel).filter_by(login=login).first()
        if user is None:
            user = models.UserModel(login=login, role=role, email=email)
            db.session.add(user)
            db.session.commit()
        return user
    except Exception as e:
        print(e)
        db.session.rollback()
        return None

def get_or_create_device(lab_id, id, port) -> models.DeviceModel:
    try:
        device = db.session.query(models.DeviceModel).filter_by(id=id).first()
        if device is None:
            device = models.DeviceModel(lab_id=lab_id, id=id, port=port)
            db.session.add(device)
            db.session.commit()
        return device
    except Exception as e:
        print(e)
        db.session.rollback()
        return None

def get_or_create_lab(id, name) -> models.LaboratoryModel:
    try:
        lab = db.session.query(models.LaboratoryModel).filter_by(id=id).first()
        if lab is None:
            lab = models.LaboratoryModel(id=id, name=name)
            db.session.add(lab)
            db.session.commit()
        return lab
    except Exception as e:
        print(e)
        db.session.rollback()
        return None

def create_value(lab_id, device_id, measurement_id, value) -> models.ValueModel:
    try:
        print("Creating value")
        print(f"{lab_id} {device_id} {measurement_id} {value}")
        value = models.ValueModel(lab_id=lab_id, device_id=device_id, measurement_id=measurement_id, value=value)
        db.session.add(value)
        db.session.commit()
        return value
    except Exception as e:
        # print(e)
        #db.session.rollback()
        return None
    

def get_or_create_measurement(id, name, unit_id, has_string_values) -> models.MeasurementModel:
    try:
        measurement = db.session.query(models.MeasurementModel).filter_by(id=id).first()
        if measurement is None:
            measurement = models.MeasurementModel(id=id, name=name, unit_id=unit_id, has_string_values=has_string_values)
            db.session.add(measurement)
            db.session.commit()
        return measurement
    except Exception as e:
        print(e)
        #db.session.rollback()
        return None

def get_or_create_unit(id, name) -> models.UnitModel:
    try:
        unit = db.session.query(models.UnitModel).filter_by(id=id).first()
        if unit is None:
            unit = models.UnitModel(id=id, name=name)
            db.session.add(unit)
            db.session.commit()
        return unit
    except Exception as e:
        print(e)
        db.session.rollback()
        return None

def get_or_create_string(measurement_id, string) -> models.StringMapModel:
    try:
        db_string = db.session.query(models.StringMapModel).filter_by(
            measurement_id=measurement_id, string=string).first()
        if db_string is None:
            db_string = models.StringMapModel(
                measurement_id=measurement_id, string=str(string))
            db.session.add(db_string)
            db.session.commit()
        return db_string
    except Exception as e:
        print(e)
        db.session.rollback()
        return None