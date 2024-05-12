# Traveler's Diary API

## API Design
This section shows the Overall REST API design in a tabular format. This provides an easier reference to the API and the
API design of the service.

### User profile API
This section show the user profile API endpoints with the HTTP method, intended operation and the target view in a possible
user interface.

| HTTP   | URI           | Operation            | View    | Comment                     |
|--------|---------------|----------------------|---------|-----------------------------|
| GET    | /profiles     | List all profiles    | List    |                             |
| POST   | /profiles     | Create user profile  | List    | Triggered by user creation  |
| GET    | /profiles/:id | Get profile by id    | Details |                             |
| PUT    | /profiles/:id | Update profile by id | Details |                             |
| DELETE | /profiles/:id | Delete profile by id | Details | Admin performs the deletion |

