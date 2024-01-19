# PhonePe Pulse Data Dashboard

## Overview
This dashboard offers insights into PhonePe's transaction data, highlighting trends and patterns across various parameters. It's built using Python and visualizes the data through a Streamlit-based interactive dashboard.

## Components

- `data_extraction.py`: Script to process JSON data into structured CSVs and load them into a MySQL database.
- `dashboard.py`: Streamlit application for visualizing the data.

## Getting Started

### Prerequisites
- Python 3.x
- MySQL
- Streamlit
- Plotly
- Pandas

### Installation
Clone the repository and install dependencies:
```
git clone  https://github.com/phonepe/pulse.git
pip install -r requirements.txt
```

### Setting up the Database
1. Create a MySQL database named `phonepe_data`.
2. Create `credentials.py` with your MySQL credentials:
   ```python
   DB_USER = 'your_username'
   DB_PASSWORD = 'your_password'
    ```

### Running the Data Extraction Script
1. Make sure pulse (Phonepe Data) is inside your project directory
2. Run `data_extraction.py`:
```
python data_extraction.py
```

### Launching the dashboard
Run the streamlit dashboard:
```
streamlit run dashboard.py
```

## Features

- Data Extraction: Automates processing of raw JSON data into structured formats.
- Interactive Dashboard: Dynamic visualization with filters for different data perspectives.
- Geographical Insights: Transaction data visualization on a choropleth map of India.
- User Growth Analysis: Displays user growth trends over time.

## File Descriptions

- `data_extraction.py`: Processes raw PhonePe data.
- `dashboard.py`: Streamlit app for data visualization.
- `requirements.txt`: Python dependencies for the project.

## Further Development

- UI Enhancement: Improve the user interface for better user experience.
- Hosting Readiness: Modify the script for online hosting on Streamlit, including updating the MySQL server to a cloud-based solution.
- Expanded Data Utilization: Increase the use of `map_transaction_amount` and `map_user_data`.
- Enhanced Visualizations: Develop more sophisticated visualizations for the top data insights page.
- District-Level Detail: Incorporate more granular, district-level details in the geographical insights map.

## Acknowledgements

- PhonePe for providing the dataset
- Streamlit for the interactive web app framework.
- Plotly for data visualization tools.
- Thanks to the author of this Youtube video ("https://www.youtube.com/watch?v=aJmaw3QKMvk") for guidance on creating a choropleth map of India.

## Authors

- Habeel Ansari

<b>Check out the project walkthrough video at : https://www.youtube.com/watch?v=jvy2zLvaBNA&t=61s</b>
