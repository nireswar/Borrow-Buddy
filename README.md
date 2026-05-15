BorrowBuddy is a peer-to-peer rental platform that allows individuals to rent out their unused items and borrow what they need from others nearby. This project aims to build a circular, cost-effective economy where resources are reused rather than wasted.

🚀 Features
User Authentication: Secure login and signup powered by Firebase Auth.

Item Listings: Users can list items with titles, descriptions, categories, pricing, and images.

Dynamic Marketplace: A real-time "Buy" page that fetches available items directly from Google Firestore.

Image Management: Local image uploading and handling via Flask and werkzeug.

Rental Requests: Integrated "Request to Rent" system to notify owners.

Secure Contact: WhatsApp integration that allows verified (logged-in) users to contact owners directly.

🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML5, CSS3 (Custom Responsive Design), JavaScript (ES6 Modules)

Database: Google Firebase Firestore

Authentication: Firebase Auth

File Storage: Local Static Uploads

📂 Folder Structure
Plaintext
BorrowBuddy/
│
├── app.py              # Main Flask application & Backend Logic
├── static/
│   └── uploads/        # Directory where item images are stored
├── templates/          # HTML Templates
│   ├── index.html      # Landing Page
│   ├── login.html      # Login Page
│   ├── signup.html     # Registration Page
│   ├── buy.html        # Marketplace / Browse Items
│   ├── sell.html       # Item Listing Form
│   ├── item.html       # Detailed Item View
│   └── howitworks.html # Platform Guide
└── requirements.txt    # Python dependencies
⚙️ Setup & Installation
1. Clone the repository
Bash
git clone https://github.com/your-username/borrowbuddy.git
cd borrowbuddy
2. Install dependencies
Bash
pip install flask firebase-admin werkzeug
3. Firebase Configuration
Create a project in the Firebase Console.

Download your Service Account Key (JSON file).

Rename it or update the filename in app.py:

Python
cred = credentials.Certificate("your-firebase-adminsdk-key.json")
Update the firebaseConfig object in your HTML files (login.html, signup.html, sell.html, etc.) with your web app credentials.

4. Set Secret Key
Create an environment variable for your Flask secret key or use the default for development:

Bash
export FLASK_SECRET_KEY="your-secret-key"
5. Run the application
Bash
python app.py
The app will be available at http://127.0.0.1:5000/.

📸 Screenshots
(Pro-tip: Add some screenshots of your UI here to make your GitHub profile pop!)

🛡️ License
Distributed under the MIT License. See LICENSE for more information.
