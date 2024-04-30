API Testing for CoinCap.io

This API testing was created using Python, Locust and the Pytest framework. It encompasses the following tests:

Testing CoinCap's API (virtual coins info website), includes the following tests:
1. Test all assets using boundary testing:
* Valid testing 0-99.
* Invalid testing -1,100.
2. Test specific asset (first entry which is "Bitcoin"):
* Test the data outputs correctly.
* Test and validate we got indeed just one specific asset/entry.
3. Test asset history dates using boundary testing:
* Valid testing: 0,182,363.
* Invalid testing: -1,364.
4. Test different HTTP methods (GET, POST, PUT, DELETE) and validate status codes.
5. Performance testing:
 * Fetch all assets and print the response time.
 * Load testing using Locust (load 100 virtual users for 1 minute).
