import json
from typing import Any, Literal, Mapping, Optional, TypeAlias

from aiohttp import ClientSession

METHODS = Literal["post", "get"]

ReturnWBData: TypeAlias = dict[str, list | str | int | float]
RequestParamsType: TypeAlias = Mapping[str, Any]


class WildberiesParser:
    _BASE_URL: str = "https://card.wb.ru/cards/v1/detail"
    _DEFAULT_PARAMS = {
        "appType": "1",
        "curr": "rub",
        "dest": "-1257786",
        "spp": "30",
    }
    _DEFAULT_HEADERS = {"Content-Type": "application/json"}

    async def get_product(self, articul: int) -> ReturnWBData | None:
        q_params = self._DEFAULT_PARAMS.copy()
        q_params["nm"] = str(articul)

        return await self._send_request("get", self._BASE_URL, params=q_params)

    async def _send_request(
        self,
        method: METHODS,
        url: str,
        *_,
        params: Optional[dict[str, str]] = None,
        data: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> ReturnWBData | None:
        request_params: RequestParamsType = self._get_request_params(
            method=method, url=url, params=params, headers=headers, data=data
        )

        async with ClientSession() as session:
            async with session.request(**request_params) as response:
                if response.ok:
                    return await response.json()
                return None

    def _get_request_params(
        self,
        method: METHODS,
        url: str,
        *_,
        params: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
        data: Optional[dict[str, str]] = None,
    ) -> RequestParamsType:

        request_params: RequestParamsType = {
            "method": method,
            "url": url,
            "headers": self._DEFAULT_HEADERS.copy(),
        }
        if params is not None:
            request_params["params"] = params

        if data is not None:
            request_params["data"] = json.dumps(data)

        if headers is not None:
            if isinstance(request_params["headers"], dict):
                request_params["headers"].update(headers)

        return request_params
