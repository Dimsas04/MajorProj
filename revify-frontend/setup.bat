@echo off
echo 🚀 Setting up Revify Frontend...

cd revify-frontend

echo 📦 Installing dependencies...
npm install

echo 🔍 Checking backend connection...
curl -s http://localhost:5000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is running!
) else (
    echo ⚠️  Backend is not running. Please start the Revify backend server.
    echo    Navigate to the revify_flow directory and run:
    echo    python src/revify_flow/api.py
)

echo 🌟 Starting development server...
echo Frontend will be available at: http://localhost:3000
npm run dev