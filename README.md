# 🎒 Backpacking Trip Planner

A modern, interactive web application for planning your perfect backpacking adventure. Built with Streamlit and featuring a clean, responsive design with advanced trip analytics.

![Trip Planner Screenshot](https://via.placeholder.com/800x400/667eea/ffffff?text=Trip+Planner+Preview)

## ✨ Features

### 🌟 **Core Features**
- **Interactive Trip Planning** - Day-by-day itinerary builder
- **Smart Budget Calculator** - Track expenses with visual breakdowns
- **Real-time Analytics** - Insights into your travel patterns
- **Modern UI/UX** - Clean, responsive design with animations
- **Export Options** - Download as CSV or generate text summaries

### 📊 **Advanced Analytics**
- Trip completion tracking
- Cost trend analysis
- Transport and accommodation insights
- Budget utilization metrics

### 🎨 **Modern Design**
- Gradient backgrounds and smooth animations
- Interactive cards with hover effects
- Progress tracking for trip planning
- Mobile-responsive layout

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/backpacking-trip-planner.git
   cd backpacking-trip-planner
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run backpacking_planner.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
backpacking-trip-planner/
├── src/
│   ├── main.py                 # Main application entry point
│   ├── components/
│   │   ├── __init__.py
│   │   ├── trip_overview.py    # Trip overview component
│   │   ├── day_planning.py     # Day-by-day planning component
│   │   ├── budget_calculator.py # Budget management component
│   │   ├── analytics.py        # Analytics dashboard component
│   │   └── trip_summary.py     # Trip summary component
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py          # Helper functions
│   │   ├── data_manager.py     # Data management utilities
│   │   └── export_utils.py     # Export functionality
│   └── styles/
│       ├── __init__.py
│       └── css_styles.py       # CSS styling definitions
├── assets/
│   ├── screenshots/            # Application screenshots
│   └── icons/                  # Icon assets
├── docs/
│   ├── user_guide.md          # User guide documentation
│   ├── api_reference.md       # API reference
│   └── contributing.md        # Contributing guidelines
├── tests/
│   ├── __init__.py
│   ├── test_main.py           # Main application tests
│   └── test_components.py     # Component tests
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Development dependencies
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── LICENSE                   # License information
└── CHANGELOG.md              # Version history
```

## 🎯 Usage Guide

### 1. **Trip Overview** 🌍
Start by setting up your basic trip information:
- Trip name and dates
- Main destinations
- Total budget
- Travel preferences (style, group size, transport)

### 2. **Day-by-Day Planning** 📅
Plan each day of your adventure:
- Add/remove/copy days
- Set locations and dates
- Plan transportation routes
- Book accommodations
- Add notes and activities
- Track completion progress

### 3. **Budget Calculator** 💰
Manage your finances:
- Set budget categories
- Track spending by category
- View visual budget breakdowns
- Monitor budget utilization
- Get budget recommendations

### 4. **Analytics Dashboard** 📊
Gain insights into your trip:
- Completion status tracking
- Transport usage analysis
- Accommodation distribution
- Cost trend visualization
- Daily spending patterns

### 5. **Trip Summary** 📋
Review and export your plans:
- Complete itinerary overview
- Export to CSV format
- Generate text summaries
- View detailed statistics

## 🛠️ Development

### Setting up Development Environment

1. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run tests**
   ```bash
   python -m pytest tests/
   ```

3. **Code formatting**
   ```bash
   black src/
   flake8 src/
   ```

### Adding New Features

1. Create feature branch: `git checkout -b feature-name`
2. Add your component to `src/components/`
3. Update `backpacking_planner.py` to include new component
4. Add tests in `tests/`
5. Update documentation
6. Submit pull request

## 📱 Screenshots

### Trip Overview
![Trip Overview](https://via.placeholder.com/600x400/667eea/ffffff?text=Trip+Overview)

### Day Planning
![Day Planning](https://via.placeholder.com/600x400/f5576c/ffffff?text=Day+Planning)

### Budget Calculator
![Budget Calculator](https://via.placeholder.com/600x400/4facfe/ffffff?text=Budget+Calculator)

### Analytics Dashboard
![Analytics](https://via.placeholder.com/600x400/fa709a/ffffff?text=Analytics)

## 🎨 Customization

### Themes
The application supports easy theme customization through CSS variables in `src/styles/css_styles.py`:

```python
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
```

### Adding New Components
1. Create new file in `src/components/`
2. Follow the existing component structure
3. Import and add to main navigation

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/contributing.md) for details.

### Quick Contribution Guide
1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [User Guide](docs/user_guide.md)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/backpacking-trip-planner/issues)
- **Discussions**: Join discussions on [GitHub Discussions](https://github.com/yourusername/backpacking-trip-planner/discussions)

## 🎉 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Charts powered by [Plotly](https://plotly.com/)
- Icons from various sources
- Inspired by the backpacking community

## 🗺️ Roadmap

### Version 2.0 (Coming Soon)
- [ ] Multi-currency support
- [ ] Weather integration
- [ ] Map visualization
- [ ] Collaborative planning
- [ ] Mobile app version

### Version 2.1
- [ ] AI-powered recommendations
- [ ] Social sharing features
- [ ] Trip templates
- [ ] Expense tracking photos

---

**Happy Planning! 🎒✈️**

*Made with ❤️ for adventurers everywhere*
