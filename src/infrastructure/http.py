from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, alias_generators


class ResponseMulti(PublicData, Generic[_TPublicData]):
    """Generic response model that consist multiple results."""

    result: Sequence[_TPublicData]


class Response(PublicData, Generic[_TPublicData]):
    """Generic response model that consist only one result."""

    result: _TPublicData


class ErrorResponse(PublicData):
    """Error response model."""

    message: str = Field(description="This field represent the message")
