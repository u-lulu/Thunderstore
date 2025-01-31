from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SchemaThunderstoreSection(BaseModel):
    name: str
    exclude_categories: List[str] = Field(default=[], alias="excludeCategories")
    require_categories: List[str] = Field(default=[], alias="requireCategories")


class SchemaThunderstoreCategory(BaseModel):
    label: str


class SchemaCommunity(BaseModel):
    display_name: str = Field(alias="displayName")
    categories: Dict[str, SchemaThunderstoreCategory]
    sections: Dict[str, SchemaThunderstoreSection]
    discord_url: Optional[str] = Field(alias="discordUrl")
    wiki_url: Optional[str] = Field(alias="wikiUrl")


class SchemaGameMeta(BaseModel):
    displayName: str


class SchemaGame(BaseModel):
    meta: SchemaGameMeta
    thunderstore: Optional[SchemaCommunity]


class Schema(BaseModel):
    schema_version: str = Field(alias="schemaVersion")
    games: Dict[str, SchemaGame]
    communities: Dict[str, SchemaCommunity]
