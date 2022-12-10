from typing import List, Optional, Generic, TypeVar
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class UnitSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    unit: Optional[str] = None

    class Config:
        orm_mode = True

class StringMapSchema(BaseModel):
    id: Optional[int] = None
    measurement_id: Optional[str] = None
    value: Optional[float] = None
    string: Optional[str] = None

    class Config:
        orm_mode = True

class MeasurementSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    unit_id: Optional[int] = None
    has_string_values: Optional[bool] = None

    class Config:
        orm_mode = True

class LaboratorySchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        orm_mode = True

class DeviceSchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    port: Optional[str] = None
    description: Optional[str] = None
    lab_id: Optional[str] = None

    class Config:
        orm_mode = True

class ValueSchema(BaseModel):
    id: Optional[int] = None
    time: Optional[datetime] = None
    lab_id: Optional[str] = None
    device_id: Optional[str] = None
    measurement_id: Optional[str] = None
    value: Optional[float] = None

    class Config:
        orm_mode = True

class ValueCompressedSchema(BaseModel):
    time: Optional[datetime] = None
    lab_id: Optional[str] = None
    device_id: Optional[str] = None
    measurement_id: Optional[str] = None
    value: Optional[float] = None

    class Config:
        orm_mode = True

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestUnit(BaseModel):
    parameter: UnitSchema = Field(...)

class RequestStringMap(BaseModel):
    parameter: StringMapSchema = Field(...)

class RequestMeasurement(BaseModel):
    parameter: MeasurementSchema = Field(...)

class RequestLaboratory(BaseModel):
    parameter: LaboratorySchema = Field(...)

class RequestDevice(BaseModel):
    parameter: DeviceSchema = Field(...)

class RequestValue(BaseModel):
    parameter: ValueSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]