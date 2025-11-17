from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    category: str
    suggested_response: str = Field(alias="suggestedResponse")

    class Config:
        # Pydantic v2 mudou o nome desta configuração
        populate_by_name = True
        json_schema_extra = {"by_alias": True}