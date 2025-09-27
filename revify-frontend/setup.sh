# Revify Frontend Setup Script

echo "🚀 Setting up Revify Frontend..."

# Navigate to frontend directory
cd revify-frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Check if backend is running
echo "🔍 Checking backend connection..."
curl -s http://localhost:5000/api/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend is running!"
else
    echo "⚠️  Backend is not running. Please start the Revify backend server."
    echo "   Navigate to the revify_flow directory and run:"
    echo "   python src/revify_flow/api.py"
fi

# Start development server
echo "🌟 Starting development server..."
echo "Frontend will be available at: http://localhost:3000"
npm run dev