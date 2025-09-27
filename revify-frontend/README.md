# Revify Frontend

A stunning, modern React.js frontend for the Revify AI-powered product review analysis system.

## 🚀 Features

- **Beautiful UI/UX**: Modern design with smooth animations and transitions using Framer Motion
- **Real-time Progress Tracking**: Live updates during analysis with beautiful progress indicators
- **Interactive Data Visualization**: Charts and graphs using Recharts for sentiment analysis
- **Responsive Design**: Fully responsive across all devices
- **Professional Animations**: Smooth page transitions and micro-interactions
- **Real-time API Integration**: Seamless communication with Revify backend API

## 🛠 Tech Stack

- **React 18** - Modern React with hooks and latest features
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework for rapid styling
- **Framer Motion** - Production-ready motion library for React
- **Heroicons** - Beautiful hand-crafted SVG icons
- **Recharts** - Composable charting library for React
- **Axios** - Promise-based HTTP client
- **React Router** - Declarative routing for React

## 📦 Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd revify-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

## 🔧 Configuration

### API Configuration

The frontend connects to the Revify backend API. Make sure your backend server is running on `http://localhost:5000`.

To change the API base URL, edit `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## 📱 Pages Overview

### 🏠 Home Page (`/`)
- Hero section with product URL input
- Feature showcase with animations
- How it works section
- Call-to-action sections

### ⚡ Analysis Page (`/analysis`)
- Real-time progress tracking
- Step-by-step analysis visualization
- Animated progress indicators
- Fun facts during processing

### 📊 Results Page (`/results`)
- Comprehensive analysis results
- Interactive data visualizations
- Sentiment analysis charts
- Feature-by-feature breakdown
- Download and share functionality

## 🎨 Design System

### Color Palette
- **Primary**: Blue gradient (`from-blue-600 to-blue-700`)
- **Secondary**: Purple gradient (`from-purple-600 to-purple-700`)
- **Accent**: Pink gradient (`from-pink-600 to-pink-700`)
- **Success**: Green (`text-green-600`)
- **Warning**: Yellow (`text-yellow-600`)
- **Error**: Red (`text-red-600`)

### Typography
- **Font Family**: Inter (from Google Fonts)
- **Headings**: Bold, various sizes with gradient text effects
- **Body**: Regular weight with proper line spacing

### Animations
- **Page Transitions**: Fade and slide effects
- **Micro-interactions**: Hover states, button animations
- **Progress Indicators**: Smooth progress bars and loading states
- **Data Visualization**: Animated charts and counters

## 🔌 API Integration

The frontend communicates with the Revify backend through these endpoints:

- `GET /api/health` - Health check
- `POST /api/analyze` - Start product analysis
- `GET /api/status` - Get analysis progress
- `GET /api/results` - Get final results
- `GET /api/download/:filename` - Download analysis files

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Mobile**: `sm` (640px+)
- **Tablet**: `md` (768px+)
- **Desktop**: `lg` (1024px+)
- **Large Desktop**: `xl` (1280px+)

## 🚀 Build and Deployment

### Development Build
```bash
npm run dev
```

### Production Build
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navigation.jsx   # Main navigation component
│   ├── Footer.jsx       # Footer component
│   ├── Alert.jsx        # Alert/notification component
│   └── LoadingSpinner.jsx # Loading spinner component
├── pages/               # Page components
│   ├── Home.jsx         # Landing page
│   ├── Analysis.jsx     # Analysis progress page
│   └── Results.jsx      # Results display page
├── services/            # API services
│   └── api.js           # API client configuration
├── utils/               # Utility functions
│   └── helpers.js       # Helper functions
├── App.jsx              # Main app component
├── main.jsx             # App entry point
└── index.css            # Global styles
```

## 🎯 Key Features Explained

### Real-time Analysis Tracking
- Polls backend API every 2 seconds for progress updates
- Smooth progress bar animations
- Phase-based step indicators
- Estimated time remaining

### Data Visualization
- Pie charts for sentiment distribution
- Bar charts for feature scores
- Interactive tooltips
- Responsive chart containers

### User Experience
- Loading states for all async operations
- Error handling with user-friendly messages
- Copy-to-clipboard functionality
- File download capabilities
- Social sharing integration

## 🔍 Performance Optimizations

- **Code Splitting**: Automatic route-based code splitting
- **Image Optimization**: Optimized assets and lazy loading
- **Bundle Analysis**: Optimized bundle size with Vite
- **Caching**: Proper HTTP caching headers
- **Animations**: Hardware-accelerated CSS transforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the Revify Major Project. All rights reserved.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Contact the development team

---

Built with ❤️ for better product decisions