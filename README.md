# AI EMAIL ANALYZER ⚡

A Full-Stack web application for automated email classification, developed as a technical challenge for AutoU. The app uses AI to categorize emails and suggest appropriate responses.

**Access the live application:** [**PASTE YOUR RENDER APP URL HERE**]

---

![Dashboard Screen](https://via.placeholder.com/800x450.png/1e1e1e/00aaff?text=Screenshot+of+Dashboard)
*Main dashboard showing the AI analysis result.*

---

## 🚀 About The Project

This project was developed as a complete solution to automate the classification of high-volume emails. The application allows users to submit email content (via text or file upload) and receive an AI-powered classification ("Productive" or "Unproductive") along with a suggested response.

## ✨ Features

*   **AI-Powered Classification:** Utilizes OpenAI's GPT-3.5 model to analyze and categorize email content with high accuracy.
*   **Text and File Processing:** Supports direct text input and file uploads (`.txt`, `.pdf`).
*   **Natural Language Processing (NLP):** Implements a preprocessing pipeline with NLTK for text cleaning, stop-word removal, and lemmatization.
*   **Modern & Reactive UI:** A sleek, dark-themed Single-Page Application (SPA) built with React and styled with Tailwind CSS.
*   **Robust Backend:** A layered and tested API built with Python and FastAPI.

## 🧪 Testing

The backend is covered by a suite of **unit and integration tests** written with **Pytest**.
*   **Unit Tests:** Isolate and verify the logic of the `nlp_service`, mocking external API calls to ensure predictable behavior.
*   **Integration Tests:** Test the FastAPI routes using `TestClient`, simulating file uploads and text submissions to validate the complete request-response cycle and error handling.

## 🛠️ Tech Stack

This project is a monorepo integrating a Python backend with a React frontend.

#### **Backend (API)**
*   **Python 3.12**
*   **FastAPI:** For building the RESTful API.
*   **OpenAI API:** For AI-based classification.
*   **NLTK:** For the NLP preprocessing pipeline.
*   **PyPDF:** For PDF text extraction.
*   **Pytest:** For unit and integration testing.

#### **Frontend**
*   **React.js 18** & **Vite**
*   **Tailwind CSS:** For utility-first styling.

#### **Deployment**
*   **Render:** For hosting the Web Service (Backend) and Static Site (Frontend).
*   **Git & GitHub:** For version control and CI/CD.

---

## ⚙️ Running The Project Locally

Follow the steps below to set up and run the application in your development environment.

### Prerequisites
*   **Python** (version 3.8 or higher)
*   **Node.js** and **npm**

### Backend

1.  **Navigate to the backend folder:**
    ```bash
    cd backend
    ```
2.  **Create and activate the virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/Scripts/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file** in the `backend` folder and add your API key:
    ```
    OPENAI_API_KEY="sk-..."
    ```
5.  **Run the tests (Optional):**
    ```bash
    pytest
    ```
6.  **Start the backend server:**
    ```bash
    uvicorn main:app --reload
    ```

### Frontend

1.  **Navigate to the frontend folder:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the frontend server:**
    ```bash
    npm run dev
    ```

---

## Author

**Gabriel Corrêa**

*   **GitHub:** [@correagss](https://github.com/correagss)
*   **LinkedIn:** [Your LinkedIn URL here]