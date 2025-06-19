# India Temperature Difference Analysis

This repository contains a Python script that generates temperature difference visualizations for major Indian cities for June 2025.

## Overview

The script simulates temperature patterns for 11 major Indian cities and visualizes:
1. Average temperature differences from historical averages (bar chart)
2. Daily temperature differences throughout the month (heatmap)

## Cities Included

- New Delhi
- Mumbai
- Chennai
- Kolkata
- Bangalore
- Hyderabad
- Ahmedabad
- Pune
- Jaipur
- Srinagar
- Bhubaneswar

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn

## Installation

```bash
# Clone the repository
git clone https://github.com/SouravBarik00/india-temp-analysis.git
cd india-temp-analysis

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pandas numpy matplotlib seaborn
```

## Usage

```bash
python india_temp_diff.py
```

This will generate two visualization files:
- `india_temperature_diff_june_2025.png`: Bar chart showing average temperature differences
- `india_temperature_diff_heatmap_june_2025.png`: Heatmap showing daily temperature differences

## Sample Output

The visualizations show projected temperature differences from historical averages for June 2025.

## Note

This is a simulation based on historical patterns and does not represent actual forecasts for June 2025.
