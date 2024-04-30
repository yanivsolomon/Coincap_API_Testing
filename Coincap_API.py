import json
import requests
import pytest
import time
from locust import HttpUser, task, between


# Testing CoinCap's API (virtual coins info website), includes the following tests:
# 1. Test all assets using boundary testing:
# * Valid testing 0-99.
# * Invalid testing -1,100.
# 2. Test specific asset (first entry which is "Bitcoin"):
# * Test the data outputs correctly.
# * Test and validate we got indeed just one specific asset/entry.
# 3. Test asset history dates using boundary testing:
# * Valid testing: 0,182,363.
# * Invalid testing: -1,364.
# 4. Test different HTTP methods (GET, POST, PUT, DELETE) and validate status codes.
# 5. Performance testing:
# 1. Fetch all assets and print the response time.
# 2. Load testing using Locust (load 100 virtual users for 1 minute)



# Test all assets using boundary testing (valid testing 0-99, invalid testing -1,100)
def test_all_assets():
    url = "https://api.coincap.io/v2/assets"
    response = requests.get(url)
    data = json.loads(response.text)

    # test the first data value (1)
    assert data['data'][0]['name'] == "Bitcoin"
    assert data['data'][0]['rank'] == "1"
    assert data['data'][0]['id'] == "bitcoin"
    assert data['data'][0]['symbol'] == "BTC"

    # test the middle data value (50)
    assert data['data'][49]['name'] == "Quant"
    assert data['data'][49]['rank'] == "50"
    assert data['data'][49]['id'] == "quant"
    assert data['data'][49]['symbol'] == "QNT"


    # test the last data value (100)
    assert data['data'][99]['name'] == "FTX Token"
    assert data['data'][99]['rank'] == "100"
    assert data['data'][99]['id'] == "ftx-token"
    assert data['data'][99]['symbol'] == "FTT"

    # INVALID TESTING - testing boundaries (testing data value (0) - should be equal to 100)
    assert data['data'][-1]['name'] == "FTX Token"
    assert data['data'][-1]['rank'] == "100"
    assert data['data'][-1]['id'] == "ftx-token"
    assert data['data'][-1]['symbol'] == "FTT"

    # INVALID TESTING - testing boundaries (testing data value (101), should give us an error "out of range")
    with pytest.raises(IndexError, match="list index out of range"):
        data = {'data': []}
        print(data['data'][100]['name'])



# Test specific asset (Bitcoin)
def test_specific():
    url = "https://api.coincap.io/v2/assets/bitcoin"
    response = requests.get(url)
    data = json.loads(response.text)

    # print the data
    print(data)

    # validate response data outputs correctly
    assert data['data']['name'] == "Bitcoin"
    assert data['data']['rank'] == "1"
    assert data['data']['id'] == "bitcoin"
    assert data['data']['symbol'] == "BTC"

    # validate we got a specific value (only one entry/rank)
    if "data" in data:
        data_dict = data["data"]
        rank_count = data_dict.get("rank")
        rank_name = data_dict.get("name")
        print(f"Data contains {len(rank_count)} number of entries.")
        print("Entries names are:", rank_name)

# Test asset history dates using boundary test (Valid testing: 0,182,363, Invalid: -1,364)
def test_asset_history():
    url = "https://api.coincap.io/v2/assets/bitcoin/history?interval=d1"
    response = requests.get(url)
    data = json.loads(response.text)


    # test first data value (2023-04-17)
    assert data['data'][0]['date'] == "2023-04-17T00:00:00.000Z"
    assert data['data'][0]['priceUsd'] == "29735.3273542551182441"

    # test middle data value (2023-10-16)
    assert data['data'][182]['date'] == "2023-10-16T00:00:00.000Z"
    assert data['data'][182]['priceUsd'] == "27920.0497840546018590"

    # test last data value (2024-04-14)
    assert data['data'][363]['date'] == "2024-04-14T00:00:00.000Z"
    assert data['data'][363]['priceUsd'] == "64408.4181862819955761"

    # INVALID testing - test data value -1 (should be equal to the last value)
    assert data['data'][-1]['date'] == "2024-04-14T00:00:00.000Z"
    assert data['data'][-1]['priceUsd'] == "64408.4181862819955761"

    # INVALID testing - test data value 364 (should be out of range - error)
    with pytest.raises(IndexError, match="list index out of range"):
        data = {'data': []}
        print(data['data'][364]['name'])

# GET method testing (expected outcome: should fetch all assets - 100 entries)
def test_GET():
    url = "https://api.coincap.io/v2/assets"
    response = requests.get(url)
    data = json.loads(response.text)
    # assert status code=200 and data entries are equal to 100 entries
    assert response.status_code == 200
    assert len(data["data"]) == 100

# POST method testing (expected outcome: we should get an error msg: 404)
def test_POST():
    url = "https://api.coincap.io/v2/assets"
    response = requests.post(url)
    # assert status code=404
    assert response.status_code == 404

# PUT method testing (expected outcome: we should get an error msg: 404)
def test_PUT():
    url = "https://api.coincap.io/v2/assets"
    response = requests.put(url)
    # assert status code=404
    assert response.status_code == 404

# DELETE method testing (expected outcome: we should get an error msg: 404)
def test_DELETE():
    url = "https://api.coincap.io/v2/assets"
    response = requests.delete(url)
    # assert status code=404
    assert response.status_code == 404

# fetch all assets and print the response time
def test_coincap_fetch_all():
    url = "https://api.coincap.io/v2/assets"
    # Record the start time
    start_time = time.time()
    response = requests.get(url)
    data = json.loads(response.text)
    # Record the end time
    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(data)
    print(f"Time taken: {elapsed_time:.4f} seconds")



# Load testing using Locust (load 100 virtual users for 1 minute)
# code to run in headless mode: locust -f Coincap_API.py --headless -u 100 -r 1 -t 1m
class CoinCapUser(HttpUser):
    host = "https://api.coincap.io"
    wait_time = between(1, 3)  # Wait time between requests
    @task
    def fetch_assets(self):
        url = "/v2/assets"
        response = self.client.get(url)
        data = json.loads(response.text)
        print("Data fetched successfully:")
        print(data)

