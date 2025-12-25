# Simplified Bus Tracking System Guide (GPS-Free)

This guide explains how to use the simplified bus tracking system that works without GPS functionality - perfect for campus projects.

## What Changed?

✅ **Removed:**
- GPS coordinate tracking
- Google Maps API integration
- Geopy distance calculations
- "My Location" GPS detection
- Real-time map visualization

✅ **Simplified to:**
- Bus stop name-based tracking
- Predefined bus stop selection
- Route-based location tracking
- Simple status display

## System Overview

The system now works entirely with **bus stop names** instead of GPS coordinates. Buses report which stop they're currently at, and the system tracks their progress along predefined routes.

## Setting Up Your Bus System

### Step 1: Add Bus Stops (Locations)

1. Go to **Admin Panel**: http://127.0.0.1:8000/admin/
2. Navigate to **Dashboard > Locations**
3. Click **"Add Location"**
4. Fill in:
   - **Name**: Bus stop name (e.g., "Main Gate", "Library", "Dormitory A")
   - **Route Number**: The route this stop belongs to (e.g., "1", "2")
   - **Geographic Location**: You can leave this as "0,0" or any placeholder (not used anymore)
   - **Sub Route**: Usually 0

**Example Locations:**
- Name: "Main Gate", Route: "1", Geographic Location: "0,0"
- Name: "Library", Route: "1", Geographic Location: "0,0"
- Name: "Dormitory A", Route: "1", Geographic Location: "0,0"

### Step 2: Define Route Order

1. Go to **Dashboard > Location Orders**
2. Click **"Add Location Order"**
3. Fill in:
   - **Route Number**: Same as your bus route (e.g., 1)
   - **Sub Route**: Usually 0
   - **List of Locations**: Comma-separated list of stop names in order

**Example:**
- Route Number: 1
- List of Locations: `Main Gate,Library,Dormitory A,Science Building,Main Gate`

**Important:** The order matters! This defines the sequence of stops on the route.

### Step 3: Add Buses

1. Go to **Webhook > Buses**
2. Click **"Add Bus"**
3. Fill in:
   - **Bus Registration Number**: Unique ID (e.g., "BUS001")
   - **Route Number**: The route this bus serves (e.g., 1)
   - **Sub Route Number**: Usually 0
   - **Destination**: Final stop name (e.g., "Main Gate")
   - **Starting Point**: First stop name (e.g., "Main Gate")

### Step 4: Add Bus Schedules

1. Go to **Webhook > Schedules**
2. Click **"Add Schedule"**
3. Select the **Bus ID**
4. Fill in:
   - **Destination to Starting Point**: Comma-separated times (e.g., "08:00,10:00,12:00,14:00")
   - **Starting Point to Destination**: Comma-separated times (e.g., "08:30,10:30,12:30,14:30")
   - **Times of Turns**: Comma-separated times (e.g., "08:00,08:30,10:00,10:30")

### Step 5: Activate Buses

1. Go to **Webhook > Active Buses**
2. Click **"Add Active Bus"**
3. Select the **Bus ID**
4. Set:
   - **Active**: True/False
   - **Active Time**: Current time
   - **Starting Time**: Next scheduled departure time

## How the Webhook Works Now

### Old Format (GPS - Removed):
```json
{
  "altitude": 9.0227,
  "longitude": 38.7468,
  "massage": "test"
}
```

### New Format (Bus Stop Name):
```json
{
  "current_stop": "Library",
  "massage": "optional message"
}
```

### Webhook Headers:
- `id`: Bus registration number (e.g., "BUS001")
- `route`: Route number (e.g., "1")
- `connected`: "true" or "false"

### Example Webhook Call:

```bash
curl -X POST http://127.0.0.1:8000/webhook/ \
  -H "id: BUS001" \
  -H "route: 1" \
  -H "connected: true" \
  -H "Content-Type: application/json" \
  -d '{"current_stop": "Library", "massage": "At Library stop"}'
```

## How Users Search for Buses

1. User goes to: http://127.0.0.1:8000/location/
2. User selects **Starting Point** from dropdown (predefined bus stops only)
3. User selects **Destination** from dropdown (predefined bus stops only)
4. System shows available bus schedules
5. User can view bus status and next/previous stops

**Note:** Users can no longer use "My Location" - they must select from the bus stop list.

## Updating Bus Location

When a bus arrives at a stop, send a webhook with the current stop name:

```json
{
  "current_stop": "Library"
}
```

The system will automatically:
- Update the bus's current location
- Determine the next stop (based on route order)
- Determine the previous stop
- Update bus status

## Testing the System

### 1. Test Location Selection
- Go to http://127.0.0.1:8000/location/
- Try selecting different bus stops
- Verify schedules appear

### 2. Test Webhook
Use the curl command above or Postman to send test webhook data.

### 3. Test Bus Status
- Go to a tour details page
- Verify bus status updates (Online/Offline)
- Check that next/last locations display correctly

## Troubleshooting

### Error: "Please select a bus stop from the list"
- **Solution**: Make sure you selected actual bus stop names, not "My Location"

### Error: "Invalid bus stop selected"
- **Solution**: The stop name must exactly match a location in the database

### Error: "Starting point and destination must be on the same route"
- **Solution**: Both stops must belong to the same route number

### Bus location not updating
- **Solution**: Check that the `current_stop` name in webhook exactly matches a location name in the database

## Benefits of Simplified System

✅ **No GPS Required** - Works indoors and in areas with poor GPS signal  
✅ **No API Keys Needed** - No Google Maps API required  
✅ **Simpler Setup** - Just add bus stop names  
✅ **More Reliable** - No GPS accuracy issues  
✅ **Perfect for Campus** - Ideal for fixed routes with known stops  
✅ **Lower Cost** - No API usage fees  

## Next Steps

1. Add your campus bus stops to the Locations model
2. Define your route orders
3. Add your buses and schedules
4. Update your ESP32/IoT devices to send bus stop names instead of GPS coordinates
5. Test the system with real bus data

## Example Campus Setup

**Route 1 - Main Campus Loop:**
- Stops: Main Gate → Library → Science Building → Dormitory A → Main Gate
- Bus: BUS001
- Schedule: Every 30 minutes from 7:00 AM to 10:00 PM

**Route 2 - North Campus:**
- Stops: Main Gate → North Gate → Sports Complex → Main Gate
- Bus: BUS002
- Schedule: Every 45 minutes from 8:00 AM to 9:00 PM

The system will track which stop each bus is at and show users the next available bus based on schedules.

