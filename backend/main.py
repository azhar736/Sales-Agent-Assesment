from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import logging
from models.request_models import AnalysisRequest
from services.analysis_service import AnalysisService

from models.company import Company
from models.product import Product
from models.analysis import Analysis

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sales Assistant API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
analysis_service = AnalysisService()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/analyze", status_code=status.HTTP_200_OK)
async def analyze_product(
    productName: str = Form(),
    productDescription: str = Form(),
    price: float = Form(),
    companyUrl: str = Form(),
    competitors: Optional[str] = Form(None),
    additionalNotes: Optional[str] = Form(None),
    file: Optional[UploadFile] = None,
) -> Dict[str, Any]:
    """
    Analyze product and company data to generate sales insights.
    """
    try:
        logger.info(f"Received analysis request for product: {productName}")

        # Validate and prepare analysis data
        analysis_data = {
            "productName": productName.strip(),
            "productDescription": productDescription.strip(),
            "price": float(price),
            "companyUrl": companyUrl.strip(),
        }

        # Add optional fields only if they exist
        if competitors:
            analysis_data["competitors"] = competitors.strip()
        if additionalNotes:
            analysis_data["additionalNotes"] = additionalNotes.strip()

        # Process file if provided
        file_content = None
        if file and hasattr(file, "filename") and file.filename:
            try:
                file_content = await file.read()
                logger.info(f"Processed file: {file.filename}")
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error processing uploaded file",
                )

        # Perform analysis
        results = await analysis_service.analyze(analysis_data, file_content)
        logger.info("Analysis completed successfully")
        return results

    except ValidationError as e:
        logger.error(f"Request validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
    finally:
        if file and hasattr(file, "file"):
            await file.close()


@app.post("/api/process-document")
async def process_document(document: bytes):
    """Process and analyze a document"""
    try:
        # Implement document processing logic
        pass
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom exception handler for HTTP exceptions"""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
