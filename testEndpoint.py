import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_livability_score(test_case):
    """Sends a test case to the livability score endpoint and prints the result."""
    headers = {'Content-Type': 'application/json'}
    
    # Use a requests session to persist cookies across requests
    with requests.Session() as session:
        # Send preferences directly, not nested inside 'preferences' key
        print(f"Sending preferences: {test_case}")
        response = session.post(f"{BASE_URL}/preferences", headers=headers, data=json.dumps(test_case))
        
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Error: Received non-JSON response from the server:\n{response.text}")
            return
        
        if response.status_code == 200 and response_json.get('success'):
            # Now request the livability score
            score_response = session.get(f"{BASE_URL}/livability")
            try:
                score_json = score_response.json()
                if score_response.status_code == 200:
                    print(f"Test Case: {test_case}")
                    print(f"Livability Score: {score_json['score']}\n")
                else:
                    print(f"Error in getting score: {score_json}\n")
            except requests.exceptions.JSONDecodeError:
                print(f"Error: Received non-JSON response from the server:\n{score_response.text}")
        else:
            print(f"Error in setting preferences: {response_json}\n")

if __name__ == "__main__":
    # Define a set of test cases
    test_cases = [
        {
            'city': 'New York',
            'aqi': 0,
            'carbon_intensity': 50,
            'environmental_stance': 'Pro',
            'heat_index_temp': 62.2,
            'wind_mph': 5
        },
        {
            'city': 'Los Angeles',
            'aqi': 500,
            'carbon_intensity': 450,
            'environmental_stance': 'Anti',
            'heat_index_temp': 100,
            'wind_mph': 50
        }
    ]
    
    # Loop through the test cases
    for case in test_cases:
        test_livability_score(case)
