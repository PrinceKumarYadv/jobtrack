# JobTrack API Testing Guide (Postman)

Import `JobTrack.postman_collection.json` into Postman, or follow the requests below manually. All examples assume the server is running at `http://127.0.0.1:8000`.

## 1. Register

```
POST /api/register/
Content-Type: application/json

{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "password": "StrongPass123",
  "confirm_password": "StrongPass123"
}
```
**201 Created**
```json
{
  "detail": "Account created successfully.",
  "user": { "id": 1, "full_name": "Jane Doe", "email": "jane@example.com", "created_at": "2026-01-01T10:00:00Z" },
  "tokens": { "access": "<jwt-access-token>", "refresh": "<jwt-refresh-token>" }
}
```

## 2. Login

```
POST /api/login/
Content-Type: application/json

{ "email": "jane@example.com", "password": "StrongPass123" }
```
**200 OK** — same shape as register, minus `full_name`/`confirm_password` in the request.

> Copy the `tokens.access` value — every request below needs it in the `Authorization: Bearer <token>` header.

## 3. Create Application

```
POST /api/applications/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "company_name": "Google",
  "job_title": "Software Engineer Intern",
  "job_type": "Internship",
  "location": "Bengaluru",
  "salary": 600000,
  "job_url": "https://careers.google.com/jobs/123",
  "application_date": "2026-01-15",
  "status": "Applied",
  "priority": "High",
  "notes": "Referred by a friend."
}
```
**201 Created** — returns the full application object with a nested `company` and an empty `interviews` array.

## 4. Get Applications (list, with filters)

```
GET /api/applications/?search=engineer&status=Applied&ordering=-application_date
Authorization: Bearer <access_token>
```
**200 OK**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    { "id": 1, "company_name": "Google", "job_title": "Software Engineer Intern", "location": "Bengaluru",
      "job_type": "Internship", "application_date": "2026-01-15", "status": "Applied", "priority": "High",
      "status_badge_class": "badge-status-applied" }
  ]
}
```

## 5. Get Application Details

```
GET /api/applications/1/
Authorization: Bearer <access_token>
```
**200 OK** — full object, including nested interviews.
**404 Not Found** if the application doesn't exist or belongs to another user.

## 6. Update Application

```
PUT /api/applications/1/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "company_name": "Google",
  "job_title": "Software Engineer Intern",
  "job_type": "Internship",
  "application_date": "2026-01-15",
  "status": "Interview",
  "priority": "High"
}
```
**200 OK**

## 7. Delete Application

```
DELETE /api/applications/1/
Authorization: Bearer <access_token>
```
**204 No Content**

## 8. Create Interview

```
POST /api/interviews/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "application": 1,
  "interview_date": "2026-02-01",
  "interview_time": "10:00:00",
  "interview_type": "Technical",
  "interviewer": "Alex Smith",
  "meeting_link": "https://meet.google.com/xyz",
  "result": "Pending"
}
```
**201 Created**
**400 Bad Request** if `application` belongs to a different user (`{"errors": {"application": ["You do not have access to this application."]}}`).

## 9. Get Interviews

```
GET /api/interviews/
Authorization: Bearer <access_token>
```
**200 OK** — paginated list, each entry includes `company_name` and `job_title` for display convenience.

## 10. Dashboard

```
GET /api/dashboard/
Authorization: Bearer <access_token>
```
**200 OK**
```json
{
  "total_applications": 18,
  "applied": 5, "shortlisted": 3, "interview": 4, "selected": 2, "rejected": 3, "withdrawn": 1,
  "status_breakdown": [{ "status": "Applied", "count": 5 }],
  "applications_over_time": [{ "month": "Jan 2026", "count": 6 }],
  "upcoming_interviews": [{ "id": 1, "company_name": "Google", "job_title": "SWE Intern",
    "interview_date": "2026-09-10", "interview_time": "11:00:00", "interview_type": "Video",
    "meeting_link": "https://meet.google.com/xyz" }],
  "recent_applications": [{ "id": 18, "company_name": "Amazon", "job_title": "Backend Developer",
    "status": "Applied", "application_date": "2026-01-20" }]
}
```

## 11. Profile

```
GET /api/profile/
Authorization: Bearer <access_token>
```
```
PUT /api/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{ "full_name": "Jane A. Doe", "email": "jane@example.com" }
```

## Error Examples

**Invalid login (400):**
```json
{ "detail": "Please correct the errors below.", "errors": { "non_field_errors": ["Invalid email or password."] } }
```

**Unauthenticated (401):**
```json
{ "detail": "Authentication credentials were not provided." }
```

**Accessing another user's application (404):**
```json
{ "detail": "Not found." }
```

**Validation error, e.g. missing job title (400):**
```json
{ "detail": "Please correct the errors below.", "errors": { "job_title": ["Job title is required."] } }
```
