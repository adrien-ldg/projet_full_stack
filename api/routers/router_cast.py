from fastapi import APIRouter, status, Depends, Request
from services import service_cast
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from shemas.shema import CastIn, CastOut, User
from models.db import get_db
from services.oauth2 import get_current_active_user
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="/cast", tags=["casts"])


#non
@router.post("/", status_code=status.HTTP_201_CREATED , response_model=CastOut)
async def create_cast(title_film:str, c: CastIn = Depends(), db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
        return service_cast.create_cast(c, title_film, db)


#non
@router.get("/{id}", status_code=status.HTTP_202_ACCEPTED , response_model=CastOut)
async def get_one_cast(id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service_cast.get_one_cast(id, db)


#oui
@router.get("/cast_film/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=List[CastOut])
async def get_cast_one_film(title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service_cast.get_cast_one_film(title, db)

#oui
@router.get("/cast_name/{name}", status_code=status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
async def get_cast_one_name(
    name: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    templates = request.app.state.templates

    # Appeler le service pour obtenir les données
    films = service_cast.get_cast_one_name(name, db)

    # Rendre le template
    return templates.TemplateResponse(
        "one_actor.html",
        {"request": request, "actor_name": name, "films": films},
    )


#oui
@router.get("/", status_code=status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
async def get_all_cast(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 2000,
):
    templates = request.app.state.templates

    # Récupérer tous les acteurs depuis la base de données
    casts = service_cast.get_all_cast(limit, db)

    # Trier les acteurs par ordre alphabétique
    sorted_casts = sorted(casts, key=lambda cast: cast.name)

    # Préparer les données pour le template
    cast_out_list = [CastOut.model_validate(cast) for cast in sorted_casts]

    # Rendre le template avec la liste des acteurs
    return templates.TemplateResponse(
        name="all_cast.html",
        request=request,
        context={"casts": cast_out_list},
    )



#non
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED , response_model=CastOut)
async def update_cast(id: UUID, title_film: str = None, c: CastIn = Depends(), db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service_cast.update_cast(id, title_film, c, db)
    

#non
@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED , response_model=CastIn)
async def delete_cast(id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service_cast.delete_cast(id, db)