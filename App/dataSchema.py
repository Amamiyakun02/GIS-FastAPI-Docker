from pydantic import BaseModel, field_validator, Field
from shapely.geometry import Polygon, Point, LineString
from shapely.validation import explain_validity
from typing import TypeVar, Dict, Any

GeometryType = TypeVar('GeometryType', Point, Polygon, LineString)


class GeoSchema(BaseModel):
    id: int
    name: str
    jenis: str
    geom: Dict[str, Any]

    class Config:
        from_attributes = True

    # @field_validator('geom')
    # def validate_polygon(cls, points):
    #     polygon_data = Polygon(points)
    #     if not polygon_data.is_valid:
    #         raise ValueError(f"Invalid polygon: {explain_validity(polygon_data)}")
    #     return points


class ReqeustSchema(BaseModel):
    parameter: GeoSchema = Field(...)


class ResponseSchema(BaseModel):
    code: int
    message: str
    status: str
    data: Dict[str, Any]

