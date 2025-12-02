# Santa Wishing Machine

A personalized video message generator from Santa, built with a React frontend and a Python (FastAPI) backend.

## Structure

- `backend/`: Python FastAPI backend that handles transcript generation and API logic.
- `frontend/`: React frontend (Vite) for Web.

## Prerequisites

- Python 3.8+
- Node.js & npm
- (Optional) Virtualenv

## Getting Started

### Backend (Python)

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the backend server:
    ```bash
    python3 main.py
    ```
    The backend will be available at `http://localhost:8000`.

### Frontend (React)

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the application:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## Testing

### Backend

You can test the backend API using `curl`:

```bash
curl -X POST http://localhost:8000/generate-transcript \
-H "Content-Type: application/json" \
-d '{"name": "Alex", "gifts": "bike"}'
```

### Frontend

The frontend should connect to the backend automatically via the Vite proxy.
