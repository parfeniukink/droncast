from fastapi import APIRouter

router = APIRouter(prefix="/bazinga", tags=["Debug"])


@router.get("")
async def bazinga() -> None:
    """Test resource to see that the server is running."""

    print("Bazinga!")
