from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Класс для пользователей
class User(Base):
    __tablename__ = 'пользователи'
    id = Column(Integer, primary_key=True)
    логин = Column(String(50), unique=True, nullable=False)
    пароль = Column(String(255), nullable=False)
    имя = Column(String(100), nullable=False)
    email = Column(String(100))
    роль = Column(String(50), default='тренер')

# Класс для спортсменов
class Athlete(Base):
    __tablename__ = 'спортсмены'
    id = Column(Integer, primary_key=True)
    имя = Column(String(100), nullable=False)
    фамилия = Column(String(100), nullable=False)
    дата_рождения = Column(Date, nullable=False)
    вид_спорта = Column(String(100), nullable=False)
    тренер_id = Column(Integer, ForeignKey('пользователи.id'))
    активен = Column(Boolean, default=True)
    тренер = relationship("User", back_populates="спортсмены")

User.спортсмены = relationship("Athlete", back_populates="тренер")

# Класс для соревнований
class Competition(Base):
    __tablename__ = 'соревнования'
    id = Column(Integer, primary_key=True)
    название = Column(String(255), nullable=False)
    дата_проведения = Column(Date, nullable=False)
    место = Column(String(255), nullable=False)
    описание = Column(String)
    завершено = Column(Boolean, default=False)
    участники = relationship("Athlete", secondary="участие_в_соревнованиях")

# Связующая таблица для участия
class Participation(Base):
    __tablename__ = 'участие_в_соревнованиях'
    id = Column(Integer, primary_key=True)
    спортсмен_id = Column(Integer, ForeignKey('спортсмены.id'))
    соревнование_id = Column(Integer, ForeignKey('соревнования.id'))
    результат = Column(String(100))

# Подключение к базе данных
class Connect:
    @staticmethod
    def create_connection():
        try:
            engine = create_engine("postgresql://postgres:1234@localhost:5432/paralimp_reserve", echo=True)
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            print("Подключение к базе данных успешно!")
            return session
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise