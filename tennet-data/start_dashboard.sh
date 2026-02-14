#!/bin/bash
cd /Users/moesa/KIIRA-PAY/tennet-data
pkill -f "streamlit run dashboard.py"
streamlit run dashboard.py --server.port 8501
