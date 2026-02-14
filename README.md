# 🎓 College URL Validator API

A FastAPI-based backend service to validate university / college website domains.

This API performs:

- ✅ Domain format validation  
- ✅ DNS resolution check  
- ✅ Website title extraction  
- ✅ Fuzzy matching between college name and website title  
- ✅ Confidence scoring  

---

## 🚀 Tech Stack

- Python 3.10+
- FastAPI
- Requests
- BeautifulSoup4
- RapidFuzz
- Uvicorn

---

## 📂 Project Structure

college-url-validator/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore




---

## 🧠 Validation Logic

The API validates a college website in 3 stages:

### 1️⃣ Format Validation
Checks if the provided domain has a valid structure.

### 2️⃣ DNS Validation
Uses `socket.gethostbyname()` to confirm that the domain exists.

### 3️⃣ Title Matching
- Fetches the homepage
- Extracts the `<title>` tag
- Compares it with the provided college name
- Uses fuzzy matching (RapidFuzz)
- Returns a similarity score (0–100)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/college-url-validator.git
cd college-url-validator




2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate


(Windows)

venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Server
uvicorn main:app --host 0.0.0.0 --port 8000


API will be available at:

http://localhost:8000


Swagger Docs:

http://localhost:8000/docs

🌐 API Endpoint
GET /validate
Query Parameters
Parameter	Type	Required	Description
college_name	string	✅ Yes	Full official college name
domain	string	✅ Yes	College website domain or full URL
🧪 Example Request
GET /validate?college_name=Visvesvaraya%20National%20Institute%20of%20Technology&domain=vnit.ac.in


Full URL:

http://localhost:8000/validate?college_name=VNIT&domain=vnit.ac.in

📦 Example Response
{
  "isValid": true,
  "workingURL": "https://vnit.ac.in",
  "title": "Visvesvaraya National Institute of Technology, Nagpur",
  "similarity_score": 82,
  "checks": {
    "format": true,
    "dns": true,
    "name_match": true
  },
  "warnings": [],
  "errors": []
}



| Field             | Description                          |
| ----------------- | ------------------------------------ |
| isValid           | True if domain exists (DNS verified) |
| workingURL        | URL that responded successfully      |
| title             | Extracted `<title>` from homepage    |
| similarity_score  | Fuzzy match confidence (0–100)       |
| checks.format     | Domain format validation result      |
| checks.dns        | DNS resolution result                |
| checks.name_match | Title-name similarity validation     |
| warnings          | Non-blocking validation warnings     |
| errors            | Blocking validation errors           |

