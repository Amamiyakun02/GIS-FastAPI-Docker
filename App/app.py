from .database import Base, Session, engine
from fastapi import FastAPI, APIRouter, HTTPException, Path, Depends
from fastapi.middleware.cors import CORSMiddleware
from .Models.geomodel import GeoModel
from .dataSchema import GeoSchema, ReqeustSchema, ResponseSchema
from geoalchemy2.shape import to_shape
from shapely import wkt, geometry
from starlette.responses import RedirectResponse

app: FastAPI = FastAPI()


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url='/docs')


router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


# @app.get('/info')
# async def info() -> Dict[str, str | int]:
#     data = {
#         "text": "hello world"
#     }
#     return data


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


db: Session = Session()


def insert_data(db: Session, nama: str, jenis: str, geometri: str):
    geodata = GeoModel(name=nama, jenis=jenis, geom=geometri)
    db.add(geodata)
    db.commit()
    db.refresh(geodata)
    return geodata


geom = ('POLYGON((114.76623336574977 -3.803239010534085, 114.76730684747503 -3.8036344233002524, 114.76697649419629 '
        '-3.804831168394543, 114.76582233148667 -3.8045940529667917, 114.76620987938554 -3.803223686816878, '
        '114.76623336574977 -3.803239010534085))')


# new_data = insert_data(db=db,
#                        nama="Taman Hasan Basri",
#                        jenis="taman",
#                        geometri=geom
#                        )


def get_data(db: Session, data_id: int):
    return db.query(GeoModel).filter(GeoModel.id == data_id).first()


@router.get("/{id}", response_model=ResponseSchema)
async def get_geo_data(id: int, db: Session = Depends(get_db)):
    _geodata = get_data(db, id)

    geom_wkt = None
    if _geodata.geom:
        geom_wkt = to_shape(_geodata.geom).wkt
    _geodata.geom = geom_wkt
    _geodata.geom = geometry.mapping(wkt.loads(_geodata.geom))

    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "nama": _geodata.name,
                    "jenis": _geodata.jenis
                },
                "geometry": _geodata.geom
            }
        ]
    }

    return ResponseSchema(code=200, message="Success To Get Spatial Data", status="Success", data=data).dict(
        exclude_none=True)


@app.get('/geojson')
async def get_json_data():
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "Nama": "RSUD H. Boejasin"
                },
                "geometry": {
                    "coordinates": [
                        [114.777711716337, -3.79877715744155],
                        [114.779478974795, -3.79867602470041],
                        [114.779582566859, -3.79972930976304],
                        [114.777575399683, -3.79997811637318],
                        [114.777541989589, -3.79962036485935],
                        [114.777764018277, -3.7996278031942],
                        [114.777707056788, -3.79876816303074]
                    ],
                    "type": "LineString"
                },
                "id": 0
            },
            {
                "type": "Feature",
                "properties": {
                    "Nama": "MTSN 2 Tanah Laut"
                },
                "geometry": {
                    "coordinates": [
                        [114.781848280404, -3.79584298048457],
                        [114.782815024739, -3.79635305472237],
                        [114.783203453479, -3.79564095406683],
                        [114.782155659445, -3.79511113524057],
                        [114.781855117287, -3.79584515304146]
                    ],
                    "type": "LineString"
                },
                "id": 1
            }
        ]
    }
    return data


# Define Route
app.include_router(router, prefix="/geo", tags=["geo"])
