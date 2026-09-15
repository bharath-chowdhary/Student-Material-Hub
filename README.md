# Student-Material-Hub
A centralized academic resource platform featuring role-based upload governance and integrated Gemini AI for instant, in-browser document querying.
## ⚡ Core Features

* **Role-Based Access (RBAC):** Max 5 verified Class Representatives (CRs) per section can upload materials to prevent spam.
* **Structured Hierarchy:** Organizes study materials logically by **Section → Subject → Material**.
* **In-App Gemini AI:** Summarize and query uploaded PDFs directly in the browser without downloading files.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5 |
| **Backend** | Python, Django, Google Gemini API |
| **Database** | MySQL |

---

## 🚀 Quick Start

1. **Clone & Navigate:**
   ```bash
   git clone [https://github.com/your-username/student-material-hub.git](https://github.com/your-username/student-material-hub.git)
   cd student-material-hub
Setup Virtual Environment:

2. Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure Environment (.env):

3. Code snippet
SECRET_KEY=your_django_secret_key
DEBUG=True
DB_NAME=student_material_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
GEMINI_API_KEY=your_gemini_api_key
Migrate & Run:

4. Bash
python manage.py migrate
python manage.py runserver
