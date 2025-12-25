# Localhost Setup Guide - Bus Tracking System (Ethiopian Context)

This guide will help you run the Bus Tracking System on your local machine.

## Prerequisites

- **Python 3.9.6 or higher** (Python 3.9+ recommended)
- **pip** (Python package installer)
- **Git** (if cloning from repository)
- **Google Maps API Key** (for map functionality)

## Step-by-Step Setup

### 1. Navigate to the WebApp Directory

Open your terminal/command prompt and navigate to the WebApp folder:

```bash
cd Bus-Tracking-System/WebApp
```

### 2. Create a Virtual Environment

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt, indicating the virtual environment is active.

### 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

If you encounter any issues, you can also install packages individually:
```bash
pip install Django==4.2.6 geopy==2.4.0 django-cors-headers==4.2.0 requests==2.31.0 pytz==2023.3.post1
```

### 4. Set Up the Database

Run migrations to create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create a `db.sqlite3` file in the WebApp directory with all necessary database tables.

### 5. Create a Superuser (Optional but Recommended)

Create an admin user to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 6. System Configuration

**Note:** This system has been simplified and **does NOT require Google Maps API** or GPS functionality. It works entirely with predefined bus stop names, making it perfect for campus projects.

See `SIMPLIFIED_SYSTEM_GUIDE.md` for detailed setup instructions.

### 7. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 8. Access the Application

Open your web browser and navigate to:

- **Homepage:** http://127.0.0.1:8000/
- **Location Search:** http://127.0.0.1:8000/location/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Webhook Endpoint:** http://127.0.0.1:8000/webhook/

## Initial Data Setup

To use the system, you'll need to populate the database with:

1. **Bus Routes** - Add buses through the admin panel
2. **Locations** - Add bus stops/locations (names only, no GPS needed)
3. **Schedules** - Add bus schedules for each route
4. **Location Order** - Define the order of stops on each route

### Adding Data via Admin Panel

1. Go to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Add data to:
   - **Locations** - Bus stop names (geographic_location can be "0,0" - not used)
   - **Location Order** - Comma-separated list of stop names in route order
   - **Buses** - Bus registration numbers, routes, destinations
   - **Schedules** - Bus schedules with times
   - **Active Buses** - Activate buses and set their status

### Example: Adding a Location

In the admin panel, add a location like:
- **Name:** "Main Gate"
- **Route Number:** "1"
- **Geographic Location:** "0,0" (not used - can be any placeholder)
- **Sub Route:** 0

**See `SIMPLIFIED_SYSTEM_GUIDE.md` for complete setup instructions.**

## Testing the System

### Test the Webhook Endpoint

You can test the IoT webhook endpoint using curl or Postman:

```bash
curl -X POST http://127.0.0.1:8000/webhook/ \
  -H "id: BUS001" \
  -H "route: 1" \
  -H "connected: true" \
  -H "Content-Type: application/json" \
  -d '{"current_stop": "Main Gate", "massage": "test"}'
```

**Note:** The webhook now accepts bus stop names instead of GPS coordinates. Make sure the `current_stop` value matches a location name in your database.

### Test the Frontend

1. Visit http://127.0.0.1:8000/
2. Click "Get Started"
3. Select starting point and destination
4. View available schedules

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, run the server on a different port:

```bash
python manage.py runserver 8001
```

### Database Errors

If you encounter database errors:
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading

Collect static files:
```bash
python manage.py collectstatic --noinput
```

### Import Errors

Make sure your virtual environment is activated and all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```

## Important Notes

1. **Timezone:** The system is configured for Ethiopian timezone (`Africa/Addis_Ababa`)
2. **Database:** Uses SQLite3 by default (no additional setup needed)
3. **CORS:** CORS is enabled for all origins (configure in settings.py for production)
4. **No GPS Required:** The system works with bus stop names only - perfect for campus projects
5. **No API Keys Needed:** Google Maps API has been removed - no external API dependencies

## Next Steps

After setup:
1. Add bus routes and locations (bus stop names) specific to your campus
2. Define the order of stops for each route
3. Configure bus schedules
4. Set up ESP32/IoT devices to send bus stop names (not GPS) to the webhook endpoint
5. Test the real-time tracking functionality

**For detailed instructions, see `SIMPLIFIED_SYSTEM_GUIDE.md`**

## Support

For issues or questions, refer to the main README.md file or check the Django documentation.

