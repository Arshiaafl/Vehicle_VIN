# VIN Report API

A FastAPI application that generates vehicle market reports and risk scores using Google Gemini LLM. Users can query via REST API or use a simple web form.

---

## Features

- Generate vehicle market summaries and risk scores based on CSV data.
- REST API endpoint: `/vin/{vin}`
- Fully containerized with Docker.

---

## Requirements

- Docker
- `.env` file containing your Gemini API key:

```

GEMINI_API_KEY=your_api_key_here

````

- `sample_data.csv` with vehicle data including `VIN` column.

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/Arshiaafl/Vehicle_VIN
````

2. **Ensure `.env` and `sample_data.csv` are in the project root**

```
.env
sample_data.csv
```

3. **Build the Docker image**

```bash
docker build -t vin-report-app .
```

4. **Run the container**

```bash
docker run -d -p 8000:8000 --env-file .env vin-report-app  
```

5. **Access the application**

* Web form: [http://localhost:8000/](http://localhost:8000/)
* REST API: [http://localhost:8000/vin/{VIN}](http://localhost:8000/vin/YOUR_VIN_HERE)

---

## API Endpoints

| Method | Endpoint     | Description                    |
| ------ | ------------ | ------------------------------ |
| GET    | `/vin/{vin}` | Returns JSON report for a VIN  |
| GET    | `/`          | Simple HTML form for VIN input |
| POST   | `/analyze`   | Form submission endpoint       |

---

## Project Structure

```
vin-report-api/
├─ app.py
├─ requirements.txt
├─ sample_data.csv
├─ .env
├─ Dockerfile
└─ templates/
```

* `app.py` → main FastAPI application
* `requirements.txt` → Python dependencies
* `sample_data.csv` → vehicle database
* `.env` → Gemini API key
* `templates/` → optional Jinja2 templates

---

## Notes

* Make sure your Gemini API key is valid in `.env`.
* Ensure the CSV has a `VIN` column matching user input.
* Docker mounts are used so `.env` and `sample_data.csv` are read inside the container.

---




