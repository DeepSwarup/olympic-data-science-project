import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

# Load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

# Custom page configuration
# Custom page configuration
st.set_page_config(
    page_title="Olympic Data Analysis", 
    page_icon="https://e7.pngegg.com/pngimages/311/694/png-clipart-olympics-torch-illustration-winter-olympic-games-2016-summer-olympics-2018-winter-olympics-torch-relay-torch-food-sport-thumbnail.png",  # Replace with your image URL
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .sidebar .sidebar-content img {
        width: 150px;
        margin-bottom: 10px;
    }
    .sidebar .sidebar-content h2 {
        font-family: monospace,'Arial Black', sans-serif;
        font-size: 18px;
    }

    /* Main Title and Text */
    h1 {
        font-family: monospace,'Georgia', serif;
        font-size: 40px;
        color: #1f4e79;
    }
    h2 {
        font-family: monospace, sans-serif;
        font-size: 26px;
        color: #1f4e79;
    }
    p {
        font-family: monospace, sans-serif;
        font-size: 18px;
        color: #333;
    }

    /* Card-Like Container */
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin: 20px 0;
    }
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        flex: 1;
        min-width: 200px;
        text-align: center;
        margin-bottom: 15px;
    }
    .card h3 {
        font-family: monospace, 'Arial Black', sans-serif;
        font-size: 24px;
        color: #1f4e79;
    }
    .card p {
        font-family: monospace, 'Arial', sans-serif;
        font-size: 20px;
        color: #555;
    }

    /* Center Plotly Charts */
    .plotly-chart {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.image('https://colorlib.com/wp/wp-content/uploads/sites/2/olympic-logo-2024.png', use_column_width=True)
st.sidebar.title("Olympics Analysis")
# st.sidebar.markdown("Explore historical data on Olympic events, countries, athletes, and more.")
user_menu = st.sidebar.radio('Navigate', ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis'))

# Main Title and Introduction
st.title("Olympics Data Analysis")
st.markdown("""
    Welcome to the Olympics Data Analysis app! Dive deep into historical Olympic data, uncover insights, and explore trends across different sports and countries.
""")

# Medal Tally Tab
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    st.subheader(f"{selected_country} performance in {selected_year} Olympics" if selected_year != 'Overall' and selected_country != 'Overall' else 
                 f"{selected_country} overall performance" if selected_country != 'Overall' else 
                 f"Medal Tally in {selected_year} Olympics" if selected_year != 'Overall' else 
                 "Overall Tally")
    
    st.table(medal_tally)

# Overall Analysis Tab
elif user_menu == 'Overall Analysis':
    st.subheader("Top Statistics")
    
    # Use a container for card-like statistics
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="card">
                    <h3>Editions</h3>
                    <p>{}</p>
                </div>
            """.format(df['Year'].nunique() - 1), unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="card">
                    <h3>Host Cities</h3>
                    <p>{}</p>
                </div>
            """.format(df['City'].nunique()), unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class="card">
                    <h3>Sports</h3>
                    <p>{}</p>
                </div>
            """.format(df['Sport'].nunique()), unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="card">
                    <h3>Events</h3>
                    <p>{}</p>
                </div>
            """.format(df['Event'].nunique()), unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="card">
                    <h3>Nations</h3>
                    <p>{}</p>
                </div>
            """.format(df['region'].nunique()), unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class="card">
                    <h3>Athletes</h3>
                    <p>{}</p>
                </div>
            """.format(df['Name'].nunique()), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Participating Nations Over Time
    st.subheader("Participating Nations over the Years")
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region", title="Participating Nations over the Years",
                  labels={"region": "Number of Participating Nations"}, template="plotly_white")
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=50))
    st.plotly_chart(fig)

    # Events Over Time
    st.subheader("Events over the Years")
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event", title="Events over the Years",
                  labels={"Event": "Number of Events"}, template="plotly_white")
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=50))
    st.plotly_chart(fig)

    # Athletes Over Time
    st.subheader("Athletes over the Years")
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name", title="Athletes over the Years",
                  labels={"Name": "Number of Athletes"}, template="plotly_white")
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=50))
    st.plotly_chart(fig)

    # Heatmap of Events
    st.subheader("Number of Events over Time (Every Sport)")
    fig, ax = plt.subplots(figsize=(15, 10))
    heatmap_data = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(heatmap_data.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True, linewidths=.5, ax=ax, cmap="YlGnBu")
    st.pyplot(fig)

    # Most Successful Athletes
    st.subheader("Most Successful Athletes")
    sport_list = ['Overall'] + sorted(df['Sport'].unique().tolist())
    selected_sport = st.selectbox('Select a Sport', sport_list)
    top_athletes = helper.most_successful(df, selected_sport)
    st.table(top_athletes)

# Country-wise Analysis Tab
elif user_menu == 'Country-wise Analysis':
    st.sidebar.header('Country-wise Analysis')
    
    country_list = sorted(df['region'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    
    st.subheader(f"{selected_country} - Medal Tally Over the Years")
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal", title=f"{selected_country} - Medal Tally Over the Years",
                  labels={"Medal": "Number of Medals"}, template="plotly_white")
    st.plotly_chart(fig)
    
    st.subheader(f"{selected_country} Excels in the Following Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(pt, annot=True, linewidths=.5, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
    
    st.subheader(f"Top 10 Athletes from {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# Athlete-wise Analysis Tab
elif user_menu == 'Athlete-wise Analysis':
    st.subheader("Distribution of Age")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    age_data = {
        "Overall Age": athlete_df['Age'].dropna(),
        "Gold Medalist": athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna(),
        "Silver Medalist": athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna(),
        "Bronze Medalist": athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna(),
    }
    fig = ff.create_distplot([age_data[k] for k in age_data.keys()], list(age_data.keys()), show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    st.subheader("Height vs Weight Analysis")
    sport_list = ['Overall'] + sorted(df['Sport'].unique().tolist())
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=temp_df,
        x='Weight', y='Height', 
        hue='Medal', style='Sex', 
        s=60, ax=ax
    )
    ax.set_title(f'Height vs Weight in {selected_sport}')
    ax.set_xlabel('Weight (kg)')
    ax.set_ylabel('Height (cm)')
    st.pyplot(fig)

    st.subheader("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"], title="Men vs Women Participation Over the Years",
                  labels={"value": "Number of Athletes"}, template="plotly_white")
    st.plotly_chart(fig)
