from sqlalchemy import Column, Boolean, Integer, Float, Enum, DateTime, String, event, DDL, orm, UniqueConstraint, ForeignKey, PrimaryKeyConstraint, Sequence
from datetime import datetime
import enum

Base = orm.declarative_base()

class UnitModel(Base):
    __tablename__ = 'unit_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    unit = Column(String(50), nullable=False)

    __table_args__ = (UniqueConstraint('name', 'unit', name='_unit_model_uc'),)

StringMapSequence = Sequence('string_map_val_seq', metadata=Base.metadata, start=1)

class StringMapModel(Base):

    __tablename__ = 'string_map_model'
    id = Column(Integer, primary_key=True)
    measurement_id = Column(String(50), ForeignKey('measurement_model.id'), nullable=False)
    value = Column(Float, StringMapSequence, nullable=False, server_default=StringMapSequence.next_value())
    string = Column(String(75), nullable=False)

    __table_args__ = (UniqueConstraint('value', 'string', name='_string_map_model_uc'),)


class MeasurementModel(Base):
    __tablename__ = 'measurement_model'
    id = Column(String(50), primary_key=True)
    name = Column(String(75), nullable=False, unique=True)
    unit_id = Column(Integer, ForeignKey('unit_model.id'))
    has_string_values = Column(Boolean, nullable=False, default=False)

class LaboratoryModel(Base):
    __tablename__ = 'laboratory_model'
    id = Column(String(50), primary_key=True)
    name = Column(String(75), nullable=False, unique=True)
    description = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

    __table_args__ = (UniqueConstraint('latitude', 'longitude', name='laboratory_model_uc'),)

class DeviceModel(Base):
    __tablename__ = 'device_model'

    def get_default_name(context):
        return context.get_current_parameters().get("id", "Unknown")

    id = Column(String(50), primary_key=True)
    lab_id = Column(String(50), ForeignKey('laboratory_model.id'), nullable=False)
    name = Column(String(75), nullable=False, default=get_default_name)
    port = Column(String(8), nullable=False, default="main")

ValueSequence = Sequence('value_id_seq', metadata=Base.metadata, start=1)

class ValueModel(Base):
    __tablename__ = 'value_model'

    id = Column(Integer, ValueSequence, server_default=ValueSequence.next_value())
    time = Column(DateTime, default=datetime.now, nullable=False)
    lab_id = Column(String(50), ForeignKey('laboratory_model.id'), nullable=False)
    device_id = Column(String(50), ForeignKey('device_model.id'), nullable=False)
    measurement_id = Column(String(50), ForeignKey('measurement_model.id'), nullable=False)
    value = Column(Float)

    __table_args__ = (PrimaryKeyConstraint('time', 'lab_id', 'device_id', 'measurement_id', name='value_model_pk'),)

class TmpValueModel(Base):
    __tablename__ = 'tmp_value_model'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    lab_id = Column(String(50), ForeignKey('laboratory_model.id'), nullable=False)
    device_id = Column(String(50), ForeignKey('device_model.id'), nullable=False)
    measurement_id = Column(String(50), ForeignKey('measurement_model.id'), nullable=False)
    value = Column(Float)

class Role(enum.Enum):
    ADMIN = 1
    EDITOR = 2
    VIEWER = 3

class UserModel(Base):
    __tablename__ = 'user_model'

    login = Column(String(50), primary_key=True)
    role = Column(Enum(Role), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))

event.listen(
    ValueModel.__table__,
    'after_create',
    DDL(f"SELECT create_hypertable('{ValueModel.__tablename__}', 'time');")
)