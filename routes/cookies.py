from fastapi import APIRouter, Response, Cookie,Request

cookie_router = APIRouter(prefix="/cookies", tags=["Cookies"])


@cookie_router.post("/set")
async def set_cookie(customer_name : str , response: Response):
    response.set_cookie(
        key="customer_name",
        value=customer_name,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600
    )

    return {"message": "Cookie created successfully"}



@cookie_router.get("/read")
async def read_cookie(request: Request):
    invoice_user = request.cookies.get("customer_name")
    return {"customer_name": invoice_user}


@cookie_router.delete("/delete")
async def delete_cookie(response: Response):
    response.delete_cookie(key="customer_name")

    return {"message": "Cookie deleted successfully"}
