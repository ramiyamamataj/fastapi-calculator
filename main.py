import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app import operations

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("calculator_app")

app = FastAPI(title="FastAPI Calculator")
templates = Jinja2Templates(directory="templates")

class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: str

class CalculationResponse(BaseModel):
    result: float

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/calculate", response_model=CalculationResponse)
async def calculate(calc: CalculationRequest):
    logger.info(f"Received calculation: {calc.a} {calc.operation} {calc.b}")
    op = calc.operation.lower()
    try:
        if op == "add":
            res = operations.add(calc.a, calc.b)
        elif op == "subtract":
            res = operations.subtract(calc.a, calc.b)
        elif op == "multiply":
            res = operations.multiply(calc.a, calc.b)
        elif op == "divide":
            res = operations.divide(calc.a, calc.b)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        return CalculationResponse(result=res)
    except ValueError as e:
        logger.error(f"Calculation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# FastAPI Calculator application entrypoint
