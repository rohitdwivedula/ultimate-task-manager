# URL - BASE_URL/api/auth/

Some of these views require users to be logged in to access. Requests made to such views must contain a header with key `Authorization` and value `Bearer {{access_token}}`, where `access_token` is a valid, non-expired access token. If the token is not valid (eg: expired, refresh token is sent instead of access token etc), then a `401 Unauthorized` is returned. After a user has signed up the account will not be active until the email has been verified. 

Backend Developer Note: Use @permission_classes([IsAuthenticated]) decorator for adding the JWT auth to a view. This isn't added to the default permission class so that the login and signup views aren't JWT authenticated.

## [POST] /signup/

Endpoint for registering a new user. 
**Request Format:**
```
{
    "email": "test@gmail.com",
    "password": "123456789",
    "first_name": "John",
    "last_name": "Smith"
}
```

**Response**:
* *Status 200*: User creation successful. Returns message saying `{"Message": "User creation successful."}`.
* *Status 400*: User already exists, or poorly formatted request. eg. `{"ERROR": "User already exists"}`

## [POST] /login/

Login an existing user. Works only if email has been verified.
**Request Format:**
```
{
    "email": "ghost@gmail.com",
    "password": "123456789",
}
```

**Response**:
* *Status 200*: User creation successful. Returns:
  * `access`: an access token
  * `refresh`: a refresh token
* *Status 403*: Incorrect username or password, or email not verified yet. `{"ERROR": "Invalid email or password"}` (or) email not verified yet `{"ERROR": "Email not verified"}`
* *Status 400*: Bad request.

## [POST] /reset/ (login required)  

Reset password of a user.

**Request Format:**
```
{
	"password": "{{new_password}}"
}
```

**Response**:
* *Status 200*: `{"STATUS": "Password reset successful"}`
* *Status 206*: Password not changed due to missing attributes. Contains a key `MISSING` with a list of missing attributes.

## [POST] /refresh/
Refresh an `access_token` and `refresh_token` using a valid `refresh_token`. The `refresh_token` and outstanding `access_token` are revoked.

**Request Format:**
```
{
   "refresh": "{{refresh_token}}"
}
```

**Response**:
* *Status 200*: Returns:
  *  `access`: a refreshed access token. 
  *  `refresh`: a refreshed access token.

* *Status 400*: Not refreshed due to some error. Might be poor formatting or already expired token. The response will usually contain more detailed information about the error. 

## [GET] /me/ (requires login)

Returns the basic information of current user. Response format:

```
{
    "first_name": "Test", 
    "last_name": "User", 
    "bio": "This is my bio", 
    "email": "test@gmail.com"
}
```


## [POST] /me/ (requires login)

Update user information: `first_name, last_name, bio`. Only send the attributes that need to be updated (you can edit only first name by just sending `{"first_name": "New Name Here"}` as the post body. 

```
{
   "first_name": "ardula",
   "last_name": "testing123"
   "bio": "This is a new bio."
}
```

**Response**:
* *Status 200*: `"{"OK": "Updated"}`

## [GET & POST] /forgot/

Firstly send a GET request with `"email"` address in the request. This will trigger an email to be sent to the associated email address if it exists. The endpoint will return a message saying `{"SUCCESS": "Email sent, if associated account exists."}` usually. Email sending is rate limited to once every five minutes, and HTTP 429 (TOO_MANY_REQUESTS) will be raised if a user tries too many times. 

Next, send a POST request to the same endpoint with three attributes: `email`, `password` and `otp`. `password` must contain the new password. If the OTP is valid, the password will be set to the value sent and HTTP 200 status will be returned. If any attributes are missing a HTTP 206 will result (PARTIAL_CONTENT). If the OTPs are not equal a HTTP 403 will be generated. 

The backend server currently does not check the password's strength, nor does it check if password==confirm_password. Even trivial passwords like "123" will also be acceptable by the backend, and will be updated as long as the OTP is valid. Recommended to check strength of password and also verify if password and confirm_password are the same in frontend itself. 

## [GET] /verify/

Used for verifying the email address in the initial signup flow. The link with user `email` and `token` will be created and sent to email - when user clicks on it, it will be verified. 