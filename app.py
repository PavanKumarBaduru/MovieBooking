import mysql.connector, sys
import datetime
from mysql.connector import Error
from flask import Flask, request, jsonify, render_template
from random import randint
import pyodbc

app = Flask(__name__)

@app.route('/')
def renderLoginPage():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def verifyAndRenderRespective():
    username = request.form['username']
    password = request.form['password']

    try:
        if username == 'cashier' and password == 'cashier123':
            res = runQuery('call delete_old()')
            return render_template('cashier.html')

        elif username == 'manager' and password == 'Password@123':
            res = runQuery('call delete_old()')
            return render_template('manager.html')

        else:
            return render_template('loginfail.html')
    except Exception as e:
        print(e)
        return render_template('loginfail.html')


# Routes for cashier
@app.route('/getMoviesShowingOnDate', methods=['POST'])
def moviesOnDate():
    date = request.form['date']

    res = runQuery("SELECT DISTINCT movie_id,movie_name,type FROM movies NATURAL JOIN shows WHERE Date = '" + date + "'")

    if res == []:
        return '<h4>No Movies Showing</h4>'
    else:
        return render_template('movies.html', movies=res)


@app.route('/getTimings', methods=['POST'])
def timingsForMovie():
    date = request.form['date']
    movieID = request.form['movieID']
    movieType = request.form['type']

    res = runQuery("SELECT time FROM shows WHERE Date='" + date + "' and movie_id = " + movieID + " and type ='" + movieType + "'")
    
    list = []

    for i in res:
        list.append((i[0], int(i[0] / 100), i[0] % 100 if i[0] % 100 != 0 else '00'))

    return render_template('timings.html', timings=list)


@app.route('/getShowID', methods=['POST'])
def getShowID():
    date = request.form['date']
    movieID = request.form['movieID']
    movieType = request.form['type']
    time = request.form['time']

    res = runQuery("SELECT show_id FROM shows WHERE Date='" + date + "' and movie_id = " + movieID + " and type ='" + movieType + "' and time = " + time)
    return jsonify({"showID": res[0][0]})


@app.route('/getAvailableSeats', methods=['POST'])
def getSeating():
    showID = request.form['showID']

    res = runQuery("SELECT class,no_of_seats FROM shows NATURAL JOIN halls WHERE show_id = " + showID)

    totalGold = 0
    totalStandard = 0

    for i in res:
        if i[0] == 'gold':
            totalGold = i[1]
        if i[0] == 'standard':
            totalStandard = i[1]

    res = runQuery("SELECT seat_no FROM booked_tickets WHERE show_id = " + showID)

    goldSeats = []
    standardSeats = []

    for i in range(1, totalGold + 1):
        goldSeats.append([i, ''])

    for i in range(1, totalStandard + 1):
        standardSeats.append([i, ''])

    for i in res:
        if i[0] > 1000:
            goldSeats[i[0] % 1000 - 1][1] = 'disabled'
        else:
            standardSeats[i[0] - 1][1] = 'disabled'

    return render_template('seating.html', goldSeats=goldSeats, standardSeats=standardSeats)


@app.route('/getPrice', methods=['POST'])
def getPriceForClass():
    showID = request.form['showID']
    seatClass = request.form['seatClass']

    res = runQuery("SELECT price FROM shows NATURAL JOIN price_listing WHERE show_id = " + showID)

    if res == []:
        return '<h5>Prices Have Not Been Assigned To This Show, Please Try Again Later!</h5>'

    price = int(res[0][0])
    if seatClass == 'gold':
        price = price * 1.5

    return '<h5>Ticket Price: $ ' + str(price) + '</h5><button onclick="confirmBooking()" class="btn-warning">Confirm Booking</button>'


@app.route('/insertBooking', methods=['POST'])
def createBooking():
    showID = request.form['showID']
    seatNo = request.form['seatNo']
    seatClass = request.form['seatClass']

    if seatClass == 'gold':
        seatNo = int(seatNo) + 1000

    ticketNo = 0
    res = None

    while res != []:
        ticketNo = randint(0, 2147483646)
        res = runQuery("SELECT ticket_no FROM booked_tickets WHERE ticket_no = " + str(ticketNo))
    
    res = runQuery("INSERT INTO booked_tickets VALUES(" + str(ticketNo) + "," + showID + "," + str(seatNo) + ")")

    if res == []:
        return '<h5>Ticket Has Been Booked Successfully!</h5><h6>Ticket Number: ' + str(ticketNo) + '</h6>'


# Routes for manager
@app.route('/getShowsShowingOnDate', methods=['POST'])
def getShowsOnDate():
    date = request.form['date']

    res = runQuery("SELECT show_id,movie_name,type,time FROM shows NATURAL JOIN movies WHERE Date = '" + date + "'")
    
    if res == []:
        return '<h4>No Shows Showing</h4>'
    else:
        shows = []
        for i in res:
            x = i[3] % 100
            if i[3] % 100 == 0:
                x = '00'
            shows.append([i[0], i[1], i[2], int(i[3] / 100), x])

        return render_template('shows.html', shows=shows)


@app.route('/getBookedWithShowID', methods=['POST'])
def getBookedTickets():
    showID = request.form['showID']

    res = runQuery("SELECT ticket_no,seat_no FROM booked_tickets WHERE show_id = " + showID + " order by seat_no")

    if res == []:
        return '<h5>No Bookings!!</h5>'

    tickets = []
    for i in res:
        if i[1] > 1000:
            tickets.append([i[0], i[1] - 1000, 'Gold'])
        else:
            tickets.append([i[0], i[1], 'Standard'])

    return render_template('bookedtickets.html', tickets=tickets)


@app.route('/fetchMovieInsertForm', methods=['GET'])
def getMovieForm():
    return render_template('movieform.html')


@app.route('/insertMovie', methods=['POST'])
def insertMovie():
    movieName = request.form['movieName']
    movieLen = request.form['movieLen']
    movieLang = request.form['movieLang']
    types = request.form['types']
    startShowing = request.form['startShowing']
    endShowing = request.form['endShowing']

    res = runQuery('SELECT * FROM movies')

    for i in res:
        if i[1] == movieName and i[2] == int(movieLen) and i[3] == movieLang and i[4].strftime('%Y/%m/%d') == startShowing and i[5].strftime('%Y/%m/%d') == endShowing:
            return '<h5>The Same Movie Already Exists</h5>'

    movieID = 0
    res = None

    while res != []:
        movieID = randint(0, 2147483646)
        res = runQuery("SELECT movie_id FROM movies WHERE movie_id = " + str(movieID))
    
    res = runQuery("INSERT INTO movies VALUES(" + str(movieID) + ",'" + movieName + "'," + movieLen + ",'" + movieLang + "','" + startShowing + "','" + endShowing + "')")

    if res == []:
        print("Was able to add movie")
        subTypes = types.split(' ')

        while len(subTypes) < 3:
            subTypes.append('NUL')

        res = runQuery("INSERT INTO types VALUES(" + str(movieID) + ",'" + subTypes[0] + "','" + subTypes[1] + "','" + subTypes[2] + "')")

        if res == []:
            return '<h5>Movie Added Successfully!</h5><h6>Movie ID: ' + str(movieID) + '</h6>'
        else:
            print(res)
    else:
        print(res)

    return '<h5>Something Went Wrong</h5>'


@app.route('/getValidMovies', methods=['POST'])
def validMovies():
    startDate = request.form['startDate']
    endDate = request.form['endDate']

    res = runQuery("SELECT movie_id,movie_name FROM movies WHERE start_showing <= '" + startDate + "' and end_showing >= '" + endDate + "'")

    if res == []:
        return '<h4>No Movies Available</h4>'
    else:
        return render_template('validmovies.html', validMovies=res)


def runQuery(query):
    conn = None
    try:
        # Updated connection string for Azure SQL
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'Server=tcp:movieticketbooking.database.windows.net,1433;'
            'Database=GROUP16;'
            'Uid=Sampreeth;'
            'Pwd={Pavan@123};'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )
        cursor = conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        conn.commit()
        return res
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)