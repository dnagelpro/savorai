# SavorAI

SavorAI is a sleek and minimalist restaurant discovery app designed for food lovers exploring new cities or seeking hidden gems in their area. Powered by the Yelp Fusion API, Google Maps, and OpenAI, users can search by city, cuisine, and price—or ask in plain English where to eat.

## Features

- Search restaurants by:
  - City and State
  - Cuisine
  - Dining style (price level)
- Yelp Fusion API integration for real-time restaurant data
- Google Maps integration for map and location display
- AI-enhanced query parsing using OpenAI
- Mobile responsive design with clean user interface
- Intelligent fallback if no matches are found locally
- About section with project mission and branding
- Interactive form using Tom Select for dropdown inputs

## How It Works

Users can either:
1. Fill in the form fields manually (City, State, Cuisine, Dining Style)
2. Or use the natural language prompt:  
   Example: `I want sushi in Seattle, WA`

The AI assistant will parse the query and pre-fill the form.

## Tech Stack

- Python
- Flask
- Jinja2 Templates
- Yelp Fusion API
- Google Maps API
- OpenAI API
- Tom Select (dropdown enhancements)
- HTML/CSS (Inter font)

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/yourusername/savorai.git
cd savorai
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add:

```
YELP_API_KEY=your_yelp_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
OPENAI_API_KEY=your_openai_api_key
```

5. Run the app:

```bash
python run.py
```

6. Open the app at:

```
http://127.0.0.1:5000
```

## Project Structure

```
savorai/
│
├── app/
│   ├── home/
│   │   └── routes.py
│   ├── results/
│   │   └── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── results.html
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── img/
│   │       └── savorai-logo.png
│   └── utils/
│       ├── yelp_api.py
│       └── openai_parser.py
│   └── __init__.py
├── .env
├── requirements.txt
├── README.md
└── run.py
```

## Deployment (Optional)

To deploy on platforms like Render or Fly.io, be sure to:

- Add your environment variables securely
- Use a `Procfile` with:

```
web: gunicorn run:app
```

- Optionally include a `render.yaml` or `fly.toml` if needed

## License

This project is for educational and portfolio purposes only. Not intended for commercial use.

---

**Created by:** Dawn Nagel  
**GitHub:** https://github.com/dnagelpro/savorai

