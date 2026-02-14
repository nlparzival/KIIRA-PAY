# 🚢 Floating Edge Nodes: Schepen als Mobiele Sensoren

**Datum:** 12 februari 2026  
**Concept:** Raspberry Pi + Jetson edge nodes op schepen voor real-time maritieme intelligence  
**Status:** Advanced strategy (Phase 4+)

---

## 🎯 **CONCEPT: FLOATING SENSOR MESH**

### **Waarom schepen als edge nodes:**

```yaml
Traditional Approach (Land-Based):
  - Vaste stations op de kust
  - AIS bereik: 40-60 km
  - Zicht op schepen: Laatste uur voor aankomst
  - Waterdata: Statische meetstations (Rijkswaterstaat)
  - Coverage: Kustlijn only

Floating Edge Nodes (Ship-Based):
  - Mobiele sensoren die mee varen
  - AIS bereik: 200+ km (midden op zee)
  - Zicht op schepen: 5-12 uur VOOR ze kust bereiken
  - Waterdata: Real-time, distributed (10+ locaties)
  - Coverage: Gehele Noordzee + binnenwateren

The Advantage:
  ✅ LNG tankers zien 12-24 uur voordat ze Rotterdam bereiken
  ✅ Watertemperatuur/diepte op 10+ plekken (real-time)
  ✅ Weersomstandigheden op zee (niet aan wal)
  ✅ Scheepsverkeer patterns (congestie voorspellen)
  ✅ Mobiele coverage (waar nodig, when needed)
  
Result: 12-24 uur voorsprong op haven aankomsten! 💰
```

---

## 🌊 **WAT MEET EEN SCHIP-NODE?**

### **1. AIS/VHF Radio (SDR) - "De Ogen"**

```yaml
What It Sees:
  ✅ AIS transponders (schepen tot 200+ km)
  ✅ VHF maritieme communicatie (havens, kustwacht)
  ✅ DSC (Digital Selective Calling) noodsignalen
  ✅ Weather broadcasts (NAVTEX)

Why This Matters:
  - Landstations: Zien tot horizon (60 km)
  - Schip op zee: Ziet 360° tot 200 km
  - Coverage: 10x groter gebied!

Data Captured:
  - Ship MMSI (unique identifier)
  - Position (lat/lon, GPS)
  - Speed (SOG - Speed Over Ground)
  - Course (COG - Course Over Ground)
  - Destination (often blank, but sometimes filled)
  - Cargo type (tanker, container, bulk, etc.)
  - Draft (diepgang = cargo load indicator)

Example Use Case:
  Your Ship: 100 km offshore Rotterdam
  Detects: LNG tanker "Al Rekayyat" from Qatar
  Position: 200 km away, heading 090° (East)
  ETA calculation: 8-10 hours to Rotterdam
  
  Your land station: Receives alert 8 hours early!
  Market: Only sees ship when 1 hour from port
  
  Your edge: 7 hours to prepare trading strategy! 💰

Hardware:
  - SDRplay RSPdx + VHF antenna: €300
  - Mounted: High on ship (mast/bridge)
  - Power: 12V DC from ship (via buck converter)
```

---

### **2. NMEA 2000/0183 (Scheepsdata) - "De Zintuigen"**

```yaml
What Is NMEA?
  - Maritime data bus protocol
  - Standard on ALL modern ships
  - Like CAN bus in cars, but for boats
  - Connects: GPS, depth sounder, wind sensors, etc.

What You Can Read (Passive, Read-Only):
  ✅ GPS Position (high-accuracy, 1m precision)
  ✅ Speed Over Ground (SOG) + Speed Through Water (STW)
  ✅ Course Over Ground (COG) + Heading (HDG)
  ✅ Depth Below Keel (dieptemeter)
  ✅ Water Temperature (surface + optional deep)
  ✅ Wind Speed + Direction (true + apparent)
  ✅ Barometric Pressure (weather trends)
  ✅ Water Salinity (optional, some ships)
  ✅ Pitch/Roll/Yaw (ship movement, sea state)

Why This Is GOLD:
  1. Dieptekaart (Bathymetry):
     - 10 schepen = 10 mobiele depth sounders
     - Build real-time depth map (rivers, harbors)
     - Detect sedimentation (dredging needed)
     - Rijkswaterstaat would pay for this data!
     
  2. Watertemperatuur:
     - Cooling capacity voor power plants
     - 1°C difference = 50-100 MW capacity impact
     - Predict plant output 4-8 hours ahead
     
  3. Wind @ Sea:
     - Offshore wind conditions (not coastal!)
     - Better prediction for wind farms
     - KNMI only has coastal stations
     
  4. Sea State (Golven):
     - Pitch/roll sensors = wave height proxy
     - Rough seas = delayed ship arrivals
     - Smooth seas = faster transport
     
  5. Fuel Consumption Proxy:
     - Speed Through Water vs Speed Over Ground
     - Difference = current resistance
     - High resistance = more fuel = delays

Data Pipeline:
  Ship NMEA → Pi via PiCAN-M HAT → Parse sentences
  → Store locally (InfluxDB) → Upload via Starlink
  → Central Supabase → Agent processing
  → Predictions: Water temp impact on plants

Hardware:
  - PiCAN-M HAT (NMEA 2000 interface): €100
  - OR: USB NMEA 0183 adapter: €50
  - Galvanic isolation: CRITICAL (protects Pi)
  - NO TRANSMIT (read-only, safety!)

CRITICAL SAFETY:
  ⚠️ READ-ONLY MODE (cannot write to ship bus)
  ⚠️ Galvanic isolation (no ground loops)
  ⚠️ Separate power supply (not ship's systems)
  ⚠️ No interference with navigation (passive tap)
  ⚠️ Physical data diode (hardware read-only)
```

---

### **3. Environmental Sensors - "Extra Zintuigen"**

```yaml
Optional Sensors You Can Add:

  Air Quality (€100):
    - NOx, CO2, PM2.5, PM10
    - Detects: Ship emissions + port pollution
    - Use Case: Environmental compliance tracking
    - Market: Emissions trading data
    
  Thermal Camera (€300):
    - FLIR Lepton module
    - Detects: Other ships, port heat signatures
    - Use Case: Night vision, thermal pollution
    
  Weather Station (€100):
    - Temp, humidity, pressure, wind
    - Better than NMEA wind sensor (calibrated)
    - Use Case: Hyper-local forecasting
    
  Hydrophone (€200):
    - Underwater microphone
    - Detects: Ship engines, marine life
    - Use Case: Traffic density, whale migration
    
  Vibration Sensors (€50):
    - Accelerometer (ship motion)
    - Use Case: Sea state, engine health
    
  Light Sensor (€20):
    - Ambient light (day/night, fog)
    - Use Case: Visibility, safety index

Total Extra Sensors: €770 (optional)
Core Sensors (AIS + NMEA): €400
Full Setup: €1,170 per ship
```

---

## 📡 **CONNECTIVITEIT OP ZEE**

### **De 3 Lagen van Communicatie:**

```yaml
LAYER 1: Coastal (0-20 km)
  Technology: 5G / 4G LTE
  Hardware: Teltonika RUT955/956 (€250)
  Speed: 50-300 Mbps
  Latency: 30-100 ms
  Cost: €20-50/maand (unlimited data)
  
  Use Case:
    - Real-time streaming (within range)
    - Live dashboard (schip in haven)
    - Instant uploads (high bandwidth)

LAYER 2: Open Sea (20-500 km)
  Technology: Starlink Maritime
  Hardware: Starlink dish + router (€2,500-5,000)
  Speed: 100-350 Mbps
  Latency: 25-50 ms (LEO satellites!)
  Cost: €250-500/maand (priority maritime)
  
  Use Case:
    - Continuous connectivity (anywhere)
    - Live streaming (medium bandwidth)
    - Remote access (SSH, monitoring)
    
  Note: Expensive but GAME-CHANGER
        Only deploy on high-value routes

LAYER 3: Offline (No Coverage)
  Technology: Local storage (NVMe SSD)
  Hardware: 2 TB SSD (€150)
  Duration: 2-4 weeks offline capacity
  Sync: Automatic when connection restored
  
  Use Case:
    - Long voyages (intercontinental)
    - Backup (if Starlink fails)
    - Low-priority data (batch upload)

RECOMMENDED APPROACH:

  Phase 1 (MVP): 4G only (coastal ships)
    - Cost: €250 hardware + €30/maand
    - Coverage: Rotterdam ↔ Antwerpen ↔ Amsterdam
    - Good for: River barges, coastal ferries
    
  Phase 2 (Growth): 4G + Offline buffer
    - Cost: €400 (add SSD)
    - Coverage: North Sea (upload when in port)
    - Good for: Cargo ships, tankers
    
  Phase 3 (Advanced): Starlink Maritime
    - Cost: €5,000 hardware + €500/maand
    - Coverage: Global oceans
    - Good for: High-value LNG tankers, container ships
    
  Break-Even:
    Starlink only justified if:
      ✅ Ship value: €50M+ (LNG tanker)
      ✅ Cargo value: €10M+ per trip
      ✅ Data value: €5k+ per month (trading edge)
```

---

## 💻 **HARDWARE SETUP PER SCHIP**

### **Option A: Budget Setup (River/Coastal)**

```yaml
Core Components:
  - Raspberry Pi 5 (8GB): €120
  - 256GB NVMe SSD: €80
  - M.2 HAT: €20
  - SDRplay RSPdx (VHF/AIS): €250
  - VHF Marine Antenna: €50
  - NMEA USB adapter: €50
  - Teltonika RUT955 (4G): €250
  - Waterproof case (IP67): €100
  - Power supply (12V → 5V): €30
  - Mounting hardware: €50
  
  Total: €1,000 per ship

Power Consumption:
  - Pi 5: 5W
  - SDR: 2W
  - 4G modem: 5W
  - Total: 12W continuous
  - 288 Wh per day
  - Cost: €0.10 per day (ship's power)

Data Volume:
  - AIS: 1-5 MB/hour
  - NMEA: 0.1 MB/hour
  - Sensors: 0.5 MB/hour
  - Total: 2-7 MB/hour = 50-170 MB/day
  - 4G cost: Negligible (within unlimited data)

Software:
  - Raspberry Pi OS Lite (headless)
  - Docker + Docker Compose
  - AIS receiver (rtl_ais or ais-decoder)
  - NMEA parser (gpsd or custom Python)
  - InfluxDB (time-series storage)
  - Tailscale (VPN)
  - BalenaCloud (fleet management)

Deployment Time: 4 hours per ship
Maintenance: Remote (via Tailscale SSH)
Lifespan: 3-5 years (saltwater environment)
```

---

### **Option B: Advanced Setup (North Sea / Open Ocean)**

```yaml
Core Components:
  - NVIDIA Jetson Orin Nano: €500
  - 1 TB NVMe SSD: €120
  - SDRplay RSPdx: €250
  - PiCAN-M HAT (NMEA 2000): €100
  - Starlink Maritime Dish: €2,500-5,000
  - Environmental sensors: €500
  - Industrial IP68 case: €300
  - UPS battery backup (12V): €150
  - Solar panel (optional, 50W): €100
  
  Total: €4,500-7,500 per ship

Why Jetson (Not Pi):
  ✅ On-board AI inference (edge intelligence)
  ✅ Process video (thermal camera, navigation)
  ✅ Anomaly detection (don't send all data)
  ✅ Autonomous decision-making
  ✅ Lower bandwidth (only send alerts)

Example Use Case:
  Jetson: Monitors AIS for 100 ships
  Normal traffic: Ignored (not transmitted)
  Anomaly: Tanker slows down + changes course
  Alert: "Anomaly detected, sending details"
  Bandwidth: 99% reduction vs raw stream!

Power Consumption:
  - Jetson: 15W (full load)
  - Starlink: 100W (!!!)
  - SDR: 2W
  - Sensors: 3W
  - Total: 120W continuous
  - 2.9 kWh per day
  - Cost: €1-2 per day (ship's diesel)

Software:
  - JetPack (Ubuntu + CUDA)
  - Docker + Kubernetes
  - TensorRT (AI inference)
  - Custom AI models (anomaly detection)
  - BalenaCloud (fleet management)

Deployment Time: 8 hours per ship
Maintenance: Remote (95% of time)
Lifespan: 3-5 years
```

---

## 🚢 **SCENARIO: 10 SCHEPEN FLOATING MESH**

### **Fleet Composition (Strategic Mix):**

```yaml
TIER 1 - High Value (3 ships):
  Type: LNG Tankers / Large Container Ships
  Routes: Rotterdam ↔ Middle East / Asia
  Hardware: Jetson + Starlink (€7,500/ship)
  Investment: €22,500
  
  Why:
    ✅ Long voyages (weeks at sea)
    ✅ High cargo value (€10M-50M)
    ✅ Critical data (LNG = gas prices!)
    ✅ 24/7 connectivity needed
    
  Coverage: Deep ocean (200+ km offshore)
  ROI: €5k-20k per month (trading edge on gas)

TIER 2 - Medium Value (4 ships):
  Type: Cargo ships, Ro-Ro, Chemical tankers
  Routes: Rotterdam ↔ Antwerpen ↔ UK ↔ Germany
  Hardware: Pi + 4G + SSD (€1,000/ship)
  Investment: €4,000
  
  Why:
    ✅ Regular routes (predictable)
    ✅ North Sea coverage (60-100 km offshore)
    ✅ 4G mostly available (coastal)
    ✅ Offline buffer for gaps
    
  Coverage: North Sea + Channel
  ROI: €1k-5k per month (cross-border arbitrage)

TIER 3 - Volume Coverage (3 ships):
  Type: River barges, Coastal ferries
  Routes: Rotterdam ↔ Antwerpen ↔ Moerdijk ↔ Amsterdam
  Hardware: Pi + 4G only (€800/ship)
  Investment: €2,400
  
  Why:
    ✅ High frequency (daily trips)
    ✅ River/coastal only (always 4G)
    ✅ Water quality data (rivers)
    ✅ Low cost, high coverage
    
  Coverage: Maas, Rijn, Scheldt, Noordzeekanaal
  ROI: €500-2k per month (river traffic intel)

TOTAL FLEET INVESTMENT:
  Hardware: €28,900
  Monthly: €1,800 (Starlink + 4G)
  Annual: €50,500
```

---

### **What 10 Ships Give You:**

```yaml
COVERAGE MAP:

  Geographic Coverage:
    - Rotterdam → Antwerpen: 4-6 ships daily
    - North Sea: 2-4 ships at any time
    - Deep Ocean: 1-2 ships (LNG routes)
    - Rivers: 2-3 ships (Maas, Rijn, Scheldt)
    
    Total area: 50,000+ km² (vs 5,000 km² land stations)
    Coverage increase: 10x!

  Temporal Coverage:
    - LNG tanker arrivals: 12-24h early warning
    - Container ships: 6-12h early warning
    - River barges: Real-time traffic flow
    - Weather patterns: 4-8h ahead of coast
    
  Data Volume:
    - AIS contacts: 500-2000 ships/day (vs 50-200 land)
    - NMEA datapoints: 1M+ per day (10 ships)
    - Environmental: Water temp 10 locations, wind 10 locations
    - Storage: 5-15 GB per day (all ships)

UNIQUE CAPABILITIES:

  1. Maritime Traffic Prediction:
     - See congestion 6-12h before harbor
     - Predict delays (weather, waiting times)
     - Rotterdam berth availability forecast
     
  2. Oceanographic Intelligence:
     - Real-time bathymetry (10 depth sounders)
     - Water temperature grid (10x10 km resolution)
     - Wind field (offshore, not coastal)
     - Wave height (pitch/roll sensors)
     
  3. Early Warning System:
     - LNG arrivals: 12-24h advance
     - Container volumes: 8-12h advance
     - Coal/oil shipments: 6-12h advance
     - Weather systems: 4-8h advance (at-sea data)
     
  4. Cross-Border Intelligence:
     - NL ↔ BE ↔ UK ↔ DE ship flows
     - Trade volume indicators (economic activity)
     - Shipping delays (port efficiency)
     
  5. Environmental Monitoring:
     - Ship emissions (NOx, CO2)
     - Water pollution (oil spills, chemicals)
     - Marine traffic density (noise pollution)
     - Compliance verification (MARPOL)

COMPETITIVE ADVANTAGE:
  ✅ NOBODY else has floating sensor mesh
  ✅ Satellite AIS costs €500-2000/month (you have it free)
  ✅ Oceanographic data worth €10k-50k/month (research, ports)
  ✅ Trading edge: 6-24h lead time (priceless!)
  
  Comparable Service (Commercial):
    - Spire Maritime: $2,000-10,000/month
    - Windward: $5,000-20,000/month
    - MarineTraffic Pro: $500-5,000/month
    
  Your Cost: €4,200/month (10 ships all-in)
  Your Value: €10,000-50,000/month equivalent
  
  ROI: 2-12x! 💰💰💰
```

---

## 🛠️ **FLEET MANAGEMENT (10 SCHEPEN)**

### **Hoe beheer je 10 varende computers?**

```yaml
PROBLEM:
  - 10 ships, scattered across Europe
  - Can't physically access (at sea!)
  - Different routes, different schedules
  - Software updates needed
  - Troubleshooting required
  - Security monitoring critical

SOLUTION: Professional Fleet Management Stack
```

---

### **1. BalenaCloud (Container Fleet Management)**

```yaml
What Is It:
  - Cloud platform for IoT device management
  - Built on Docker (containerized apps)
  - Used by: Industrial IoT, edge computing
  - Pricing: Free for 10 devices! (then $15/device)

Why Use It:
  ✅ Deploy software to all 10 ships simultaneously
  ✅ Different apps per ship (if needed)
  ✅ Rollback if deployment fails
  ✅ Monitor health (CPU, RAM, disk, network)
  ✅ Remote access (web terminal)
  ✅ OTA updates (over-the-air)

How It Works:
  1. Create BalenaCloud account
  2. Register 10 devices (Pi's or Jetsons)
  3. Flash BalenaOS to SD cards
  4. Ships boot → Auto-connect to BalenaCloud
  5. Push Docker Compose app from laptop
  6. All 10 ships receive + run app
  
  Update Process:
    You: git push balena main
    BalenaCloud: Builds Docker images
    Ships: Download new version
    Rollout: One-by-one or all-at-once
    Rollback: Instant if something breaks

Dashboard Features:
  - Device list (online/offline status)
  - CPU/RAM/Disk graphs
  - Application logs (real-time)
  - Environment variables (API keys, etc.)
  - Remote terminal (SSH replacement)
  - Metrics (data usage, uptime)

Cost: €0/month (10 devices free tier!)
```

---

### **2. Tailscale VPN (Secure Network)**

```yaml
What Is It:
  - Zero-config VPN (WireGuard based)
  - Mesh network (peer-to-peer)
  - Each device gets static private IP
  - NAT traversal (works behind firewalls)

Why Use It:
  ✅ All 10 ships in one private network
  ✅ SSH access from anywhere (securely)
  ✅ Ships can talk to each other (mesh)
  ✅ Access from laptop/phone
  ✅ No port forwarding needed
  ✅ No exposed services (security!)

How It Works:
  1. Install Tailscale on all devices
  2. Authenticate once (OAuth)
  3. Each device gets IP: 100.x.x.x
  4. Done! (no configuration)
  
  Access:
    Your laptop: SSH 100.64.0.5 (Ship #1)
    Ship #1: SSH 100.64.0.6 (Ship #2)
    Ship #2: Query 100.64.0.1 (Central server)
    
  All encrypted (WireGuard, state-of-the-art)

Features:
  - ACLs (access control lists)
  - Magic DNS (use hostnames, not IPs)
  - Subnet routing (access ship's local network)
  - Exit nodes (route traffic through ship)
  - Taildrop (send files between devices)

Cost:
  - Free: 20 devices, 1 user
  - Personal: $48/jaar (100 devices, 3 users)
  - Team: $6/user/month (unlimited devices)
  
  Recommendation: Personal plan (€48/jaar)
```

---

### **3. Monitoring Dashboard (Grafana + Prometheus)**

```yaml
What To Monitor:

  System Health (per ship):
    - CPU usage (%)
    - RAM usage (MB)
    - Disk usage (GB)
    - Network bandwidth (Mbps up/down)
    - Temperature (°C)
    - Uptime (hours)
    
  Connectivity:
    - 4G signal strength (dBm)
    - Starlink status (connected/offline)
    - Latency (ms)
    - Packet loss (%)
    - Data usage (GB)
    
  Sensors:
    - AIS contacts (ships detected)
    - NMEA sentences received (per hour)
    - GPS quality (satellites, HDOP)
    - SDR frequency errors
    - Camera status (if installed)
    
  Application:
    - Data processed (MB/hour)
    - Database size (GB)
    - API calls made (per hour)
    - Errors logged (count)
    - Last upload timestamp

Dashboard Layout:
  
  Fleet Overview (Main Screen):
    - Map: 10 ship locations (GPS)
    - Table: Online/offline status
    - Graphs: Total AIS contacts, data uploaded
    
  Individual Ship (Drill-Down):
    - System metrics (CPU, RAM, disk)
    - Connectivity (4G/Starlink status)
    - Sensor data (latest readings)
    - Logs (tail -f style, real-time)
    
  Alerts:
    - Ship offline > 1 hour
    - CPU > 90% for 10 minutes
    - Disk > 90% full
    - Temperature > 80°C
    - No GPS fix for 30 minutes
    - SDR error rate > 5%

Implementation:
  - Prometheus: Scrapes metrics from all ships
  - Grafana: Visualizes + alerts
  - AlertManager: Sends SMS/email on issues
  - Loki: Centralized log aggregation
  
  Hosting:
    Option A: Self-hosted (Pi on land)
    Option B: Grafana Cloud (free tier: 10k metrics)
    
  Cost: €0 (Grafana Cloud free tier sufficient)
```

---

### **4. Data Pipeline Architecture**

```yaml
FLOW: Ship → Cloud → Agent

  On Ship (Edge):
    1. Sensors → Raw data → Local processing
    2. Parse (AIS, NMEA) → Structured data
    3. Store (InfluxDB) → 30-day buffer
    4. Compress → 10:1 ratio (gzip)
    5. Upload (4G/Starlink) → Every 15 minutes
    
  In Transit (Network):
    - Tailscale VPN (encrypted)
    - HTTP POST (chunked transfer)
    - Retry logic (if upload fails)
    - Resume (if connection drops)
    
  On Cloud (Central):
    1. Supabase receives data
    2. Decompress → Store in database
    3. Trigger: New data event
    4. Agent: Process new data
    5. Dashboard: Update visualizations
    
  Agent Processing:
    - AIS contacts → Ship tracking database
    - LNG tankers → Alert if Qatar origin
    - NMEA depth → Bathymetry map update
    - Water temp → Plant cooling model update
    - Wind @ sea → Offshore wind forecast
    - Aggregate → Feed to trading model

Data Volume Management:
  
  RAW (On Ship):
    - AIS: 5 MB/hour (before parsing)
    - NMEA: 0.5 MB/hour
    - Sensors: 1 MB/hour
    - Total: 6.5 MB/hour = 156 MB/day
    
  PROCESSED (Uploaded):
    - AIS: 1 MB/hour (parsed, compressed)
    - NMEA: 0.1 MB/hour
    - Sensors: 0.2 MB/hour
    - Total: 1.3 MB/hour = 31 MB/day
    
  10 Ships Total: 310 MB/day = 9.3 GB/month
  
  4G Cost: Included in unlimited plan
  Starlink Cost: Negligible (< 1% of capacity)
  Storage Cost: €0.23/month (Supabase 10 GB free)
```

---

## 💰 **BUSINESS MODEL: DATA AS A SERVICE**

### **Who Pays For Your Fleet Data?**

```yaml
CUSTOMER 1: Commodity Traders
  
  What They Buy:
    - LNG tanker arrivals (12-24h early)
    - Container ship ETAs (6-12h early)
    - Cargo volumes (trade activity index)
    
  Value Proposition:
    - Trade TTF gas futures with 12h lead
    - Trade power futures with 8h lead
    - Position before market reacts
    
  Pricing:
    - Real-time feed: €2,000-5,000/month
    - Historical data: €1,000/month
    - API access: €500/month + usage
    
  Expected Revenue: €3k-6k per client
  Target: 5-10 clients = €15k-60k/month

CUSTOMER 2: Port Authorities
  
  What They Buy:
    - Real-time bathymetry (depth mapping)
    - Sedimentation rates (dredging planning)
    - Traffic flow predictions (berth allocation)
    - Water quality (environmental compliance)
    
  Value Proposition:
    - Save €500k-2M/jaar on dredging
    - Optimize berth allocation (more ships)
    - Environmental reporting (mandatory)
    
  Pricing:
    - Annual license: €50,000-200,000
    - Per-port pricing (Rotterdam, Antwerpen)
    
  Expected Revenue: €50k-200k per port
  Target: 2-4 ports = €100k-800k/year

CUSTOMER 3: Insurance Companies
  
  What They Buy:
    - Ship route data (risk assessment)
    - Sea state conditions (wave height, storms)
    - Pitch/roll/vibration (ship stress)
    - Speed patterns (behavior analysis)
    
  Value Proposition:
    - Underwrite policies with real data
    - Detect risky behavior (speeding in storms)
    - Claims validation (was sea really rough?)
    
  Pricing:
    - API access: €10,000-50,000/year
    - Per-ship analytics: €500-2000/ship
    
  Expected Revenue: €10k-50k per insurer
  Target: 2-5 insurers = €20k-250k/year

CUSTOMER 4: Research Institutes
  
  What They Buy:
    - Oceanographic data (water temp, salinity)
    - Weather at-sea (wind, pressure, humidity)
    - Marine traffic density (noise pollution)
    - Environmental monitoring (emissions)
    
  Value Proposition:
    - Data nobody else collects
    - 10 distributed sensors (coverage)
    - Real-time (not monthly reports)
    
  Pricing:
    - Data access: €5,000-20,000/year
    - Custom sensors: €10,000-50,000 (one-time)
    
  Expected Revenue: €5k-20k per institute
  Target: 3-5 institutes = €15k-100k/year

CUSTOMER 5: Government (Rijkswaterstaat)
  
  What They Buy:
    - Water quality monitoring (compliance)
    - Traffic flow (infrastructure planning)
    - Depth surveys (river maintenance)
    - Weather stations (forecasting)
    
  Value Proposition:
    - Supplement existing monitoring (10x coverage)
    - Real-time vs monthly surveys
    - Lower cost than dedicated ships
    
  Pricing:
    - Annual contract: €100,000-500,000
    - Multi-year deals (3-5 years)
    
  Expected Revenue: €100k-500k/year
  Target: 1-2 agencies

TOTAL REVENUE POTENTIAL:
  Conservative: €200k-500k/year
  Realistic: €500k-1.5M/year
  Optimistic: €1.5M-3M/year

INVESTMENT vs RETURN:
  Fleet setup: €50k (one-time)
  Annual operating: €50k
  Total Year 1: €100k
  
  Revenue Year 1: €200k-500k (conservative)
  Profit Year 1: €100k-400k
  ROI: 100-400% (first year!)
  
  By Year 3:
    Revenue: €1M-2M/year
    Profit: €800k-1.5M/year
    Valuation: €5M-15M (5-10x revenue)
```

---

## ⚠️ **VEILIGHEID & LEGAL**

### **Critical Safety Considerations:**

```yaml
HARDWARE SAFETY:

  ✅ READ-ONLY MODE (Cannot Write):
    - NMEA interface: Passive tap only
    - Physical data diode (hardware enforced)
    - No ability to send commands to ship
    - Cannot interfere with navigation
    
  ✅ Galvanic Isolation:
    - Separate power supply (not ship's 12V)
    - Isolated NMEA interface (optocouplers)
    - No ground loops (prevents damage)
    - Protects both Pi and ship systems
    
  ✅ Physical Security:
    - Waterproof case (IP67 minimum)
    - Shock-mounted (vibration damping)
    - Secured mounting (doesn't move)
    - Away from navigation equipment (no RF interference)
    
  ✅ Power Backup:
    - UPS battery (2-4 hour backup)
    - Graceful shutdown (on ship power loss)
    - Auto-restart (when power restored)
    
  ✅ Redundancy:
    - Local storage (if internet fails)
    - Watchdog (auto-restart if frozen)
    - Dual power inputs (primary + backup)

CYBER SECURITY:

  ✅ VPN Only (No Public Exposure):
    - Tailscale VPN (encrypted)
    - No open ports (inbound blocked)
    - Outbound-only connections
    
  ✅ Authentication:
    - SSH key-only (no passwords)
    - Ed25519 keys (strongest)
    - Separate keys per ship
    - Rotate every 6 months
    
  ✅ Firewall:
    - Drop all inbound (except VPN)
    - Allow outbound (data upload)
    - Rate limiting (DDoS protection)
    
  ✅ Updates:
    - Auto security patches
    - Staged rollouts (test on 1 ship first)
    - Rollback capability
    
  ✅ Monitoring:
    - Intrusion detection (fail2ban)
    - Log analysis (suspicious activity)
    - Alerts (security events)

LEGAL COMPLIANCE:

  ✅ Maritime Regulations:
    - No interference with navigation (IMO)
    - No radio transmission (receive-only)
    - Passive monitoring only
    - No safety-critical systems affected
    
  ✅ Data Privacy (GDPR):
    - No personal data collected
    - Aggregate data only (ship IDs = public)
    - AIS = public broadcast (legal to receive)
    - NMEA = ship's own data (with permission)
    
  ✅ Frequency Licenses:
    - Receive-only: No license needed (EU)
    - VHF maritime: Public band (legal to monitor)
    - AIS: Intended for all vessels (safety)
    - DO NOT TRANSMIT (illegal without license)
    
  ✅ Contracts with Ship Owners:
    - Written agreement (scope, liability)
    - Insurance (equipment + data)
    - Maintenance responsibility (who fixes?)
    - Data ownership (who owns collected data?)
    - Termination clause (easy removal)
    
  ✅ Environmental:
    - No emissions (passive equipment)
    - Minimal power draw (< 100W)
    - E-waste disposal (3-5 year lifespan)

LIABILITY & INSURANCE:

  ✅ Equipment Insurance:
    - Cover: Theft, damage, salt water
    - Value: €1,000-7,500 per ship
    - Cost: €100-300/year per ship
    
  ✅ Liability Insurance:
    - Cover: If equipment causes ship damage
    - Cover: If data breach occurs
    - Amount: €1M-5M
    - Cost: €1,000-5,000/year
    
  ✅ Data Insurance:
    - Cover: Loss of collected data
    - Cover: Downtime (if customers affected)
    - Amount: €500k-2M
    - Cost: €500-2,000/year
```

---

## 🎯 **DEPLOYMENT ROADMAP**

### **Phase 1: Proof of Concept (Month 1-3)**

```yaml
Goal: Prove floating edge nodes work

Deploy: 1 ship (friendly connection)
Type: River barge or coastal ferry (daily route)
Hardware: Pi + 4G + AIS + NMEA (€1,000)
Route: Rotterdam ↔ Antwerpen (regular)
Duration: 3 months trial

Success Criteria:
  ✅ 99% uptime (device stays online)
  ✅ AIS data: 500+ ships detected per trip
  ✅ NMEA data: Depth, position, wind recorded
  ✅ 4G connectivity: > 90% coverage
  ✅ Data uploaded: Every 15 minutes
  ✅ No interference: Ship systems unaffected
  ✅ Value demonstrated: Predict Rotterdam traffic 2-4h early

Investment: €1,000 hardware + €30/maand
Expected Outcome: Proof floating nodes add value
Decision: If successful → Phase 2
```

---

### **Phase 2: Strategic Expansion (Month 4-9)**

```yaml
Goal: Cover critical routes

Deploy: 3 ships total (1 existing + 2 new)
Types:
  - 1x River barge (Rotterdam ↔ Antwerpen)
  - 1x Coastal cargo (Rotterdam ↔ UK/DE)
  - 1x Container ship (Rotterdam ↔ Hamburg)
  
Hardware: Pi + 4G + SSD (€1,000 each)
Investment: €2,000 (2 new ships)
Monthly: €90 (3 × €30 data)

Coverage:
  - North Sea: 60-100 km offshore
  - Rivers: Maas, Rijn, Scheldt
  - Cross-border: NL ↔ BE ↔ DE ↔ UK

Expected Results:
  - AIS coverage: 10x larger area
  - Water data: 3 distributed sensors
  - Early warnings: 4-8 hours (ship arrivals)
  - Accuracy improvement: +3-5% (energy agent)

Revenue Target: €10k-20k MRR (justify expansion)
Decision: If profitable → Phase 3
```

---

### **Phase 3: Fleet Build-Out (Month 10-18)**

```yaml
Goal: 10-ship floating mesh

Deploy: 10 ships total (3 existing + 7 new)
Composition:
  - 3x Coastal cargo/ferry (Pi + 4G)
  - 3x River barges (Pi + 4G)
  - 2x North Sea cargo (Pi + 4G + SSD)
  - 2x LNG tankers (Jetson + Starlink) 🔥
  
Hardware Investment:
  - 7x Pi setups: €7,000
  - 2x Jetson + Starlink: €15,000
  - Total: €22,000
  
Monthly Operating:
  - 8x 4G: €240
  - 2x Starlink: €1,000
  - Maintenance: €500
  - Total: €1,740/month = €21k/year

Coverage:
  - Full North Sea + rivers
  - Deep ocean (LNG routes, 200+ km)
  - Cross-border (BE, DE, UK, DK)
  - 24/7 monitoring

Data Products Launch:
  - API for traders: €2k-5k/month
  - Port authority contracts: €50k-200k/year
  - Research data sales: €10k-50k/year

Revenue Target: €100k-300k/year
Break-Even: Month 12-18
Decision: Expand to data-as-service business
```

---

### **Phase 4: Monetization & Scale (Month 18+)**

```yaml
Goal: Sustainable business model

Products:
  1. Energy Trading Intelligence:
     - Real-time LNG arrivals
     - Gas price predictions (12-24h lead)
     - Power plant cooling forecasts
     - Price: €5k-10k/month per client
     - Target: 5-10 clients = €50k-100k/month
     
  2. Maritime Intelligence SaaS:
     - API access (AIS, NMEA, environmental)
     - Historical data (years of coverage)
     - Predictive analytics (ship ETAs, congestion)
     - Price: €1k-5k/month per client
     - Target: 20-50 clients = €20k-250k/month
     
  3. Government Contracts:
     - Rijkswaterstaat (water monitoring)
     - KNMI (weather data)
     - Havenbeheer Rotterdam (traffic)
     - Price: €100k-500k/year
     - Target: 1-3 contracts = €100k-1.5M/year
     
  4. Research Partnerships:
     - Universities (oceanography)
     - TNO (applied research)
     - NIOZ (marine research)
     - Price: €10k-50k/year + co-authorship
     - Target: 3-5 partners = €30k-250k/year

Total Revenue Potential: €500k-2M/year
Operating Costs: €100k-200k/year
Net Profit: €300k-1.8M/year
Valuation: €3M-18M (10x profit)

Scale Options:
  - Expand to 20-50 ships (Europe-wide)
  - Add new sensors (atmospheric, underwater)
  - Partner with shipping companies (fleet-wide)
  - License technology to competitors
  - Acquisition target (TomTom, Windward, Spire)
```

---

## 🎯 **TL;DR - EXECUTIVE SUMMARY**

```yaml
Concept: Floating Edge Nodes
  → Raspberry Pi / Jetson on ships
  → Mobiele sensoren (AIS, NMEA, environmental)
  → 10-ship fleet = 50,000 km² coverage

Investment:
  Phase 1 (PoC): €1,000 (1 ship)
  Phase 2 (Strategic): €3,000 (3 ships)
  Phase 3 (Fleet): €25,000 (10 ships)
  Phase 4 (Scale): €50,000-100,000 (20-50 ships)

Operating Costs:
  - 4G data: €30/ship/month
  - Starlink: €500/ship/month (2 ships)
  - Maintenance: €50/ship/month
  - Total (10 ships): €1,740/month = €21k/year

Expected Results:
  - AIS coverage: 10x larger (200+ km offshore)
  - Early warnings: 6-24 hours (LNG tankers)
  - Water data: 10 distributed sensors (real-time)
  - Accuracy gain: +5-10% (energy trading agent)

Revenue Potential:
  Year 1: €100k-300k (trading edge + port data)
  Year 2: €300k-1M (SaaS platform)
  Year 3: €1M-3M (government contracts + scale)

ROI:
  Break-even: 12-18 months
  Year 3 profit: €500k-2M
  Valuation: €5M-20M (acquisition target)

Competitive Moat:
  ✅ Proprietary floating sensor network
  ✅ Data nobody else has (at-sea, not coastal)
  ✅ 6-24h lead time (vs satellite AIS)
  ✅ €2k-10k/month value (vs €500-2000/month Spire)
  ✅ Scalable (add ships = add coverage)

Key Insight:
  → This is NOT about controlling ships
  → This IS about mobile intelligence gathering
  → Ships = Vehicles for sensors (taxi model)
  → Data value >> Hardware cost (100x)
  
When To Deploy:
  ✅ After land-based edge network proven (Phase 3+)
  ✅ After revenue > €50k-100k/month
  ✅ After trading strategy validated
  ✅ After first 1-2 pilot ships successful
  
Priority: PHASE 4+ (Advanced, not MVP)
But: If opportunity arises (friendly ship owner) → Grab it!
```

---

**Dit is hoe je "ogen en oren op zee" worden! 🚢🌊**
