# 🚀 MedAi – AI Powered Healthcare Prediction System

![MedAi Banner](https://img.shields.io/badge/MedAi-Medical%20AI%20System-blueviolet?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.2.0-61dafb?style=flat-square\&logo=react)
![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square\&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> **An advanced AI-driven medical prediction platform built using Python (Flask), Machine Learning, and a modern React + 3D frontend.**

---

## 🌟 Overview

**MedAi** is a full-stack AI healthcare platform designed to predict:

* 🦟 **Dengue Risk Level**
* 🫘 **Kidney Disease Probability**
* 🧠 **Mental Health / Stress Assessment**

The system features a **3D animated UI**, bilingual support (English & Bangla), ML models trained on real datasets, and a secure Flask API.

---

## 📁 Project Structure

```
MedAi-app/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── api_endpoints.py
│   ├── training_pipeline.py
│   ├── database.py
│   ├── models/
│   ├── datasets/
│   ├── logs/
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── api/
│   │   ├── store/
│   │   ├── i18n/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env.example
│
└── README.md
```

---

## 🛠 Tech Stack

### **Frontend**

* React 18, React Router
* Tailwind CSS
* Framer Motion animations
* Three.js + React Three Fiber (3D UI)
* Zustand
* i18next (Bangla/English translation)
* Axios

### **Backend**

* Python 3.8+
* Flask API
* Scikit-learn, NumPy, Pandas
* SQLAlchemy ORM
* SQLite / PostgreSQL

---

## 💻 Installation

### **Prerequisites**

* Python 3.8+
* Node.js 14+
* Git

---

## ⚙️ Backend Setup (Flask API)

```bash
git clone https://github.com/SazzadHossain1461/MedAi-app.git
cd MedAi-app/backend
```

### Create Virtual Environment

```bash
python -m venv env
env\Scripts\activate   # Windows

# Linux / macOS
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```bash
cp .env.example .env
```

### Train All Models (Required First Time)

```bash
python main.py train-all
```

---

## 🎨 Frontend Setup

```bash
cd ../frontend
npm install --legacy-peer-deps
cp .env.example .env
```

### Update Environment File

```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
```

---

## 🚀 Running the Application

### **Start Backend**

```bash
cd backend
python main.py api
```

Runs on → `http://localhost:5000`

### **Start Frontend**

```bash
cd frontend
npm start
```

Runs on → `http://localhost:3000`

---

## 📡 API Endpoints

### **Dengue Prediction**

`POST /api/dengue/predict`

### **Kidney Disease Prediction**

`POST /api/kidney/predict`

### **Mental Health Assessment**

`POST /api/mental-health/assessment`

### **Health Check**

`GET /api/health`

*(Full examples are included above.)*

---

## ⚙️ Model Performance

| Model         | Accuracy | Precision | Recall |
| ------------- | -------- | --------- | ------ |
| Dengue        | 96.8%    | 0.95      | 0.97   |
| Kidney        | 94.2%    | 0.93      | 0.94   |
| Mental Health | 92.1%    | 0.91      | 0.92   |

---

## 🔧 Troubleshooting

### **Backend not connecting**

* Ensure Flask is running
* Check `REACT_APP_API_URL` in `.env`
* Disable Windows firewall for local testing

### **3D animations not loading**

* Check browser WebGL support
* Try Firefox/Chrome
* Inspect console logs

### **Model not trained**

```bash
python main.py train-all
```

---

## 📚 Documentation Links

* `/backend/README.md`
* `/frontend/README.md`
* `/docs/API.md`

---

## 🤝 Contributing

We welcome contributions!
Please read:

* `CONTRIBUTING.md`
* `CODE_OF_CONDUCT.md`

Steps:

```bash
git checkout -b feature/my-feature
git commit -m "Add new feature"
git push origin feature/my-feature
```

---

## 📝 License

This project is licensed under the **MIT License**.

---

## 📞 Support

📧 Email: **[sazzadhossain74274@gmail.com](mailto:sazzadhossain74274@gmail.com)**

🔗 LinkedIn: [https://www.linkedin.com/in/sazzadhossain1461/](https://www.linkedin.com/in/sazzadhossain1461/)

💻 GitHub: [https://github.com/SazzadHossain1461](https://github.com/SazzadHossain1461)

---

## ⭐ Star the Repository

If this project helped you, **please give it a star!** ⭐
It motivates future development.

---

## 📸 Screenshots

**Dashboard**

<img width="1891" height="924" alt="Screenshot (584)" src="https://github.com/user-attachments/assets/e3acf901-ce57-4fff-a290-c72f13973807" />


**Bangla Dashboard**

<img width="1898" height="926" alt="Screenshot (588)" src="https://github.com/user-attachments/assets/a8d508ec-a4c3-4820-99c5-74c3ba78f3cf" />


**Dengue Risk Prediction**

<img width="1899" height="929" alt="Screenshot (585)" src="https://github.com/user-attachments/assets/0f99a6fa-5fea-453a-a411-b19af9350f5e" />


**Kidney Dieases Prediction**

<img width="1898" height="915" alt="Screenshot (586)" src="https://github.com/user-attachments/assets/dcf515ea-ea14-4636-89d6-6642e5b13a24" />


**Mental Health Assesment**

<img width="1891" height="923" alt="Screenshot (587)" src="https://github.com/user-attachments/assets/78a551f9-7386-4927-8fdf-011f68dc7979" />


---
                                                                                          
###Made with ❤️ for better healthcare
