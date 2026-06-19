import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="India Weather Analytics", page_icon="🌤️", layout="wide")
st.markdown(
    "<h1 style='text-align:center; color: #60A5FA;'>🌤️ India 50 Cities Weather & AQI Analytics Portal</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color: #FACC15;'>Advanced Trend Detection, Correlation Study, and Regional Insights</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

uploaded_file = st.file_uploader("UPload CSV File", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    city_list = ["All City"] + list(df["City"].unique())
    selected_city = st.sidebar.selectbox("Choose Your City", city_list)
    if selected_city == "All City":
        filtered_df = df
    else:
        filtered_df = df[df["City"] == selected_city]

    day_selecter = st.sidebar.checkbox("Filter by Day")
    if day_selecter:
        min_day = int(df["Day"].min())
        max_day = int(df["Day"].max())
        day_selecter = st.sidebar.slider("Choose a Specific Day", 1, max_day, min_day)
        filtered_df = filtered_df[filtered_df["Day"] == day_selecter]

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📋 Executive Overview",
            "🌡️ Temperature & AQI Hub",
            "⛈️ Monsoon & Wind Dynamics",
            "🧠 Advanced Statistical Insights",
        ]
    )
    with tab1:
        x = df["Max_Temperature"].idxmax()
        city = df.loc[x, "City"]
        day = df.loc[x, "Day"]
        temp = df.loc[x, "Max_Temperature"]
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric(
            label=f"Highest Temperature Overall (India) - ", value=f"{temp} °C"
        )

        y = df["Min_Temperature"].idxmin()
        city = df.loc[y, "City"]
        day = df.loc[y, "Day"]
        temp = df.loc[y, "Min_Temperature"]
        m_col2.metric(
            label=f"Lowest temperature overall (India) - ", value=f"{temp} °C"
        )

        avg_aqi = round(df["AQI"].mean(), 2)
        m_col3.metric("Average AQI in India - ", f"{avg_aqi}, AQI")

        total_rainfall = round(df["Rainfall"].sum(), 2)
        m_col4.metric("Total Rainfall in India - ", f"{total_rainfall} mm")
        st.markdown("---")
        st.dataframe(filtered_df)

    with tab2:
        x = filtered_df["Max_Temperature"].idxmax()
        city = filtered_df.loc[x, "City"]
        day = filtered_df.loc[x, "Day"]
        temp = filtered_df.loc[x, "Max_Temperature"]
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric(
            label=f"Highest Temperature Overall in {selected_city} - ",
            value=f"{temp} °C",
        )

        y = filtered_df["Min_Temperature"].idxmin()
        city = filtered_df.loc[y, "City"]
        day = filtered_df.loc[y, "Day"]
        temp = filtered_df.loc[y, "Min_Temperature"]
        m_col2.metric(
            label=f"Lowest temperature overall in {selected_city} - ",
            value=f"{temp} °C",
        )

        avg_aqi = round(filtered_df["AQI"].mean(), 2)
        m_col3.metric(f"Average AQI in {selected_city} - ", f"{avg_aqi}, AQI")

        avg_temp = round(filtered_df["Temperature"].mean(), 2)
        m_col4.metric(f"Average Temperature in {selected_city} - ", f"{avg_temp} °C")

        if avg_temp > 40:
            st.error("🔴 Extreme Heat Alert")
        elif avg_temp > 35:
            st.warning("🟠 High Temperature Warning")
        else:
            st.success("🟢 Temperature is Normal")

        if avg_aqi > 200:
            st.error("🔴 Hazardous Air Quality")
        elif avg_aqi > 175:
            st.warning("🟠 Poor Air Quality")
        else:
            st.success("🟢 Air Quality Acceptable")

        heatwave_days = (filtered_df["Max_Temperature"] > 40).sum()
        cold_days = (filtered_df["Min_Temperature"] < 20).sum()
        st.info(f"🔥 Total Heatwave Days: {heatwave_days}")
        st.info(f"❄️ Total Cold Days: {cold_days}")

        trendss = []
        first_temp = filtered_df.groupby("City")["Temperature"].first()
        last_temp = filtered_df.groupby("City")["Temperature"].last()
        for city in first_temp.index:
            diff = last_temp[city] - first_temp[city]
            if diff > 0:
                trendss.append([city, "Increasing"])
            elif diff < 0:
                trendss.append([city, "Decreasing"])
            else:
                trendss.append([city, "Stable"])

        trend_df = pd.DataFrame(trendss, columns=["City", "Trend"])
        st.subheader("Temperature Trend by City")
        st.dataframe(trend_df.head(5))

        trends = []
        first_aqi = filtered_df.groupby("City")["AQI"].first()
        last_aqi = filtered_df.groupby("City")["AQI"].last()
        for city in first_aqi.index:
            diff = last_aqi[city] - first_aqi[city]
            if diff > 0:
                trends.append([city, "Increasing"])
            elif diff < 0:
                trends.append([city, "Decreasing"])
            else:
                trends.append([city, "Stable"])

        trend_df = pd.DataFrame(trends, columns=["City", "Trend"])
        st.subheader("AQI Trend by City")
        st.dataframe(trend_df.head(5))
        st.markdown("---")

        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.markdown("### 🌡️ Temperature Daily Trend")
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.lineplot(
                data=filtered_df,
                x="Day",
                y="Temperature",
                palette="#1E293B",
                ax=ax1,
                linewidth=2.5,
                markers="o",
            )
            plt.grid(True, alpha=0.2, linestyle="--")
            plt.title("30-Day Temperature Movement", fontsize=10, fontweight="bold")
            plt.xlabel("Day", fontsize=8)
            plt.ylabel("Temperature (°C)", fontsize=8)
            st.pyplot(fig1)

        with g_col2:
            st.markdown("### 🌡️ AQI Daily Trend")
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.barplot(
                data=filtered_df,
                x="Day",
                y="AQI",
                palette="mako",
                errorbar=None,
                ax=ax2,
            )
            plt.title(
                "Average Air Quality Index Across Cities",
                fontsize=10,
                fontweight="bold",
            )
            plt.xlabel("City", fontsize=8)
            plt.ylabel("AQI Level", fontsize=8)
            st.pyplot(fig2)


    with tab3:
        m_col1, m_col2, m_col3 = st.columns(3)
        total_rainfall = filtered_df["Rainfall"].sum()
        m_col1.metric("🌧️ Total Rainfall", f"{total_rainfall:,.2f} mm")

        avg_humid = filtered_df["Humidity"].mean()
        m_col2.metric("💧 Average Humidity", f"{avg_humid:.2f}%")

        avg_wind = filtered_df["Wind_Speed"].mean()
        m_col3.metric("💨 Average Wind Speed", f"{avg_wind:.2f} km/h")

        a_col1, a_col2, a_col3 = st.columns(3)
        heavy_rainfall = (filtered_df["Rainfall"] > 50).sum()
        storm_level = (filtered_df["Wind_Speed"] > 30).sum()
        calm_days = (filtered_df["Wind_Speed"] < 10).sum()

        a_col1.info(f"🚨 Heavy Rain Days: {heavy_rainfall}")
        a_col2.warning(f"🌪️ Storm Days: {storm_level}")
        a_col3.success(f"🍃 Calm Days: {calm_days}")

        st.markdown("---")
        trendsss = []
        first_rain = filtered_df.groupby("City")["Rainfall"].first()
        last_rain = filtered_df.groupby("City")["Rainfall"].last()
        for city in first_rain.index:
            diff = last_rain[city] - first_rain[city]
            if diff > 0:
                trendsss.append([city, "🔺 Increasing"])
            elif diff < 0:
                trendsss.append([city, "🔻 Decreasing"])
            else:
                trendsss.append([city, "🔹 Stable"])
        trend_df = pd.DataFrame(trendsss, columns=["City", "Trend"])
        st.subheader("🌧️ Rainfall Trend by City (Top 5)")
        st.dataframe(trend_df.head(5), use_container_width=True, hide_index=True)
        st.markdown("---")

        st.markdown("### 📊 Monsoon & Wind Speed Visualizations")
        g3_col1, g3_col2 = st.columns(2)
        with g3_col1:
            st.markdown("#### 💨 Wind Speed Distribution")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            sns.histplot(
                data=filtered_df, x="Wind_Speed", kde=True, ax=ax3, color="#0EA5E9", bins=15
            )
            plt.title("Frequency of Wind Speeds", fontsize=10, fontweight="bold")
            plt.xlabel("Wind Speed (km/h)", fontsize=8)
            plt.ylabel("Frequency / Count", fontsize=8)
            plt.grid(True, alpha=0.15, linestyle="--")
            st.pyplot(fig3)

        with g3_col2:
            st.markdown("#### 🌧️ Daily Rainfall Timeline")
            fig4, ax4 = plt.subplots(figsize=(6, 4))

            sns.barplot(
                data=filtered_df,
                x="Day",
                y="Rainfall",
                ax=ax4,
                palette="Blues_r",
                errorbar=None,
            )
            plt.title("Rainfall Volume across Days", fontsize=10, fontweight="bold")
            plt.xlabel("Day of Month", fontsize=8)
            plt.ylabel("Rainfall (mm)", fontsize=8)
            plt.xticks(rotation=90, ha="right", fontsize=7)
            plt.grid(axis="y", alpha=0.15, linestyle="--")
            st.pyplot(fig4)

    with tab4:
        st.markdown("### 🧠 Advanced Statistical Insights (Pearson Correlation)")
        col1, col2, col3 = st.columns(3)
        mean_temp = filtered_df["Temperature"].mean()
        mean_humid = filtered_df["Humidity"].mean()
        mean_rain = filtered_df["Rainfall"].mean()
        mean_ws = filtered_df["Wind_Speed"].mean()

        filtered_df["dev_temp"] = filtered_df["Temperature"] - mean_temp
        filtered_df["dev_humid"] = filtered_df["Humidity"] - mean_humid
        filtered_df["dev_rain"] = filtered_df["Rainfall"] - mean_rain
        filtered_df["dev_ws"] = filtered_df["Wind_Speed"] - mean_ws

        filtered_df["sq_dev_temp"] = filtered_df["dev_temp"] ** 2
        filtered_df["sq_dev_humid"] = filtered_df["dev_humid"] ** 2
        filtered_df["sq_dev_rain"] = filtered_df["dev_rain"] ** 2
        filtered_df["sq_dev_ws"] = filtered_df["dev_ws"] ** 2

        filtered_df["mul_temp_humid"] = (
            filtered_df["dev_temp"] * filtered_df["dev_humid"]
        )
        total_sum_temp_humid = filtered_df["mul_temp_humid"].sum()

        filtered_df["mul_rain_humid"] = filtered_df["dev_rain"] * filtered_df["dev_humid"]
        total_sum_rain_humid = filtered_df["mul_rain_humid"].sum()

        filtered_df["mul_ws_rain"] = filtered_df["dev_rain"] * filtered_df["dev_ws"]
        total_sum_ws_rain = filtered_df["mul_ws_rain"].sum()

        total_sum_sq_dev_temp = filtered_df["sq_dev_temp"].sum()
        total_sum_sq_dev_humid = filtered_df["sq_dev_humid"].sum()
        total_sum_sq_dev_ws = filtered_df["sq_dev_ws"].sum()
        total_sum_sq_dev_rain = filtered_df["sq_dev_rain"].sum()

        temp_humid = total_sum_sq_dev_temp * total_sum_sq_dev_humid
        lower = (temp_humid) ** 0.5

        rain_humid = total_sum_sq_dev_rain * total_sum_sq_dev_humid
        lower2 = (rain_humid) ** 0.5

        ws_rain = total_sum_sq_dev_ws * total_sum_sq_dev_rain
        lower3 = (ws_rain) ** 0.5

        correlation_temp_humid = total_sum_temp_humid / lower
        if correlation_temp_humid > 0:
            col1.metric(
                "🌡️ Temp vs Humidity",
                f"{round(correlation_temp_humid, 2)}",
                delta="📈 Direct Relation",
            )
        elif correlation_temp_humid < 0:
            col1.metric(
                "🌡️ Temp vs Humidity",
                f"{round(correlation_temp_humid, 2)}",
                delta="📉 Inverse Relation",
                delta_color="inverse",
            )
        else:
            col1.metric(
                "🌡️ Temp vs Humidity",
                f"{round(correlation_temp_humid, 2)}",
                delta="🔹 No Relation",
                delta_color="off",
            )

        correlation_rain_humid = total_sum_rain_humid / lower2
        if correlation_rain_humid > 0:
            col2.metric(
                "🌧️ Rain vs Humidity",
                f"{round(correlation_rain_humid, 2)}",
                delta="📈 Direct Relation",
            )
        elif correlation_rain_humid < 0:
            col2.metric(
                "🌧️ Rain vs Humidity",
                f"{round(correlation_rain_humid, 2)}",
                delta="📉 Inverse Relation",
                delta_color="inverse",
            )  ##delta_color="inverse" ka kamaal: Agar relation negative (< 0) aata hai, toh Streamlit us red down-arrow (📉) ko automatic red color me high-highlight karega,
        else:
            col2.metric(
                "🌧️ Rain vs Humidity",
                f"{round(correlation_rain_humid, 2)}",
                delta="🔹 No Relation",
                delta_color="off",
            )  ##delta_color="off" ka use: Jab correlation exact 0 hoga, toh label bina kisi green ya red color ke neutral gray me show hoga

        correlation_ws_rain = total_sum_ws_rain / lower3
        if correlation_ws_rain > 0:
            col3.metric(
                "💨 Wind Speed vs Rain",
                f"{round(correlation_ws_rain, 2)}",
                delta="📈 Direct Relation",
            )
        elif correlation_ws_rain < 0:
            col3.metric(
                "💨 Wind Speed vs Rain",
                f"{round(correlation_ws_rain, 2)}",
                delta="📉 Inverse Relation",
                delta_color="inverse",
            )
        else:
            col3.metric(
                "💨 Wind Speed vs Rain",
                f"{round(correlation_ws_rain, 2)}",
                delta="🔹 No Relation",
                delta_color="off",
            )


        b_col1,b_col2 = st.columns(2)
        with b_col1:
         st.markdown("#### 📊 Selected Data Heatmap")
         numeric_df = filtered_df[["Temperature", "Humidity", "Rainfall", "Wind_Speed", "AQI"]]
         corr_matrix = numeric_df.corr()
         fig_heat, ax_heat = plt.subplots(figsize=(6, 4.8))
         sns.heatmap(
            corr_matrix, 
            annot=True,         ##Isse cells ke andar actual numbers (0.45, -0.21) likhe hue aayenge
            cmap="coolwarm",    ## Direct correlation ke liye Red aur Inverse ke liye Blue gradient color
            fmt=".2f",          ## Numbers ko decimal ke baad 2 digits tak clear rakhne ke liye
            ax=ax_heat,         
            vmin=-1, vmax=1     ## Standard scale line range block karne ke liye
         )
         plt.title("Correlation Matrix Grid", fontsize=10, fontweight='bold')
         st.pyplot(fig_heat)

        with b_col2:
         st.markdown("#### 🗺️ India-wide Climate Clusters")
         fig_scat, ax_scat = plt.subplots(figsize=(6, 4.83))
         sns.scatterplot(
            data=df,
            x="Temperature",
            y="Humidity",
            hue="City",
            palette="viridis",
            alpha=0.6,
            s=30,
            ax=ax_scat,
            legend=False          # Legened chupa diya taaki graph clean dikhe
         )
         plt.title("Temperature vs Humidity (City-wise)", fontsize=10, fontweight='bold')
         plt.xlabel("Temperature (°C)", fontsize=8)
         plt.ylabel("Humidity (%)", fontsize=8)
         plt.grid(True, alpha=0.15, linestyle='--')
         st.pyplot(fig_scat)
