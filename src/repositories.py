from decimal import Decimal
from typing import Optional, Protocol, Sequence, Type, TypeVar

from sqlalchemy import (
    Delete,
    Result,
    Select,
    Update,
    delete,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .errors import ExecuteError, ProductNotCreated, ProductNotFound

from .models import BaseDBModel, Product

from .specifications import Specification


T = TypeVar("T", bound=BaseDBModel, covariant=True)


class BaseRepositoryProtocol(Protocol[T]):

    async def find_all(self) -> Sequence[T]: ...

    async def find(self, spec: Specification) -> T | None: ...

    async def create(self, data: dict[str, int | str | Decimal]) -> T: ...

    async def refresh(
        self, spec: Specification, upd_data: dict[str, int | str | Decimal]
    ) -> None: ...

    async def remove(self, spec: Specification) -> None: ...


class BaseRepository(BaseRepositoryProtocol[T]):
    model: Type[T]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: dict[str, int | str | Decimal]) -> T:
        new_item = self.model(**data)
        self._session.add(new_item)

        try:
            await self._session.commit()
            return new_item
        except IntegrityError as ex:
            await self._session.rollback()
            raise ProductNotCreated(f"product not created; {data=} error = {ex}")

    async def find_all(self) -> Sequence[T]:
        stmt = select(self.model)
        try:
            result = await self._execute(stmt)
            return result.scalars().all()
        except ExecuteError:
            raise ProductNotFound(f"products not found")

    async def find(self, spec: Specification) -> T | None:
        stmt = select(self.model).where(*spec.is_satisfied())
        try:
            result = await self._execute(stmt)
            return result.scalar()
        except ExecuteError:
            raise ProductNotFound(f"product not found; spec = {spec}")

    async def refresh(
        self, spec: Specification, upd_data: dict[str, int | str | Decimal]
    ):
        stmt = update(self.model).where(*spec.is_satisfied()).values(**upd_data)
        try:
            res = await self._execute(stmt)
            return getattr(res, "rowcount")
        except ExecuteError:
            pass

    async def remove(self, spec: Specification):
        stmt = delete(self.model).where(*spec.is_satisfied())
        try:
            res = await self._execute(stmt)
            return getattr(res, "rowcount")
        except ExecuteError:
            pass

    async def _execute(self, stmt: Select | Update | Delete) -> Result:
        try:
            result = await self._session.execute(stmt)
            await self._session.commit()
            return result
        except IntegrityError:
            await self._session.rollback()
            raise ExecuteError()


class ProductRepository(BaseRepository[Product]):
    model = Product

    async def create(self, data: dict[str, int | str | Decimal]) -> Product:
        return await super().create(data)

    async def find(self, spec: Specification) -> Product | None:
        return await super().find(spec)

    async def find_all(self) -> Sequence[Product]:
        return await super().find_all()

    async def refresh(
        self, spec: Specification, upd_data: dict[str, int | str | Decimal]
    ):
        return await super().refresh(spec, upd_data)

    async def remove(self, spec: Specification):
        return await super().remove(spec)
