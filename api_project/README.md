## Obtaining an Authentication Token (Postman)

1.  Open Postman.
2.  Set the request method to `POST`.
3.  Enter the URL: `http://127.0.0.1:8000/api-token-auth/` (or your API's token endpoint).
4.  Go to the "Body" tab.
5.  Select "raw" and then "JSON" from the dropdown.
6.  Enter the following JSON in the body:

    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

7.  Click "Send."
8.  The response will contain your authentication token in the JSON body, under the "token" key. Copy this token.

## Using the Token in Requests (Postman)

1.  In Postman, for any request that requires authentication, go to the "Authorization" tab.
2.  Select "Token" from the "Type" dropdown.
3.  Paste your authentication token into the "Token" field.
4.  Now, when you send the request, Postman will include the token in the `Authorization` header.

## Permission Rules

* `/api/books/` (GET, POST, PUT, DELETE):
    * Requires authentication (`IsAuthenticated`).

    **Testing with Postman:**

    * **Without Token:**
        1.  Open Postman.
        2.  Set the request method to `GET`.
        3.  Enter the URL: `http://127.0.0.1:8000/api/books/`.
        4.  Click "Send."
        5.  You should receive a `401 Unauthorized` response.

    * **With Token:**
        1.  Follow the "Using the Token in Requests (Postman)" instructions.
        2.  Send the same request again.
        3.  You should receive a `200 OK` response with the list of books.

