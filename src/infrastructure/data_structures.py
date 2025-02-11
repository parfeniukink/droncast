from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, alias_generators


class InternalData(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
    )


class PublicData(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        loc_by_alias=True,
        alias_generator=alias_generators.to_camel,
    )


_TPublicData = TypeVar("_TPublicData", bound=PublicData)


class ResponseMulti(PublicData, Generic[_TPublicData]):
    """Generic response model that consist multiple results."""

    result: Sequence[_TPublicData]


class Response(PublicData, Generic[_TPublicData]):
    """Generic response model that consist only one result."""

    result: _TPublicData


class ErrorResponse(PublicData):
    """Error response model."""

    message: str = Field(description="This field represent the message")
