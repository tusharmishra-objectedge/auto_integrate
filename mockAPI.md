# Mock API guide

### Mock REST APIs created using mockapi.io

URL : https://651313e18e505cebc2e98c43.mockapi.io

Two resources have been created at the above URL for testing purposes.

Resource 1: /students

Resource 2: /pupils

Some of their fields are have the same name and some are different.
The type of the analogous fields have been kept the same.
For example: `student['name']` is the same type as `pupil['fullName']`.

### Methods:

**Get:** <br>
Resource 1: /students <br>
Resource 2: /pupils

**Get by ID:** <br>
Resource 1: /students/:id <br>
Resource 2: /pupils/:id

**Post:** <br>
Resource 1: /students <br>
Resource 2: /pupils

**Put:** <br>
Resource 1: /students/:id <br>
Resource 2: /pupils/:id

**Delete:** <br>
Resource 1: /students/:id <br>
Resource 2: /pupils/:id

### Resource Schema:
**students**

`{
    "createdAt": string,
    "name": string,
    "dateOfBirth": string,
    "address": string,
    "state": string,
    "city": string,
    "honors": boolean,
    "grade": number,
    "emergencyContact": string,
    "id": string
}`

**pupils**

`{ 
    "fullName": string,
    "emergencyContactNumber": string,
    "DoB": string,
    "city": string,
    "state": string,
    "street": string,
    "score": number,
    "honorStudent": boolean,
    "created": string,
    "id": string
}`

### Ideal Matching:

| student     | pupil        |
|-------------|--------------|
| id          | id           |
| name        | fullName     |
| dateOfBirth | DoB          |
| address     | street       |
| city        | city         |
| state       | state        |
| honors      | honorStudent |
| grade       | score        |
| createdAt   | created      |



