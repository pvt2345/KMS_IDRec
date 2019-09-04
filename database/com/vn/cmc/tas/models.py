from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String


Base = declarative_base()

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    can_cu = Column(String, nullable=False)
    loai_van_ban = Column(String, nullable=False)
    noi_ban_hanh = Column(String, nullable=False)
    noi_nhan = Column(String)
    so_van_ban = Column(String, unique=True)
    phu_luc = Column(String)
    thoi_gian = Column(String)
    trich_yeu = Column(String)
    yeu_cau = Column(String)
    dia_diem = Column(String)

class Document_Dtl(Base):
    __tablename__ = 'document_dtl'
    id = Column(Integer, primary_key=True)
    parent = Column(String)
    type = Column(String)
    stt = Column(String)
    tieu_de = Column(String)
    content = Column(String)