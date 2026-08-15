# Backend setup 

## Virtual Environment

Create a virtual environment:

```powershell
python -m venv venv

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1

## Install Dependencies

Install the required packages:

```powershell
pip install -r requirements.txt

## Run the Server

Start the FastAPI development server:

```powershell
python -m uvicorn main:app --reload
