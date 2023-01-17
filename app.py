import ujson
from socketify import App, sendfile
from pydantic import BaseModel, UUID4
from pydantic_factories import ModelFactory
from datetime import datetime
from faker import Faker

fake = Faker()


class Person(BaseModel):
    id: UUID4
    name: str
    address: str
    age: int
    birthday: datetime


class PersonModelFactory(ModelFactory):
    __model__ = Person

    name = fake.name
    address = fake.address


class Example(BaseModel):
    your_ip: str
    your_user_agent: str
    example: Person


app = App()
app.json_serializer(ujson)


def get_client_ip(req) -> str:
    try:
        return req.get_header("x-forwarded-for").split(",")[0].strip()
    except Exception:
        pass

    ip = req.get_header("x-real-ip")
    if ip:
        return ip
    return ""


async def json(res, req):
    m = Example(
        example=PersonModelFactory.build(),
        your_user_agent=req.get_header("user-agent") or "",
        your_ip=get_client_ip(req),
    )
    res.write_status(200).write_header(b"Content-Type",
                                       b"application/json").end(m.json())


async def swagger(res, req):
    await sendfile(res, req, "./public/swagger.html")


async def openapi(res, req):
    await sendfile(res, req, "./public/openapi.json")


async def not_found(res, req):
    res.write_status(404).end("Not Found")


app.get("/", swagger)
app.get("/openapi.json", openapi)
app.get("/example", json)
app.any("/*", not_found)

app.listen(
    8000,
    lambda config: print(
        f"Listening on port http://localhost:{config.port} now"),
)

app.run()
