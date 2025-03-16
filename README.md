# MCP Server

Mission Control Panel (MCP) Server - A backend service for managing and monitoring mission-critical operations.

## Features

- User authentication and authorization
- Mission control and monitoring
- Real-time status updates
- Secure API endpoints
- Database integration

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/mcp_db
SECRET_KEY=your-secret-key
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc` 