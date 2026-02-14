# AI Architecture Design: AlphaZero-Style Multi-Agent System

## 🎯 Vision

Een **AlphaZero/AlphaGo-achtig AI systeem** dat:
1. **Autonoom leert** via self-play en reinforcement learning
2. **Gedecentraliseerd** werkt via multi-agent architectuur
3. **Generiek** is - werkt voor energie, maar ook voor andere sectoren
4. **Schaalbaar** is - van klein experiment naar groot netwerk

---

## 🧠 Core Concept: AlphaZero voor Energie

### Wat is AlphaZero?
- **Self-play:** AI speelt tegen zichzelf en leert
- **Deep RL:** Combineert deep learning met reinforcement learning
- **Policy + Value Networks:** Voorspelt beide wat te doen én hoe goed
- **Monte Carlo Tree Search:** Simuleert toekomst voor beste beslissing
- **Tabula Rasa:** Leert vanaf nul, geen menselijke kennis nodig

### Hoe vertalen we dit naar Energie?

**AlphaZero (Chess)**
- State: Bord positie
- Actions: Zet doen
- Goal: Win het spel
- Learning: Self-play tegen klonen

**Energie Systeem (Ons)**
- State: Energie prijzen, battery level, productie, weer
- Actions: Charge, discharge, trade, hold
- Goal: Maximaliseer profit & stabiliteit
- Learning: Multi-agent self-play in markt simulatie

---

## 🏗️ System Architecture

### Layer 1: Environment (De Wereld)
```
┌─────────────────────────────────────────┐
│         ENERGY MARKET ENVIRONMENT        │
├─────────────────────────────────────────┤
│ • Real-time prijzen (spot market)       │
│ • Weer data (zon, wind)                 │
│ • Grid congestie                        │
│ • Demand forecast                       │
│ • Balancing market                      │
└─────────────────────────────────────────┘
```

**Features:**
- Simuleerbare environment voor training
- Real data feed voor production
- State space representatie
- Reward function design

### Layer 2: Agent Architecture (AI Brein)
```
┌──────────────────────────────────────────┐
│            AGENT (AlphaZero-style)       │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────┐  ┌────────────────┐ │
│  │ Policy Network │  │ Value Network  │ │
│  │ π(a|s)        │  │ V(s)          │ │
│  │ What to do?   │  │ How good?     │ │
│  └────────────────┘  └────────────────┘ │
│            │              │              │
│            └──────┬───────┘              │
│                   │                      │
│         ┌─────────▼──────────┐           │
│         │  Neural Network    │           │
│         │  (Shared Encoder)  │           │
│         └─────────▲──────────┘           │
│                   │                      │
│         ┌─────────┴──────────┐           │
│         │   State Encoder    │           │
│         │   (Observations)   │           │
│         └────────────────────┘           │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │   Monte Carlo Tree Search (MCTS)  │ │
│  │   • Simuleert toekomst            │ │
│  │   • Evalueert opties              │ │
│  │   • Selecteert beste actie        │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │   Experience Replay Buffer        │ │
│  │   • Opslaan alle beslissingen     │ │
│  │   • Learn from history            │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

**Features:**
- Dual network (policy + value)
- MCTS voor planning
- Self-play learning
- Experience replay

### Layer 3: Multi-Agent System (De Markt)
```
┌─────────────────────────────────────────────────┐
│            MULTI-AGENT MARKETPLACE              │
├─────────────────────────────────────────────────┤
│                                                 │
│  Agent A         Agent B         Agent C        │
│  (Battery)       (Solar)         (Wind)         │
│     │               │               │           │
│     └───────────────┼───────────────┘           │
│                     │                           │
│              ┌──────▼──────┐                    │
│              │   Market    │                    │
│              │   Matching  │                    │
│              │   Engine    │                    │
│              └──────┬──────┘                    │
│                     │                           │
│         ┌───────────┼───────────┐               │
│         │           │           │               │
│    ┌────▼────┐ ┌───▼────┐ ┌───▼────┐           │
│    │ Trade 1 │ │Trade 2 │ │Trade 3 │           │
│    └─────────┘ └────────┘ └────────┘           │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │   Collective Intelligence Emerges       │   │
│  │   • Price discovery                     │   │
│  │   • Grid balancing                      │   │
│  │   • Optimal resource allocation         │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

**Features:**
- Agents competeren én coöpereren
- Emergent behavior
- Decentralized control
- Market-based coordination

### Layer 4: Learning Pipeline (AlphaZero Training Loop)
```
┌────────────────────────────────────────────────┐
│          ALPHAZERO TRAINING LOOP               │
├────────────────────────────────────────────────┤
│                                                │
│  1. SELF-PLAY                                  │
│     ┌────────────────────────────────┐         │
│     │ Agent plays against versions  │         │
│     │ of itself in simulated market │         │
│     │ → Generates training data     │         │
│     └────────────────────────────────┘         │
│                    │                           │
│                    ▼                           │
│  2. TRAINING                                   │
│     ┌────────────────────────────────┐         │
│     │ Update neural networks with   │         │
│     │ self-play data                │         │
│     │ → Better policy & value       │         │
│     └────────────────────────────────┘         │
│                    │                           │
│                    ▼                           │
│  3. EVALUATION                                 │
│     ┌────────────────────────────────┐         │
│     │ New agent vs old agent        │         │
│     │ Keep best version             │         │
│     │ → Continuous improvement      │         │
│     └────────────────────────────────┘         │
│                    │                           │
│                    ▼                           │
│  4. DEPLOYMENT                                 │
│     ┌────────────────────────────────┐         │
│     │ Deploy best agent to market   │         │
│     │ Continue learning in real-time│         │
│     └────────────────────────────────┘         │
│                    │                           │
│                    │ (repeat)                  │
│                    └───────────┐               │
│                                │               │
└────────────────────────────────┼───────────────┘
                                 │
                                 ▼
                         SUPERHUMAN PERFORMANCE
```

---

## 🎮 State Space Design (COMPLETE - All Energy Sources)

### What does an agent "see"?

```python
State = {
    # ========== MARKET DATA ==========
    'current_price': float,           # EUR/MWh spot
    'price_history': List[float],     # Last 24h
    'price_forecast': List[float],    # Next 24h prediction
    'imbalance_price': float,         # Real-time balancing
    'capacity_market_price': Dict,    # FCR, aFRR, mFRR prices
    'congestion_zones': Dict,         # Regional grid status
    
    # ========== SOLAR ASSETS ==========
    'solar': {
        'installed_capacity': float,      # kWp
        'current_production': float,      # kW
        'irradiance': float,              # W/m²
        'panel_temperature': float,       # °C
        'inverter_efficiency': float,     # 0-1
        'forecast_24h': List[float],      # kW per hour
        'degradation_rate': float,        # %/year
        'optimal_angle': float,           # degrees
    },
    
    # ========== WIND ASSETS ==========
    'wind': {
        'turbine_type': str,              # 'residential' | 'commercial' | 'offshore'
        'rated_capacity': float,          # kW
        'current_production': float,      # kW
        'wind_speed': float,              # m/s
        'wind_direction': float,          # degrees
        'cut_in_speed': float,            # m/s (start producing)
        'cut_out_speed': float,           # m/s (emergency stop)
        'forecast_24h': List[float],      # m/s per hour
        'wake_effect': float,             # loss from other turbines
        'blade_pitch': float,             # degrees (optimization)
        'maintenance_status': str,        # 'ok' | 'degraded' | 'fault'
    },
    
    # ========== HYDRO ASSETS ==========
    'hydro': {
        'type': str,                      # 'run-of-river' | 'storage' | 'pumped'
        'capacity': float,                # kW
        'current_production': float,      # kW
        'water_flow': float,              # m³/s
        'reservoir_level': float,         # % (if storage type)
        'head_height': float,             # meters
        'turbine_efficiency': float,      # 0-1
        'rainfall_forecast': List[float], # mm per day
        'river_flow_forecast': List[float], # m³/s
        'environmental_minimum': float,   # m³/s (must maintain)
    },
    
    # ========== BIOMASS/BIOGAS CHP ==========
    'biomass': {
        'type': str,                      # 'wood' | 'biogas' | 'waste'
        'capacity_electric': float,       # kWe
        'capacity_thermal': float,        # kWth
        'current_production_e': float,    # kW electric
        'current_production_t': float,    # kW thermal
        'fuel_stock': float,              # tons or m³
        'fuel_cost': float,               # EUR/unit
        'efficiency_electric': float,     # %
        'efficiency_thermal': float,      # %
        'heat_demand_forecast': List[float], # kW per hour
        'maintenance_hours': int,         # hours until maintenance
    },
    
    # ========== GEOTHERMAL ==========
    'geothermal': {
        'type': str,                      # 'binary' | 'flash' | 'heat_pump'
        'capacity': float,                # kW
        'ground_temperature': float,      # °C
        'flow_rate': float,               # L/min
        'cop': float,                     # Coefficient of Performance
        'current_production': float,      # kW
        'heat_demand': float,             # kW
        'electricity_net': float,         # kW (production - consumption)
    },
    
    # ========== HYDROGEN (Power-to-Gas) ==========
    'hydrogen': {
        'electrolyzer_type': str,         # 'PEM' | 'alkaline' | 'SOEC'
        'capacity': float,                # MW
        'current_load': float,            # MW (can flex 0-100%)
        'efficiency': float,              # kWh/kg H2
        'h2_production_rate': float,      # kg/h
        'h2_storage_level': float,        # kg
        'h2_storage_capacity': float,     # kg
        'h2_price': float,                # EUR/kg
        'stack_temperature': float,       # °C
        'stack_degradation': float,       # % (lifetime tracking)
        'minimum_load': float,            # % (technical constraint)
        'ramp_rate': float,               # %/min (flexibility)
    },
    
    # ========== BATTERY STORAGE ==========
    'battery': {
        'type': str,                      # 'li-ion' | 'flow' | 'lead-acid'
        'capacity': float,                # kWh
        'power': float,                   # kW (C-rate)
        'soc': float,                     # 0-100%
        'soh': float,                     # 0-100% (health)
        'temperature': float,             # °C
        'cycles': int,                    # total cycles
        'charge_efficiency': float,       # %
        'discharge_efficiency': float,    # %
        'max_dod': float,                 # % (depth of discharge limit)
        'degradation_model': Dict,        # cycling vs calendar aging
    },
    
    # ========== ELECTRIC VEHICLE (V2G) ==========
    'ev': {
        'model': str,                     # 'Tesla Model 3' | 'Nissan Leaf' etc
        'battery_capacity': float,        # kWh
        'current_soc': float,             # 0-100%
        'charging_power': float,          # kW (AC or DC)
        'v2g_capable': bool,              # can discharge?
        'plugged_in': bool,               # currently connected?
        'next_departure': datetime,       # when will car leave?
        'min_soc_departure': float,       # % needed for trip
        'location': str,                  # 'home' | 'work' | 'public'
        'charging_pattern': Dict,         # learned behavior
    },
    
    # ========== FLEXIBLE LOADS ==========
    'loads': {
        'heat_pump': {
            'capacity': float,            # kW
            'current_demand': float,      # kW
            'indoor_temp': float,         # °C
            'outdoor_temp': float,        # °C
            'setpoint': float,            # °C target
            'thermal_mass': float,        # hours (how long can we shift)
            'cop': float,                 # efficiency
        },
        'industrial': {
            'process_type': str,          # 'data_center' | 'cold_storage' etc
            'base_load': float,           # kW (always on)
            'flexible_load': float,       # kW (can shift)
            'shift_window': int,          # hours (flexibility)
            'priority': int,              # 1-10 (how critical)
        },
    },
    
    # ========== GRID STATUS ==========
    'grid': {
        'frequency': float,               # Hz (50.00 target)
        'voltage': float,                 # V
        'phase_angle': float,             # degrees
        'congestion_level': float,        # 0-1 (local grid)
        'system_imbalance': float,        # MW (positive = shortage)
        'ancillary_services': {
            'fcr_demand': float,          # MW needed
            'afrr_demand': float,         # MW needed  
            'mfrr_demand': float,         # MW needed
        },
        'grid_operator': str,             # 'TenneT' | 'Stedin' etc
    },
    
    # ========== WEATHER ==========
    'weather': {
        'current': {
            'temperature': float,         # °C
            'cloud_cover': float,         # 0-1
            'wind_speed': float,          # m/s
            'wind_direction': float,      # degrees
            'humidity': float,            # %
            'pressure': float,            # hPa
            'precipitation': float,       # mm/h
        },
        'forecast_24h': List[Dict],       # hour-by-hour
        'forecast_7d': List[Dict],        # daily overview
    },
    
    # ========== PORTFOLIO CONTEXT ==========
    'portfolio': {
        'total_capacity': float,          # kW (all assets combined)
        'total_production': float,        # kW (current)
        'total_consumption': float,       # kW (current)
        'net_position': float,            # kW (+ = export, - = import)
        'capital_available': float,       # EUR (buying power)
        'credit_limit': float,            # EUR (max exposure)
        'risk_level': float,              # 0-1 (current exposure)
    },
    
    # ========== TIME CONTEXT ==========
    'time': {
        'timestamp': datetime,
        'time_of_day': int,               # 0-23
        'day_of_week': int,               # 0-6
        'day_of_year': int,               # 1-365
        'season': int,                    # 0-3 (winter/spring/summer/fall)
        'is_weekend': bool,
        'is_holiday': bool,
    },
    
    # ========== HISTORICAL PERFORMANCE ==========
    'history': {
        'profit_1h': float,               # EUR last hour
        'profit_24h': float,              # EUR last 24h
        'profit_7d': float,               # EUR last week
        'profit_30d': float,              # EUR last month
        'success_rate_24h': float,        # 0-1
        'avg_roi': float,                 # % average return
        'sharpe_ratio': float,            # risk-adjusted return
        'max_drawdown': float,            # EUR worst loss period
    },
    
    # ========== OTHER AGENTS (Multi-Agent Context) ==========
    'other_agents': {
        'nearby_agents': List[{
            'agent_id': str,
            'asset_type': str,            # 'solar' | 'wind' etc
            'capacity': float,            # kW
            'typical_behavior': str,      # 'aggressive' | 'conservative'
            'recent_actions': List[str],  # last few actions
        }],
        'market_sentiment': float,        # -1 to +1 (bearish/bullish)
        'coordination_opportunity': bool, # can we collaborate?
    }
}
```

---

## 🎯 Action Space Design (COMPLETE - All Energy Sources)

### What can an agent do?

```python
Actions = {
    # ========== SOLAR ACTIONS ==========
    'solar': {
        'curtail': {
            'amount': float,              # kW to curtail
            'duration': int,              # minutes
            'compensation_price': float,  # EUR/kWh requested
        },
        'self_consume': {
            'priority': int,              # 1-10 (vs selling)
        },
        'sell_to_grid': {
            'amount': float,              # kW
            'min_price': float,           # EUR/kWh
        },
        'inverter_control': {
            'reactive_power': float,      # VAr (voltage support)
            'power_factor': float,        # 0-1
        },
    },
    
    # ========== WIND ACTIONS ==========
    'wind': {
        'adjust_pitch': {
            'angle': float,               # degrees (optimize output)
        },
        'curtail': {
            'target_output': float,       # kW (reduce to this)
            'compensation_required': bool,
        },
        'sell_forecast': {
            'amount': float,              # kWh (forward contract)
            'price': float,               # EUR/kWh
            'delivery_window': tuple,     # (start, end) time
        },
        'emergency_stop': {
            'reason': str,                # 'high_wind' | 'grid_fault'
        },
    },
    
    # ========== HYDRO ACTIONS ==========
    'hydro': {
        'adjust_flow': {
            'target_flow': float,         # m³/s
            'duration': int,              # minutes
        },
        'pump': {                         # if pumped storage
            'power': float,               # kW
            'duration': int,              # minutes
        },
        'generate': {
            'power': float,               # kW
            'duration': int,              # minutes
        },
        'store_water': {                  # optimize reservoir
            'target_level': float,        # %
            'forecast_based': bool,       # wait for better prices?
        },
    },
    
    # ========== BIOMASS ACTIONS ==========
    'biomass': {
        'adjust_output': {
            'electric_power': float,      # kW
            'thermal_power': float,       # kW
            'duration': int,              # hours
        },
        'fuel_order': {
            'amount': float,              # tons
            'delivery_time': datetime,
            'max_price': float,           # EUR/ton
        },
        'maintenance_schedule': {
            'start_time': datetime,
            'duration': int,              # hours
        },
    },
    
    # ========== GEOTHERMAL ACTIONS ==========
    'geothermal': {
        'adjust_output': {
            'target_power': float,        # kW
        },
        'optimize_cop': {
            'flow_rate': float,           # L/min
            'circulation_speed': float,   # %
        },
    },
    
    # ========== HYDROGEN ACTIONS ==========
    'hydrogen': {
        'set_load': {
            'power': float,               # MW (0-100% of capacity)
            'duration': int,              # minutes
        },
        'store_h2': {
            'continue': bool,             # keep producing for storage
            'target_level': float,        # kg
        },
        'sell_h2': {
            'amount': float,              # kg
            'price': float,               # EUR/kg
            'delivery_time': datetime,
        },
        'dispatch_h2': {                  # convert back to electricity
            'amount': float,              # kg
            'via': str,                   # 'fuel_cell' | 'turbine'
        },
        'optimize_efficiency': {
            'temperature': float,         # °C
            'pressure': float,            # bar
        },
    },
    
    # ========== BATTERY ACTIONS ==========
    'battery': {
        'charge': {
            'power': float,               # kW
            'duration': int,              # minutes
            'max_price': float,           # EUR/kWh
            'source': str,                # 'grid' | 'solar' | 'wind'
        },
        'discharge': {
            'power': float,               # kW
            'duration': int,              # minutes
            'min_price': float,           # EUR/kWh
            'destination': str,           # 'grid' | 'load' | 'ev'
        },
        'hold': {
            'duration': int,              # minutes (wait)
            'trigger': Dict,              # conditions to act
        },
        'arbitrage': {
            'buy_threshold': float,       # EUR/kWh
            'sell_threshold': float,      # EUR/kWh
            'volume': float,              # kWh
        },
    },
    
    # ========== EV ACTIONS ==========
    'ev': {
        'smart_charge': {
            'target_soc': float,          # % for departure
            'departure_time': datetime,
            'max_price': float,           # EUR/kWh
            'charging_curve': str,        # 'fast' | 'slow' | 'optimal'
        },
        'v2g_discharge': {
            'power': float,               # kW
            'min_soc': float,             # % (safety margin)
            'min_price': float,           # EUR/kWh
        },
        'v2h_supply': {                   # Vehicle-to-Home
            'power': float,               # kW
            'duration': int,              # minutes
        },
    },
    
    # ========== FLEXIBLE LOAD ACTIONS ==========
    'load_shifting': {
        'heat_pump': {
            'pre_heat': {
                'duration': int,          # minutes
                'target_temp': float,     # °C (higher than normal)
            },
            'post_pone': {
                'duration': int,          # minutes (turn off)
                'min_temp': float,        # °C (comfort limit)
            },
        },
        'industrial': {
            'shift_load': {
                'amount': float,          # kW
                'from_time': datetime,
                'to_time': datetime,
                'compensation_required': float, # EUR
            },
        },
    },
    
    # ========== MARKET ACTIONS ==========
    'market': {
        'day_ahead_bid': {
            'volume': float,              # MWh
            'price': float,               # EUR/MWh
            'hours': List[int],           # 0-23 (which hours)
        },
        'intraday_trade': {
            'type': str,                  # 'buy' | 'sell'
            'volume': float,              # MWh
            'price': float,               # EUR/MWh
            'delivery_time': datetime,
        },
        'balancing_bid': {
            'service': str,               # 'FCR' | 'aFRR' | 'mFRR'
            'capacity': float,            # MW
            'price': float,               # EUR/MW/h
            'availability': float,        # % (reliability)
        },
        'p2p_trade': {
            'peer': str,                  # agent_id
            'type': str,                  # 'buy' | 'sell'
            'volume': float,              # kWh
            'price': float,               # EUR/kWh
            'contract_length': int,       # hours
        },
    },
    
    # ========== COORDINATION ACTIONS ==========
    'coordination': {
        'form_coalition': {
            'agents': List[str],          # agent_ids
            'goal': str,                  # 'peak_shaving' | 'market_power'
            'duration': int,              # hours
        },
        'share_forecast': {
            'with': str,                  # agent_id or 'all'
            'data_type': str,             # 'solar' | 'wind' | 'price'
        },
        'request_backup': {
            'from': str,                  # agent_id
            'amount': float,              # kW
            'duration': int,              # minutes
            'price': float,               # EUR/kWh
        },
    },
    
    # ========== META ACTIONS ==========
    'meta': {
        'do_nothing': {},                 # explicit hold
        'emergency_shutdown': {
            'reason': str,
            'notify': List[str],          # stakeholders
        },
        'request_human_intervention': {
            'issue': str,
            'urgency': int,               # 1-10
        },
    }
}
```
