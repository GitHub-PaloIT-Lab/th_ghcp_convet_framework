"""Favorites API routes"""
from fastapi import APIRouter, HTTPException, Path, Request
from typing import List

from weather_api.api.schemas import (
    FavoriteResponse,
    FavoritesListResponse,
    MessageResponse
)


router = APIRouter()


def get_favorites(request: Request):
    """Get favorites manager from app state"""
    favorites = request.app.state.favorites
    if not favorites:
        raise HTTPException(status_code=500, detail="Favorites service not initialized")
    return favorites


@router.get(
    "",
    response_model=FavoritesListResponse,
    summary="List favorites",
    description="Get list of favorite locations"
)
async def list_favorites(request: Request):
    """Get list of favorite locations"""
    favorites = get_favorites(request)
    locations = favorites.list()
    
    return FavoritesListResponse(
        favorites=locations,
        count=len(locations)
    )


@router.post(
    "/{location}",
    response_model=MessageResponse,
    summary="Add favorite",
    description="Add a location to favorites"
)
async def add_favorite(request: Request, location: str = Path(..., description="Location name to add")):
    """Add a location to favorites"""
    favorites = get_favorites(request)
    
    try:
        favorites.add(location)
        return MessageResponse(message=f"Added '{location}' to favorites")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{location}",
    response_model=MessageResponse,
    summary="Remove favorite",
    description="Remove a location from favorites"
)
async def remove_favorite(request: Request, location: str = Path(..., description="Location name to remove")):
    """Remove a location from favorites"""
    favorites = get_favorites(request)
    
    try:
        favorites.remove(location)
        return MessageResponse(message=f"Removed '{location}' from favorites")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/{location}",
    response_model=FavoriteResponse,
    summary="Check if favorite",
    description="Check if a location is in favorites"
)
async def check_favorite(request: Request, location: str = Path(..., description="Location name to check")):
    """Check if a location is in favorites"""
    favorites = get_favorites(request)
    locations = favorites.list()
    
    if location in locations:
        return FavoriteResponse(location=location)
    else:
        raise HTTPException(status_code=404, detail=f"'{location}' not in favorites")
