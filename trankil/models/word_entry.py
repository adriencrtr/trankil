from typing import Optional

from pydantic import BaseModel


class Example(BaseModel):
    src: str
    dst: str


class Translation(BaseModel):
    featured: bool
    text: str
    pos: str
    examples: list[Example]
    usage_frequency: Optional[str] = None


class WordEntry(BaseModel):
    featured: bool
    text: str
    pos: str
    translations: list[Translation]
