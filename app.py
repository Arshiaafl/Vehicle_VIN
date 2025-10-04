import os
import json
import pandas as pd
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from google import genai

# --- Load Environment ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

CSV_FILE = "sample_data.csv"

# --- FastAPI setup ---
app = FastAPI(title="VIN Report API")
templates = Jinja2Templates(directory="templates")

# --- Core LLM logic ---
def vin_look(vin: str):
    df = pd.read_csv(CSV_FILE, dtype=str)
    vehicle = df[df["VIN"] == vin]
    if vehicle.empty:
        raise ValueError(f"VIN {vin} not found in Database.")
    vehicle_data = vehicle.iloc[0].to_dict()

    prompt = f"""
    You are an expert automotive analyst.

    Given the following vehicle data, generate a JSON with:
    - summary: a short, human-readable summary of the vehicle's market position.
    - risk_score: a numerical score from 1-10 (1 being low risk, 10 being high risk) based on metrics like days_on_lot, price_to_market, vdp_views, etc.
    - reasoning: A clear, concise explanation for the assigned risk score

    Rules:
    1. Only output valid JSON (no extra text, no markdown).
    2. Keep it concise.
    3. Treat all CSV values as strings.

    Vehicle Data: {json.dumps(vehicle_data)}
    """

    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    llm_output = response.text.strip()
    if llm_output.startswith("```"):
        llm_output = llm_output.strip("`")
        if llm_output.lower().startswith("json"):
            llm_output = llm_output[4:].strip()

    try:
        report = json.loads(llm_output)
    except json.JSONDecodeError:
        report = {"summary": llm_output, "risk_score": None, "reasoning": None}

    return report

# --- REST endpoint ---
@app.get("/vin/{vin}")
def get_vin_report(vin: str):
   
    try:
        return vin_look(vin)
    except Exception as e:
        return {"error": str(e)}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    html = """
    <html>
        <head>
            <title>VIN Report Generator</title>
        </head>
        <body style="font-family: sans-serif; padding: 40px;">
            <h2>🚗 VIN Report Generator</h2>
            <form action="/analyze" method="post">
                <input type="text" name="vin" placeholder="Enter VIN" style="width:300px; padding:5px" required>
                <button type="submit" style="padding:5px 10px;">Generate</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, vin: str = Form(...)):
    try:
        report = vin_look(vin)
        return HTMLResponse(f"""
            <h3>Report for VIN {vin}</h3>
            <pre>{json.dumps(report, indent=2)}</pre>
            <a href="/">Back</a>
        """)
    except Exception as e:
        return HTMLResponse(f"<h3>Error:</h3><pre>{str(e)}</pre><a href='/'>Back</a>")

