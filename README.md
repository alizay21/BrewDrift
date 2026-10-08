# ☕ Brewdrift

> **Find your vibe. Find your café.**  
> *Brewdrift is a full-stack café discovery, recommendation, and personal coffee journaling platform built with Flutter and FastAPI.*

---

[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Riverpod](https://img.shields.io/badge/Riverpod-2.6-00599C)](https://riverpod.dev)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)](https://www.sqlalchemy.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Project Overview

**Brewdrift** is designed for coffee enthusiasts, remote workers, and digital nomads who care about more than just a cup of coffee—they care about the **vibe**. Whether you're looking for a quiet workspace with high-speed Wi-Fi and power outlets, or an artisanal espresso bar with a minimalist aesthetic, Brewdrift helps you discover, review, map, and journal your coffee experiences.

---

## ⚡ Current Project Status & Honest Notice

> [!IMPORTANT]
> **This project is fully built, structured, and ready to run!**  
> The **only missing configuration** is the insertion of your own **Google API Keys** (Google Maps API Key for the Flutter app and Google Places API Key for the FastAPI backend). 
> 
> Once you supply your valid keys in the respective `.env` configuration files, the application is **100% good to go!**  
> *(Note: The backend also supports a built-in mock mode (`USE_MOCK_PLACES=true`) so you can run and test the backend immediately even without a Google Places API key!)*

---

## ✨ Key Features

### 🔍 Vibe & Amenity Discovery
- **Aesthetic Filters**: Search cafés by ambiance—*Cozy, Minimalist, Work-Friendly, Industrial, Artisanal, or Outdoor*.
- **Amenity Preferences**: Filter places by Wi-Fi availability, seating capacity, power outlet access, noise levels, and coffee quality.
- **Real-Time Search**: Instant search and location proximity sorting.

### 🗺️ Interactive Google Maps Integration
- **Live Location Tracking**: View nearby cafés rendered directly on an interactive Google Map.
- **Custom Map Pin Markers**: Easily identify top-rated spots visually on the map.
- **Location Preview Cards**: Tap any pin to preview café ratings, vibe tags, distance, and quick actions.

### 📖 Personal Coffee Journal
- **Log Visits**: Save records of every café you visit.
- **Detailed Ratings**: Rate coffee quality, ambiance, service, and value.
- **Brew Tracking**: Track brew methods (*V60, Aeropress, Espresso, Cold Brew, Pour Over*), flavor notes, beans used, and price.
- **Photo Uploads**: Attach photos of your coffee and café setup directly to your journal entry.

### 📚 Curated Collections & Favorites
- **Custom Lists**: Create and manage personalized collections (e.g., *"Best Work Cafés with Fast Wi-Fi"*, *"Weekend Chill Spots"*).
- **Favorites**: One-tap bookmarking to quickly save your top spots.

### 🤖 Personalized Recommendation Engine
- Tailored café recommendations generated based on your selected vibe preferences and past visit history.

### 🔐 Auth & Security
- **JWT Authentication**: Full signup, login, refresh token rotation, and password reset flows.
- **Encrypted Local Storage**: Tokens securely stored on-device using Android Keystore / iOS Keychain (`flutter_secure_storage`).

### 🎨 Premium UI / UX
- Sleek **Dark Mode UI** tailored with Google Fonts typography (`Outfit` / `Inter`).
- Smooth micro-animations with `flutter_animate`, shimmer loading states, and responsive navigation via `go_router`.

---

## 🛠️ Tech Stack & Architecture

### 📱 Frontend (Mobile App)
| Technology | Description |
| :--- | :--- |
| **Framework** | [Flutter](https://flutter.dev) (Dart 3.x) |
| **State Management** | [Riverpod](https://riverpod.dev) (`flutter_riverpod`, `riverpod_annotation`) |
| **Routing** | [GoRouter](https://pub.dev/packages/go_router) |
| **Networking** | [Dio](https://pub.dev/packages/dio) with custom interceptors & error handling |
| **Maps & Location** | `google_maps_flutter`, `geolocator`, `permission_handler` |
| **Security & Storage** | `flutter_secure_storage`, `shared_preferences`, `flutter_dotenv` |
| **Code Generation** | `freezed`, `json_serializable`, `riverpod_generator`, `build_runner` |
| **UI & Animations** | `google_fonts`, `flutter_animate`, `shimmer`, `cached_network_image` |

### ⚙️ Backend (API Server)
| Technology | Description |
| :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com) (Python 3.11+, Async REST API) |
| **Database & ORM** | [SQLAlchemy 2.0 Async](https://www.sqlalchemy.org), [Alembic](https://alembic.sqlalchemy.org) (Migrations) |
| **Database Engines** | SQLite (`aiosqlite`) for dev, PostgreSQL (`asyncpg`) ready for prod |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev), `pydantic-settings` |
| **Security** | OAuth2 with Password Bearer, JWT (`python-jose`), Passlib with Bcrypt hashing |
| **External Integration** | Google Places API integration (`httpx` async client) with mock fallback mode |
| **File Storage** | Async file uploads (`aiofiles`, Pillow image processing) |
| **Testing** | `pytest`, `pytest-asyncio` |

---

## 📁 Repository Structure

```
brewdrift/
├── android/                   # Android native configuration & Manifest
├── assets/                    # App assets (icons, images)
├── backend/                   # FastAPI Backend Server
│   ├── app/
│   │   ├── api/               # API endpoints (auth, places, journal, collections, etc.)
│   │   ├── core/              # Security, config, JWT utilities
│   │   ├── database/          # Database session & models
│   │   ├── models/            # SQLAlchemy database schemas
│   │   ├── schemas/           # Pydantic data validation models
│   │   └── services/          # Business logic & Google Places integration
│   ├── migrations/            # Alembic database migration scripts
│   ├── brewdrift.db           # SQLite database (Development)
│   └── requirements.txt       # Python dependencies
├── lib/                       # Flutter Application Code (Feature-First Architecture)
│   ├── core/                  # Design system, themes, network client, routing, constants
│   ├── features/              # Modular features
│   │   ├── auth/              # Authentication & user sessions
│   │   ├── discovery/         # Café search & vibe filtering
│   │   ├── map/               # Google Maps integration & markers
│   │   ├── journal/           # Coffee visit journal entries & photo logs
│   │   ├── place_details/     # Detailed café views & reviews
│   │   ├── collections/       # Custom saved café lists
│   │   ├── favorites/         # Favorite places state
│   │   ├── profile/           # User stats & profile management
│   │   ├── onboarding/        # App walkthrough & vibe setup
│   │   └── settings/          # App settings & preferences
│   ├── shared/                # Shared widgets, models, & utilities
│   ├── app.dart               # Main App entry widget
│   └── main.dart              # Flutter main initialization
├── .env                       # Flutter environment variables (API URL & Google Maps key)
└── pubspec.yaml               # Flutter package configuration
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites
- **Flutter SDK**: `^3.12.0` or higher
- **Python**: `3.10` or higher
- **Google Cloud Platform Account** (For Google Maps & Places API Keys)

---

### 2️⃣ Backend Setup (FastAPI)

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a Python virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Backend Environment (`.env`)**:
   Copy `.env.example` to `.env` inside the `backend` directory:
   ```bash
   cp .env.example .env
   ```
   Open `backend/.env` and configure:
   ```env
   API_BASE_URL=http://localhost:8000
   DATABASE_URL=sqlite+aiosqlite:///./brewdrift.db
   JWT_SECRET=your-secure-jwt-secret-key
   
   # Add your Google Places API Key here:
   GOOGLE_PLACES_API_KEY=YOUR_GOOGLE_PLACES_API_KEY_HERE
   # Set to true to test without a live Places key:
   USE_MOCK_PLACES=false
   ```

5. **Run Database Migrations & Start Server**:
   ```bash
   alembic upgrade head
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The backend API will be available at `http://localhost:8000`. You can inspect interactive API documentation at `http://localhost:8000/docs`.

---

### 3️⃣ Frontend Setup (Flutter Mobile App)

1. **Navigate back to the project root**:
   ```bash
   cd ..
   ```

2. **Install Flutter packages**:
   ```bash
   flutter pub get
   ```

3. **Configure Mobile Environment (`.env`)**:
   Open or create `.env` in the root folder:
   ```env
   # Backend API URL (Use 10.0.2.2 for Android Emulator, or local IP for physical device)
   API_BASE_URL=http://10.0.2.2:8000
   
   # Add your Google Maps Android API Key here:
   GOOGLE_MAPS_ANDROID_API_KEY=YOUR_GOOGLE_MAPS_ANDROID_API_KEY_HERE
   ```

4. **Run the App**:
   ```bash
   flutter run
   ```

---

## 🔑 Required API Keys Summary

| Key Name | Location | Purpose |
| :--- | :--- | :--- |
| **`GOOGLE_MAPS_ANDROID_API_KEY`** | Root `.env` | Renders interactive maps and pin markers in the Flutter Android app. |
| **`GOOGLE_PLACES_API_KEY`** | `backend/.env` | Powers real-world café search, details, photos, and autocomplete in FastAPI backend. |

> *(Note: You can generate both keys in your [Google Cloud Console](https://console.cloud.google.com/) under **APIs & Services** by enabling **Maps SDK for Android** and **Places API**).*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
