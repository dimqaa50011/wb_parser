from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import settings

engine = create_async_engine(url=settings.db.uri(), echo=settings.project.debug)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)
