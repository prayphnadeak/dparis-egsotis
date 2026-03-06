"""Pagination helper utilities."""
from typing import List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[T]


def paginate(items: List[T], total: int, page: int, page_size: int) -> dict:
    """Build a paginated response dict."""
    total_pages = max(1, (total + page_size - 1) // page_size)
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": items,
    }


def get_skip(page: int, page_size: int) -> int:
    """Convert page number to SQL offset."""
    return (max(1, page) - 1) * page_size
