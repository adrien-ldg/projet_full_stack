from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["autres"])

@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def home(request: Request):
    try:
        templates = request.app.state.templates
        return templates.TemplateResponse(name="home.html", request=request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
