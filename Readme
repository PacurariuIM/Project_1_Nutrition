# Recipe Discovery App

A web application that helps users discover recipes based on available ingredients. Built with Flask and featuring recipe scraping, unit conversion, and PDF export capabilities.

## Features

- Search recipes by ingredients
- View detailed recipe instructions and ingredients
- Convert cooking units (weight, volume, temperature)
- Export recipes to PDF
- Mobile-responsive design

## Tech Stack

### Backend
- Flask
- Python 3.x
- Gunicorn (Production server)
- SQLAlchemy (Database ORM)
- Beautiful Soup 4 (Web scraping)

### Frontend
- HTML5
- Bootstrap 4.5
- JavaScript
- Custom CSS

### APIs
- Spoonacular API (Recipe search)

## Installation

1. Clone the repository
```sh
bash
git clone <your-repository-url>
cd recipe-discovery-app
```
2. Create and activate virtual environment
```sh
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
3. Install dependencies
```sh
pip install -r requirements.txt
```
4. Create `.env` file and add your Spoonacular API key:
```sh
SPOONACULAR_API_KEY=<your_spoonacular_api_key>
```
5. Run the application
```sh
python main.py
```

## Deployment

The application can be deployed using either Vercel or a traditional server setup with Gunicorn.

### Vercel Deployment
- Configured using vercel.json
- Automatic deployments with Git integration

### Traditional Server Deployment
Detailed server setup instructions can be found in [server_setup.md](journal/server_setup.md)

## CI/CD

Automated deployment using GitHub Actions. See [github_actions.md](journal/github_actions.md) for setup details.

## Project Structure
```sh
├── main.py # Application entry point
├── forms.py # Form definitions
├── requirements.txt # Python dependencies
├── templates/ # HTML templates
│ ├── get_recipes.html
│ └── recipe.html   
├── static/ # Static files (images, CSS)
└── .env # Environment variables
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Acknowledgments

- Spoonacular API for recipe data
- Bootstrap for responsive design
- jsPDF for PDF generation
