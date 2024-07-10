from dotenv import load_dotenv
import json
from fastapi import FastAPI

from typing import AsyncIterable
from fastapi.responses import StreamingResponse

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()
app = FastAPI()

prompt = ChatPromptTemplate.from_messages(('human', "Generate biography for {n} persons"))
model = ChatOpenAI(model="gpt-3.5-turbo-0125")


class Biography(BaseModel):
    name: str = Field(description='The first name of the person')
    surname: str = Field(description='The surname of the person')
    birth_place: str = Field(description='The birth place of the person')
    biography: str = Field(description='The biography of the person')


class Biographies(BaseModel):
    biographies: list[Biography] = Field(description='The list of biographies of the persons')


model = model.with_structured_output(Biographies)
chain = prompt | model


async def send_message(n_persons: int) -> AsyncIterable[str]:
    async for chunk in chain.astream({'n': n_persons}):
        yield json.dumps(chunk.dict())


@app.post("/stream_biographies/")
async def stream_biographies(persons: int):
    generator = send_message(persons)
    return StreamingResponse(generator, media_type="text/event-stream")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
