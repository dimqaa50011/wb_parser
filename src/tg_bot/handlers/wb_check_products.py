from aiogram import F, Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.services import ProductService
from src.tg_bot.keyboards.wb_keyboard.check_product import markup
from src.tg_bot.keyboards.wb_keyboard.callbacdata import WBCallbackdata
from ..state import CheckProductState

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Чтобы проверить товар по артикулу нажми на кнопку 👇", reply_markup=markup
    )


@router.callback_query(WBCallbackdata.filter())
async def get_articul(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(CheckProductState.wait_articul)
    await call.message.answer("Пришли мне акртикул товара")


@router.message(CheckProductState.wait_articul)
async def get_product_info(
    message: Message, state: FSMContext, service: ProductService
):
    articul = message.text.strip()
    if not articul.isdigit():
        await message.answer("Артикул должен сосотять только из цифр")
        return
    product = await service.get_product(int(articul))
    if not product:
        await message.answer("Товар в базе не найден")
        return
    msg = "\n".join(
        (
            f"Артикул: {product.articul}",
            f"Цена: {product.price}",
            f"Цена со скидкой: {product.sale_price}",
            f"Рейтинг: {product.rating}",
            f"Остатки на складах: {product.quantity_sum}",
        )
    )
    await state.clear()
    await message.answer(msg)
