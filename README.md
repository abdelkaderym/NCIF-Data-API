# NCIF AI-Based Data Integration Platform

## Overview
This project involves the development of a scalable platform for integrating data from multiple sources to support advanced analytics for stakeholders. The platform demonstrates:

1. **Data Integration**: Loading and integrating structured and unstructured data into a relational database.
2. **Data Analysis**: Extracting actionable insights from the data.
3. **API Development**: Providing secure, dynamic data access through an API.

---

## Features

### API Endpoints

#### 1. `/`
- **Description**: Home endpoint.
- **Response**:
  ```json
  {
    "message": "Welcome to the NCIF API. Use /tracts to get data or /predict for predictions."
  }
  ```

#### 2. `/tracts`
- **Description**: Fetch census tracts filtered by PM2.5 levels and branch density.
- **Query Parameters**:
  - `pm25_min` (float): Minimum PM2.5 level. Default is `5`.
  - `branches_min` (int): Minimum branch count. Default is `3`.
- **Example Request**:
  ```bash
  http://127.0.0.1:8000/tracts?pm25_min=10&branches_min=5
  ```
- **Example Response**:
  ```json
  [
    {
      "census_tract": 17031832300,
      "pm25": 14.739909,
      "total_branches": 8
    }
  ]
  ```

#### 3. `/predict`
- **Description**: Predict PM2.5 levels based on branch density.
- **Query Parameters**:
  - `branch_density` (int): Number of branches in a census tract.
- **Example Request**:
  ```bash
  http://127.0.0.1:8000/predict?branch_density=10
  ```
- **Example Response**:
  ```json
  {
    "branch_density": 10,
    "predicted_pm25": 7.0
  }
  ```

---

## Setup Instructions

### Prerequisites
1. **Python**: Version 3.8 or higher.
2. **Libraries**:
   - Install dependencies:
     ```bash
     pip install fastapi uvicorn pandas openpyxl
     ```
3. **Dataset**:
   - Ensure the file `20241125 Case Study for Position SE_Data.xlsx` is in the project directory.

### Steps
1. **Load Data**:
   Run the script to load data into the SQLite database:
   ```bash
   python load_data.py
   ```
   This will create `ncif_data.db` with the required tables.

2. **Start the API**:
   Launch the FastAPI server:
   ```bash
   python -m uvicorn main:app --reload
   ```

3. **Access the API**:
   - Home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Filtered Tracts: [http://127.0.0.1:8000/tracts?pm25_min=10&branches_min=5](http://127.0.0.1:8000/tracts?pm25_min=10&branches_min=5)
   - Predictions: [http://127.0.0.1:8000/predict?branch_density=10](http://127.0.0.1:8000/predict?branch_density=10)

---

## File Structure
```
NCIF Case Study/
|-- main.py          # API implementation
|-- load_data.py     # Script to load data into SQLite
|-- ncif_data.db     # SQLite database file (generated)
|-- README.md        # Documentation (this file)
|-- 20241125 Case Study for Position SE_Data.xlsx  # Dataset
```

---

## Assumptions
1. The `census_tract` field is consistent across datasets and serves as the primary key for joins.
2. PM2.5 data is represented by the `arithmetic_mean` column in the EPA dataset.
3. Branch data uses `NAMEBR` as the branch identifier in the SOD dataset.

---

## Future Enhancements
1. Deploy the API on a cloud platform (e.g., AWS, Azure, or Heroku).
2. Use a more sophisticated ML model for pollution predictions.
3. Add support for unstructured data integration.

---

