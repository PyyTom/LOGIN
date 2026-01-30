# LOGIN App – Python + Flet + SQLite

A graphical desktop application built with **Python**, **Flet**, and **SQLite**.  
It provides a simple user management system with **registration**, **login**, and **unregistration**, storing passwords securely using **SHA‑256 hashing**.

---

## 🚀 Features

- Modern UI built with **Flet**
- Local SQLite database (`db.db`)
- Automatic creation of the `USERS(USER, PWD)` table
- Passwords stored as SHA‑256 hashes
- Three main actions:
  - LOGIN
  - REGISTER
  - UNREGISTER
- Light/Dark theme switch
- Visual alerts using `AlertDialog`

---

## 📦 Installation

Install dependencies:

```bash
pip install -r requirements.txt


## Project Structure

project/
│── LOGIN.py
│── db.db # auto-created
│── requirements.txt
│── .gitignore
│── LICENSE
└── README.md

