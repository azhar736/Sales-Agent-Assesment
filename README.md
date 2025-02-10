# AI Sales Assistant

An AI-powered sales assistant that leverages machine learning to analyze products and generate effective sales strategies.

## Project Overview

The AI Sales Assistant is a full-stack application that helps sales teams analyze products, understand market positioning, and generate data-driven sales strategies. It combines modern web technologies with AI to provide actionable insights.

### Key Features

- Product and company analysis
- Market positioning insights
- Competitive analysis
- Sales strategy recommendations
- Document processing support
- Real-time analysis feedback

## Technical Stack & Justification

### Backend

- **FastAPI**: Chosen for high performance, async support, and automatic API documentation
- **Pydantic**: Provides robust data validation and serialization
- **OpenAI Integration**: Leverages advanced language models for analysis
- **Python 3.8+**: Offers strong ML/AI library support

### Frontend

- **Next.js 13+**: Provides excellent developer experience and performance
- **TypeScript**: Ensures type safety and better code maintainability
- **TailwindCSS**: Enables rapid UI development with utility-first approach
- **React Hook Form**: Offers efficient form handling with validation

## Architecture Overview

```
  ├── backend/
  │   ├── models/          # Data models and schemas
  │   ├── services/        # Business logic and AI integration
  │   ├── main.py         # FastAPI application
  │   └── requirements.txt # Python dependencies
  └── frontend/
      ├── src/
      │   ├── components/  # React components
      │   ├── lib/         # Utilities and API clients
      │   └── app/         # Next.js pages and routing
      └── package.json     # Node.js dependencies
```

## Project Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn
- OpenAI API key

### Backend Setup

1. Navigate to backend directory:

   ```bash
   cd backend
   ```

2. Create and activate virtual environment:

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   ```bash
   # Copy example env file
   cp .env.example .env

   # Rename and configure environment variables
   mv .env.example .env

   # Edit .env file with your OpenAI API key and other settings:
   OPENAI_API_KEY=your_api_key_here
   HOST=localhost
   PORT=8000
   ENV=development
   FRONTEND_URL=http://localhost:3000
   LOG_LEVEL=INFO
   ```

5. Run the backend server:

   ```bash
   # Development with auto-reload
   uvicorn main:app --reload

   # The API will be available at http://localhost:8000
   # API documentation at http://localhost:8000/docs
   ```

### Frontend Setup

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   # Using npm
   npm install

   # Or using yarn
   yarn install
   ```

3. Configure environment variables:

   ```bash
   # Create .env.local file
   touch .env.local

   # Add the following variables
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Run the development server:

   ```bash
   # Using npm
   npm run dev

   # Or using yarn
   yarn dev

   # The app will be available at http://localhost:3000
   ```

### Testing the Application

1. Ensure both backend and frontend are running
2. Open http://localhost:3000 in your browser
3. Fill out the product analysis form:
   - Product Name
   - Product Description
   - Price
   - Company URL
   - Optional: Competitors
   - Optional: Additional Notes
   - Optional: Supporting Document
4. Submit the form to receive AI-generated analysis

### Common Issues & Solutions

1. Backend Connection Error:

   - Verify backend is running on port 8000
   - Check CORS settings in backend/main.py

2. OpenAI API Error:

   - Verify API key in .env file
   - Check API key permissions and quota

3. File Upload Issues:
   - Check file size (max 10MB)
   - Verify supported file types
