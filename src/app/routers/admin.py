from typing import Annotated

from fastapi import APIRouter, Request, Depends

from ..dependencies import templates
from ..models import User, is_admin
from ..config import db
from ..ressources.session import cookie

router = APIRouter()


@router.get("", dependencies=[Depends(cookie)])
async def root(request: Request, current_user: Annotated[User, Depends(is_admin)]):
    return 'no template'