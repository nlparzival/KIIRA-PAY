#!/bin/bash

# KIIRA-PAY - Create all data source directories
# This creates placeholder directories for all potential data sources

echo "Creating data source directories..."

# ============================================================================
# ENERGY MARKETS & TRADING
# ============================================================================
mkdir -p energy-markets/{epex-spot,ice,eex,nordpool,omie}
mkdir -p crypto-energy/{power-ledger,energy-web,solarcoin}

# ============================================================================
# ELECTRICITY & GRID
# ============================================================================
mkdir -p grid/{tennet-data,entso-e,liander,stedin,enexis,westland-infra}
mkdir -p balancing/{tennet-balancing,regelenergie,fcr,afrr,mfrr}

# ============================================================================
# WEATHER & CLIMATE
# ============================================================================
mkdir -p weather/{knmi,openweather,darksky,weatherbit,tomorrow-io}
mkdir -p climate/{nasa,noaa,copernicus,ecmwf}
mkdir -p solar/{pvgis,solcast,solargis,nrel-solar}

# ============================================================================
# STATISTICS & GOVERNMENT
# ============================================================================
mkdir -p statistics/{cbs-data,eurostat,oecd,worldbank,imf}
mkdir -p dutch-gov/{rijkswaterstaat,rdw,pdok,kvk,kadaster}
mkdir -p economic/{cpb,dnb,ecb,fed,bls}

# ============================================================================
# ENERGY ORGANIZATIONS
# ============================================================================
mkdir -p energy-orgs/{iea,irena,ember,bp-energy,eia}

# ============================================================================
# FINANCIAL MARKETS
# ============================================================================
mkdir -p forex/{ecb-rates,exchangerate-api,fixer,currencyapi}
mkdir -p commodities/{brent-oil,natural-gas,coal,uranium}
mkdir -p stocks/{euronext,aex,shell,bp,totalenergies,orsted}
mkdir -p crypto/{bitcoin,ethereum,energy-tokens}

# ============================================================================
# CARBON & EMISSIONS
# ============================================================================
mkdir -p carbon/{eu-ets,carbon-prices,voluntary-markets}
mkdir -p emissions/{edgar,cdiac,ghg-protocol}

# ============================================================================
# REAL ESTATE & INFRASTRUCTURE  
# ============================================================================
mkdir -p buildings/{bag,ep-online,woningmarkt,bouwbesluit}
mkdir -p infrastructure/{charging-stations,hydrogen-stations,heat-networks}

# ============================================================================
# TRANSPORT & MOBILITY
# ============================================================================
mkdir -p transport/{ns-data,ndw,anwb,tomtom-traffic}
mkdir -p vehicles/{rdw,ev-database,ocpp-data}

# ============================================================================
# INDUSTRY & CONSUMPTION
# ============================================================================
mkdir -p industry/{manufacturing,data-centers,greenhouses,ports}
mkdir -p consumption/{smart-meters,household-data,commercial}

# ============================================================================
# RESEARCH & ACADEMIC
# ============================================================================
mkdir -p research/{arxiv,ieee,tu-delft,tno}
mkdir -p models/{machine-learning,forecasting,optimization}

# ============================================================================
# SOCIAL & BEHAVIORAL
# ============================================================================
mkdir -p social/{twitter,reddit,news-apis,sentiment}
mkdir -p consumer/{cbs-sentiment,gfk,consumer-confidence}

# ============================================================================
# BLOCKCHAIN & WEB3
# ============================================================================
mkdir -p blockchain/{ethereum-mainnet,polygon,arbitrum,optimism}
mkdir -p defi/{uniswap,curve,aave,compound}
mkdir -p nft/{energy-nfts,rec-tokens,carbon-credits}

# ============================================================================
# BANKS & FINANCIAL INSTITUTIONS
# ============================================================================
mkdir -p banks/{ing,rabobank,abn-amro,triodos}
mkdir -p payments/{ideal,stripe,mollie,adyen}

# ============================================================================
# INSURANCE & RISK
# ============================================================================
mkdir -p insurance/{allianz,delta-lloyd,achmea}
mkdir -p risk/{weather-risk,price-risk,grid-risk}

# ============================================================================
# SATELLITE & GEOSPATIAL
# ============================================================================
mkdir -p satellite/{sentinel,landsat,modis,planet}
mkdir -p geospatial/{openstreetmap,here,mapbox,google-earth-engine}

# ============================================================================
# AI & ML PLATFORMS
# ============================================================================
mkdir -p ai-platforms/{openai,anthropic,google-ai,azure-ml}
mkdir -p ml-models/{pretrained,custom,ensemble}

# ============================================================================
# APIS & AGGREGATORS
# ============================================================================
mkdir -p api-data/{rapid-api,apilayer,data-gov}
mkdir -p aggregators/{quandl,alpha-vantage,twelve-data}

# ============================================================================
# REAL-TIME STREAMS
# ============================================================================
mkdir -p streams/{mqtt,kafka,websockets,sse}
mkdir -p iot/{sensors,meters,controllers}

# ============================================================================
# UTILITIES & SUPPLIERS
# ============================================================================
mkdir -p suppliers/{essent,eneco,vattenfall,greenchoice,budget-energie}
mkdir -p utilities/{gas-unie,gasunie-transport,ace-terminal}

echo "✅ All data source directories created!"
echo ""
echo "Directory structure:"
tree -L 2 -d . | head -100

