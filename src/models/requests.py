from pydantic import BaseModel
from typing import List, Annotated, Optional


class ReviewSuggestion(BaseModel):
    """A model representing a single review suggestion item."""
    line_number_start: Annotated[int, ..., "Starting line number for the suggestion"]
    line_number_end: Annotated[int, ..., "Ending line number for the suggestion"]
    suggestion: Annotated[str, ..., "The suggested code change"]
    suggestion_diff: Annotated[Optional[str], None, "The diff representation of the suggestion, if applicable"]

class LLMResponseStructure(BaseModel):
    """A model representing the structure of the response from the LLM service."""
    items: Annotated[List[ReviewSuggestion], ..., "List of review suggestions"]
    
