# URL - BASE_URL/api/main/

Endpoints to manage labels, tasks and subtasks. All these endpoints require login/access token. Check `auth.md` for instructions on login and tokens.

## [GET] tasks/
Get a list of tasks of the signed in user - you can filter any of the fields using standard Django Queryset operators (such as `due_on__lte`, `labels=LABEL_UID_HERE` in the GET parameters). The `task` objects will be present in the `data` array. If the development server is on `port 5000`, example requests:

`localhost:5000/api/main/tasks/?page=1` 
`localhost:5000/api/main/tasks/?due_on__gte=2020-05-28T19:46:52&labels=0ea3bb5a-8895-4d01-8094-bbedbf6469d2&page=4`

There will be 15 records displayed per page. 

**Response Format:**
```
Status: HTTP 200
{
    "current_page": "1",
    "total_pages": 2,
    "count": 4,
    "data": [ ... ]
}
```

**Errors**:
A status 400might result if you tried accessing a page whose index is greater than `total_pages`, or you messed up a queryset operator.

## [POST] tasks/
Create a task. All attributes except `labels` are mandatory. All subtasks are initialized as Not Done while adding here. 

**Request Format:**
```
{
  "name": "Finish freelancing project on Pepper Content",
  "desc": "Write a 11,000 word article on how to fight coronavirus with social distancing",
  "labels": ["e63c8947-956b-4226-9461-f69e91394229", "0ea3bb5a-8895-4d01-8094-bbedbf6469d2"],
  "due_on": "2020-06-28T19:00:00"
  "subtasks": ["Research on COVID-19", "Prepare draft 1", "Contact client for feedback", "Edit", "Find pics for article"]
}
```

**Sample Response:**
If everything's okay you get a status 200 HTTP OK and this message.
```
{
    "success": "Task created."
}
```
Otherwise, you might get errors like this: (400 Bad Request)
```
{
    "error": "label not found"
}
```

## [GET, POST, DELETE] tasks/<uuid:task_uuid>/
GET a task, update (POST) a task, DELETE a task

## [GET and POST] labels/
GET all labels or create (POST) a new label. POST format:
```
{
  "name": "Family",
  "description": "For everything related to the people you love the most."
}
```

## [GET, POST, DELETE] labels/<uuid:label_uuid>/

## [GET and POST] tasks/<uuid:task_uuid>/subtask
GET all subtasks of a task with UUID `TASK_UID`. Send a POST request to create a subtask:

## [GET, POST, DELETE] subtasks/<uuid:subtask_uuid>/
GET to retrieve info, POST to update, DELETE to remove