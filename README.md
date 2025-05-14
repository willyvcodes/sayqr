# SayQR 📱

A modern web application that allows users to create custom pages with text and images, then instantly share them via QR codes. Perfect for events, classrooms, restaurants, or anywhere you need to share information quickly and elegantly.

![SayQR Demo]()

## ✨ Features

- 🔐 **Secure Authentication** - User registration and login with JWT tokens
- 📝 **Rich Page Creation** - Create pages with custom text and multiple images
- 🖼️ **Smart Image Handling** - Automatic image compression and optimization
- 📱 **QR Code Generation** - Instant QR codes for easy mobile sharing
- 👤 **User Dashboard** - Manage all your created pages in one place
- ✏️ **Edit & Delete** - Full control over your content
- 🎨 **Modern UI** - Beautiful, responsive design with dark theme
- ⚡ **Fast & Responsive** - Optimized for all devices and screen sizes

## 🚀 Live Demo

- **Frontend**: [Coming Soon]
- **Backend API**: [worldwide-ardelle-willyv-aa70260a.koyeb.app/] [with https://www.koyeb.com/]

## 🛠️ Tech Stack

### Frontend
- **SvelteKit** - Modern, fast web framework
- **Skeleton UI** - Component library with beautiful animations
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Lightning-fast build tool
- **browser-image-compression** - Client-side image optimization

### Backend
- **FastAPI** - High-performance Python web framework
- **MongoDB** - NoSQL database for flexibility
- **Beanie** - Async MongoDB ODM
- **FastAPI Users** - Complete authentication system
- **JWT** - Secure token-based authentication
- **Uvicorn** - ASGI server for production

## 📦 Installation

### Prerequisites
- **Node.js** 18.0.0 or higher
- **Python** 3.11 or higher
- **MongoDB** database (local or cloud)

### 1. Clone the Repository
```bash
git clone https://github.com/willyvcodes/sayqr.git
cd sayqr
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file for the backend
touch .env
```

Edit `.env` with your configuration:
```env
MONGO_URI=mongodb+srv://myuser:mypass@cluster.mongodb.net/sayqr?retryWrites=true&w=majority
JWT_SECRET=your-256-bit-secret-key-goes-here
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create environment file for the frontend
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
```

## 🏃‍♂️ Running the Application

### Start the Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```The API will be available at `http://localhost:8000`

### Start the Frontend
```bash
cd frontend
npm run dev
```
The app will be available at `http://localhost:5173`

Have fun!

<div align="center">
Made with ❤️ by <a href="https://github.com/willyvcodese">William Valido</a>
</div>

I built this because I was tired of sharing long URLs at events. Now I just generate a QR code and boom - people can scan and go.
