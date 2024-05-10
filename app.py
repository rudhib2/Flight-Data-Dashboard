import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import output_widget, render_widget
from ipyleaflet import Map, Marker

df = pd.read_csv(Path("Airports.csv"))

df['Fly_date'] = pd.to_datetime(df['Fly_date'])

def create_app_ui(airports):
    app_ui = ui.page_sidebar(
        ui.sidebar(
            ui.input_select(
                id="airport",
                label="Airport",
                choices=airports,
                selected='ORD' if airports else None,
                multiple=False,
            ),
            ui.output_text(id="airport_lat_label"),
            ui.output_text(id="airport_long_label"),
            ui.output_text(id="airport_city_label"),
            ui.input_slider(
                id="selected_year",
                label="Select Year",
                min=1990,
                max=2009,
                value=2000,
                step=1
            ),
            ui.page_fluid(output_widget("map")),
        ),
        ui.navset_underline(
            ui.nav_panel(
                "Departures",
                ui.output_plot(id="departure_vs_date_plot"),
                ui.card (
                    ui.output_data_frame(id="destination_data_table"),  
                ),
            ),
            ui.nav_panel(
                "Arrivals",
                ui.output_plot(id="arrival_vs_date_plot"),
                ui.card (
                    ui.output_data_frame(id="origin_data_table"),  
                ),
            ),
            ui.nav_panel(
                "Top 10 Airports",
                ui.card (
                    ui.output_data_frame(id="top_10_airports"),  
                ),
            ),
            ui.nav_panel(
                "Departures and Arrivals Over Time",
                ui.card (
                    ui.output_plot(id="departures_and_arrivals"),  
                ),
            ),
        ), 
        title="Flight Data Dashboard"
    )
    return app_ui

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def get_available_airports():
        selected_year = input.selected_year.get()
        available_airports = df[df['Fly_date'].dt.year == selected_year]['Origin_airport'].unique().tolist()
        return available_airports

    @reactive.effect
    def update_airport_choices():
        airports = get_available_airports()
        ui.update_selectize("airport",choices=airports)

    @reactive.calc
    def get_plot_data():
        selected_airport = input.airport.get()
        selected_year = input.selected_year.get()
        filtered_data = df[df['Origin_airport'] == selected_airport]
        filtered_data = filtered_data[filtered_data['Fly_date'].dt.year == selected_year]
        return filtered_data.groupby('Fly_date').size()
    
    @reactive.calc
    def get_plot_data2():
        selected_airport = input.airport.get()
        selected_year = input.selected_year.get()
        filtered_data = df[df['Destination_airport'] == selected_airport]
        filtered_data = filtered_data[filtered_data['Fly_date'].dt.year == selected_year]
        return filtered_data.groupby('Fly_date').size()

    @reactive.calc
    def get_airport_info():
        selected_airport = input.airport.get()
        airport_info = df[df['Origin_airport'] == selected_airport].iloc[0]
        return airport_info

    @reactive.calc
    def get_origin_city():
        airport_info = get_airport_info()
        return airport_info['Origin_city'] 

    @reactive.calc
    def get_destination_data():
        selected_airport = input.airport.get()
        selected_year = input.selected_year.get()
        destination_data = df[(df['Origin_airport'] == selected_airport) & (df['Fly_date'].dt.year == selected_year)]
        destination_data['Fly_date'] = pd.to_datetime(destination_data['Fly_date']).dt.strftime('%Y-%m-%d')
        destination_data = destination_data[[
            'Fly_date', 'Destination_city', 'Destination_airport', 'Passengers', 'Seats', 
            'Destination_population', 'Dest_airport_lat', 'Dest_airport_long'
        ]]
        return destination_data
    
    @reactive.calc
    def get_origin_data():
        selected_airport = input.airport.get()
        selected_year = input.selected_year.get()
        destination_data = df[(df['Destination_airport'] == selected_airport) & (df['Fly_date'].dt.year == selected_year)]
        destination_data['Fly_date'] = pd.to_datetime(destination_data['Fly_date']).dt.strftime('%Y-%m-%d')
        destination_data = destination_data[[
            'Fly_date', 'Origin_city', 'Origin_airport', 'Passengers', 'Seats', 
            'Origin_population', 'Org_airport_lat', 'Org_airport_long'
        ]]
        return destination_data

    @render.plot
    def departure_vs_date_plot():
        data = get_plot_data()
        if data is None:
            return None
        
        fig, ax = plt.subplots(figsize=(13, 3)) 
        data.plot(ax=ax, kind='bar', color='skyblue')
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Flights")
        ax.set_title(f"Departure Airport: {input.airport.get()} ({input.selected_year.get()})")
        
        x_ticks = data.index.strftime('%b %Y').tolist()
        ax.set_xticks(range(len(x_ticks)))
        ax.set_xticklabels(x_ticks)
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig
    
    @render.plot
    def arrival_vs_date_plot():
        data = get_plot_data2()
        if data is None:
            return None
        
        fig, ax = plt.subplots(figsize=(13, 3))  
        data.plot(ax=ax, kind='bar', color='skyblue')
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Flights")
        ax.set_title(f"Arrival Airport: {input.airport.get()} ({input.selected_year.get()})")
        
        x_ticks = data.index.strftime('%b %Y').tolist()
        ax.set_xticks(range(len(x_ticks)))
        ax.set_xticklabels(x_ticks)
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return fig

    @output
    @render.text
    def airport_lat_label():
        airport_info = get_airport_info()
        return f"Latitude: {airport_info['Org_airport_lat']}"

    @output
    @render.text
    def airport_long_label():
        airport_info = get_airport_info()
        return f"Longitude: {airport_info['Org_airport_long']}"

    @output
    @render.text
    def airport_city_label():
        origin_city = get_origin_city()
        return f"Airport City: {origin_city}"

    @output
    @render.data_frame
    def destination_data_table():
        destination_data = get_destination_data()
        return destination_data
    
    @output
    @render.data_frame
    def origin_data_table():
        destination_data = get_origin_data()
        return destination_data
    
    @render_widget
    def map():
        selected_airport = input.airport.get()
        airport_info = df[df["Origin_airport"] == selected_airport].iloc[0]
        latitude = airport_info['Org_airport_lat']
        longitude = airport_info['Org_airport_long']

        if pd.isnull(latitude) or pd.isnull(longitude):
            return "Latitude and Longitude not available for the selected airport."

        m = Map(center=(latitude, longitude), zoom=12)
        marker = Marker(location=(latitude, longitude), draggable=True)
        m.add_layer(marker)

        return m
    
    @reactive.calc
    def get_top_10_airports():
        selected_year = input.selected_year.get()
        top_airports = df[df['Fly_date'].dt.year == selected_year]['Origin_airport'].value_counts().head(10)
        return top_airports.reset_index().rename(columns={'index': 'Index', 'Origin_airport': 'Airport', 'count': 'Number of Flights'})

    @output
    @render.data_frame
    def top_10_airports():
        top_airports_data = get_top_10_airports()
        return top_airports_data
    
    @reactive.calc
    def get_departures_and_arrivals_data():
        selected_airport = input.airport.get()
        departures_data = df[df['Origin_airport'] == selected_airport]
        arrivals_data = df[df['Destination_airport'] == selected_airport]
        departures_by_year = departures_data.groupby(departures_data['Fly_date'].dt.year).size()
        arrivals_by_year = arrivals_data.groupby(arrivals_data['Fly_date'].dt.year).size()
        return pd.DataFrame({'Year': departures_by_year.index, 'Departures': departures_by_year.values, 'Arrivals': arrivals_by_year.values})

    @render.plot
    def departures_and_arrivals():
        data = get_departures_and_arrivals_data()
        if data is None:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 4))
        bar_width = 0.35
        bar1 = ax.bar(data['Year'] - bar_width/2, data['Departures'], bar_width, label='Departures')
        bar2 = ax.bar(data['Year'] + bar_width/2, data['Arrivals'], bar_width, label='Arrivals')
        
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Flights')
        ax.set_title(f'Departures and Arrivals Over Time for {input.airport.get()}')
        ax.set_xticks(data['Year'])
        ax.legend()
        
        plt.tight_layout()
        return fig



initial_departure_airports = df[df['Fly_date'].dt.year == 2000]['Origin_airport'].unique().tolist()
app_ui = create_app_ui(initial_departure_airports)

app = App(app_ui, server)