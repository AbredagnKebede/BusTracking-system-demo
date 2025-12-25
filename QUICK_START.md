# Quick Start Guide - Simplified Bus Tracking System

## Prerequisites
- Python 3.9+ installed
- Virtual environment activated
- All dependencies installed

## 5-Minute Setup

### 1. Start the Server
```bash
cd WebApp
..\venv\Scripts\python.exe manage.py runserver
```

### 2. Access Admin Panel
- URL: http://127.0.0.1:8000/admin/
- Login with your superuser credentials

### 3. Add Your First Route (Example)

#### Step A: Add Bus Stops
Go to **Dashboard > Locations** and add:
1. Name: "Main Gate", Route: "1", Geographic Location: "0,0"
2. Name: "Library", Route: "1", Geographic Location: "0,0"
3. Name: "Dormitory", Route: "1", Geographic Location: "0,0"

#### Step B: Define Route Order
Go to **Dashboard > Location Orders** and add:
- Route Number: 1
- List of Locations: `Main Gate,Library,Dormitory,Main Gate`

#### Step C: Add a Bus
Go to **Webhook > Buses** and add:
- Bus Registration Number: "BUS001"
- Route Number: 1
- Destination: "Main Gate"
- Starting Point: "Main Gate"

#### Step D: Add Schedule
Go to **Webhook > Schedules** and add:
- Bus ID: Select BUS001
- Starting Point to Destination: `08:00,10:00,12:00`
- Destination to Starting Point: `08:30,10:30,12:30`
- Times of Turns: `08:00,08:30,10:00,10:30,12:00,12:30`

#### Step E: Activate Bus
Go to **Webhook > Active Buses** and add:
- Bus ID: Select BUS001
- Active: ✓ (checked)
- Active Time: Current time
- Starting Time: "08:00"

### 4. Test the System

1. Go to: http://127.0.0.1:8000/location/
2. Select "Main Gate" as starting point
3. Select "Library" as destination
4. Click Submit
5. View available schedules

### 5. Test Webhook (Optional)

Send a test webhook to update bus location:
```bash
curl -X POST http://127.0.0.1:8000/webhook/ \
  -H "id: BUS001" \
  -H "route: 1" \
  -H "connected: true" \
  -H "Content-Type: application/json" \
  -d '{"current_stop": "Library"}'
```

## Common Issues

**"Please select a bus stop from the list"**
→ Make sure you selected actual bus stop names from the dropdown

**"Invalid bus stop selected"**
→ The stop name must exactly match what's in the Locations table

**No schedules showing**
→ Make sure you added schedules and activated the bus

## Next Steps

- Add more routes and stops
- Configure multiple buses
- Set up your IoT devices to send webhook updates
- Customize for your campus needs

For detailed documentation, see `SIMPLIFIED_SYSTEM_GUIDE.md`

