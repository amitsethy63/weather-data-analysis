
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Get weather data
url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 20.2961,
    "longitude": 85.8245,
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "temperature_2m_mean",
        "precipitation_sum"
    ],
    "timezone": "Asia/Kolkata"
}

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Step 2: Convert to DataFrame
    df = pd.DataFrame(data["daily"])

    # Step 3: Rename columns
    df.rename(columns={
        "time": "Date",
        "temperature_2m_max": "Max_Temperature",
        "temperature_2m_min": "Min_Temperature",
        "temperature_2m_mean": "Avg_Temperature",
        "precipitation_sum": "Rainfall"
    }, inplace=True)

    df["Date"] = pd.to_datetime(df["Date"])

    # Step 4: Save CSV
    df.to_csv("weather_data.csv", index=False)

    print("Weather Data:")
    print(df.head())

    # Step 5: Statistical analysis
    print("\nAverage Temperature:",
          df["Avg_Temperature"].mean())

    print("Highest Temperature:",
          df["Max_Temperature"].max())

    print("Lowest Temperature:",
          df["Min_Temperature"].min())

    print("Total Rainfall:",
          df["Rainfall"].sum())

    # Step 6: Monthly average temperature
    df["Month"] = df["Date"].dt.month

    monthly = df.groupby("Month")["Avg_Temperature"].mean()

    print("\nMonthly Average Temperature:")
    print(monthly)

    # Step 7: Display both graphs together
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    # Daily temperature graph
    axes[0].plot(
        df["Date"],
        df["Avg_Temperature"],
        label="Average Temperature"
    )
    axes[0].set_title("Daily Average Temperature - Bhubaneswar")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Temperature (°C)")
    axes[0].legend()
    axes[0].grid(True)
    axes[0].tick_params(axis="x", rotation=45)

    # Monthly temperature graph
    sns.barplot(
        x=monthly.index,
        y=monthly.values,
        ax=axes[1]
    )
    axes[1].set_title("Monthly Average Temperature")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Temperature (°C)")

    plt.tight_layout()

    # Save both graphs in one image
    plt.savefig("weather_analysis.png", dpi=300)
    plt.show()

    print("\nProject completed successfully!")

except requests.exceptions.RequestException as e:
    print("API connection error:", e)

except (KeyError, ValueError) as e:
    print("Data processing error:", e)

