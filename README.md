# CS 498 E2E Final Project (sp24) repo for NetID: rudhib2

GitHub username at initialization time: rudhib2

For next steps, please refer to the instructions provided by your course.

**Flight Data Dashboard**

**Statement of Purpose:**
The Flight Data Dashboard is designed to provide insights and visualizations into flight data, including departures, arrivals, top airports, and trends over time. It aims to offer users a convenient way to explore and analyze flight information for different airports and years.

**Domain Context:**
Air travel is a crucial aspect of modern transportation and has a significant impact on global connectivity and commerce. Understanding flight patterns, trends, and airport activity is valuable for various stakeholders, including airlines, airport authorities, travel agencies, and travelers themselves. The Flight Data Dashboard leverages data analysis and visualization techniques to present flight data in an intuitive and informative manner, facilitating better decision-making and understanding within the aviation domain.

**Setup Instructions:**

**VERY IMPORTANT**

The dataset I'm using is too big to upload to GitHub so please download it from this link: https://www.kaggle.com/datasets/flashgordon/usa-airport-dataset and save it within the same folder sp24_cs498e2e-final_rudhib2 as Airports.csv for the code to work

1. **Prerequisites:**
   - Python 3.11 installed on your system.
   - Ensure you have the required Python packages installed. You can install them using pip:
     ```
     pip install -r requirements.txt
     ```
2. **Clone the Repository:**
   ```
   git clone https://github.com/illinois-cs-coursework/sp24_cs498e2e-final_rudhib2.git
   ```
3. **Navigate to the Project Directory:**
   ```
   cd sp24_cs498e2e-final_rudhib2
   ```
4. **Run the Application:**
   ```
   python app.py
   ```
5. **Access the Dashboard:**
   Open your web browser and navigate to http://localhost:5000

**Usage Examples:**
- **Exploring Departures and Arrivals:**
  - Select an airport from the dropdown menu.
  - Use the slider to choose the desired year.
  - View the departure and arrival trends for the selected airport and year.
- **Analyzing Top 10 Airports:**
  - Navigate to the "Top 10 Airports" section to see the busiest airports for the selected year.
- **Visualizing Flight Data Over Time:**
  - Explore the "Departures and Arrivals Over Time" section to observe how flight activity has changed over the years.
- **Interactive Map:**
  - Click on the map to view the selected airport's location.
  - The marker on the map represents the latitude and longitude of the chosen airport.
