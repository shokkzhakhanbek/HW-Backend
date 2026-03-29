import math
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()


cars = [
    {"id": 1, "name": "Toyota Camry", "year": "2020"},
    {"id": 2, "name": "Honda Civic", "year": "2021"},
    {"id": 3, "name": "Ford Taurus", "year": "2019"},
    {"id": 4, "name": "BMW X5", "year": "2022"},
    {"id": 5, "name": "Mercedes C200", "year": "2023"},
    {"id": 6, "name": "Audi A4", "year": "2021"},
    {"id": 7, "name": "Kia Rio", "year": "2020"},
    {"id": 8, "name": "Hyundai Sonata", "year": "2022"},
    {"id": 9, "name": "Chevrolet Malibu", "year": "2019"},
    {"id": 10, "name": "Nissan Altima", "year": "2021"},
    {"id": 11, "name": "Volkswagen Passat", "year": "2020"},
    {"id": 12, "name": "Mazda 6", "year": "2023"},
    {"id": 13, "name": "Subaru Legacy", "year": "2022"},
    {"id": 14, "name": "Tesla Model 3", "year": "2023"},
    {"id": 15, "name": "Lexus ES", "year": "2021"},
]

users = [
    {"id": 1, "email": "test@test.com", "first_name": "Aibek", "last_name": "Bekturov", "username": "deadly_knight95"},
    {"id": 2, "email": "bob@mail.com", "first_name": "Bob", "last_name": "Smith", "username": "bob_smith"},
    {"id": 3, "email": "alice@mail.com", "first_name": "Alice", "last_name": "Johnson", "username": "alice_j"},
    {"id": 4, "email": "john@mail.com", "first_name": "John", "last_name": "Doe", "username": "john_doe"},
    {"id": 5, "email": "sara@mail.com", "first_name": "Sara", "last_name": "Connor", "username": "sara_c"},
    {"id": 6, "email": "mike@mail.com", "first_name": "Mike", "last_name": "Wilson", "username": "mike_w"},
    {"id": 7, "email": "anna@mail.com", "first_name": "Anna", "last_name": "Lee", "username": "anna_lee"},
    {"id": 8, "email": "david@mail.com", "first_name": "David", "last_name": "Brown", "username": "david_b"},
    {"id": 9, "email": "emma@mail.com", "first_name": "Emma", "last_name": "Davis", "username": "emma_d"},
    {"id": 10, "email": "alex@mail.com", "first_name": "Alex", "last_name": "Taylor", "username": "alex_t"},
    {"id": 11, "email": "kate@mail.com", "first_name": "Kate", "last_name": "Miller", "username": "kate_m"},
    {"id": 12, "email": "tom@mail.com", "first_name": "Tom", "last_name": "Anderson", "username": "tom_a"},
]


@app.get("/cars")
def get_cars(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    return cars[start:end]


@app.get("/cars/{car_id}")
def get_car(car_id: int):
    for car in cars:
        if car["id"] == car_id:
            return car
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/users", response_class=HTMLResponse)
def get_users(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    page_users = users[start:end]
    total_pages = math.ceil(len(users) / limit)

    rows = ""
    for user in page_users:
        name = user["first_name"] + " " + user["last_name"]
        rows += "<tr>"
        rows += "<td>" + user["username"] + "</td>"
        rows += '<td><a href="/users/' + str(user["id"]) + '">' + name + "</a></td>"
        rows += "</tr>"

    pagination = ""
    for p in range(1, total_pages + 1):
        if p == page:
            pagination += " <b>" + str(p) + "</b> "
        else:
            pagination += ' <a href="/users?page=' + str(p) + '&limit=' + str(limit) + '">' + str(p) + "</a> "

    html = """
    <html>
    <body>
        <h1>Users</h1>
        <table border="1">
            <tr>
                <th>Username</th>
                <th>Full Name</th>
            </tr>
            """ + rows + """
        </table>
        <br>
        <p>Pages: """ + pagination + """</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/users/{user_id}", response_class=HTMLResponse)
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            html = """
            <html>
            <body>
                <h1>""" + user["first_name"] + " " + user["last_name"] + """</h1>
                <p>ID: """ + str(user["id"]) + """</p>
                <p>Email: """ + user["email"] + """</p>
                <p>Username: """ + user["username"] + """</p>
                <br>
                <a href="/users">Back to list</a>
            </body>
            </html>
            """
            return HTMLResponse(content=html)

    raise HTTPException(status_code=404, detail="Not found")