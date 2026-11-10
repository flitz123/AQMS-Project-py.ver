# Automated Queue Management System

A complete Flask web application for registering patients, generating queue tickets, calling the next patient, tracking service status, and reviewing daily activity.

## Run locally

```powershell
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000`.

## Vercel deployment

1. Push this repository to GitHub.
2. Import the repository in Vercel.
3. Vercel will detect the Python entry point through `vercel.json`.
4. Deploy without additional environment variables.

Data is persisted in `data/patients.csv`.

## CLI mode

```powershell
py main.py
```