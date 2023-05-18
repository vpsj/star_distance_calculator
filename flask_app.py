# Flask Program to Calculate the distance between any two Stars
import MySQLdb
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, session
from math import sin, cos, acos, pi, sqrt, acosh, asinh, sinh

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'vpsj.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'vpsj'
app.config['MYSQL_PASSWORD'] = 'Imcoolest&26'
app.config['MYSQL_DB'] = 'vpsj$star_catalog'
mysql  = MySQL(app)

@app.route('/', methods=['POST', 'GET'])
def main():
    #if request.method='POST' and 'Star1' in request.form and 'Star2' in request.form:
    X=''
    Y=''
    distance=''
    tyears=''
    Tyears=''
    t2years=''
    T2years=''
    Star1=''
    Star2=''
    R1 = ''
    R2 = ''
    Star1 = request.form.get("Star1")
    Star2 = request.form.get("Star2")
    X=RA(Star1)
    Y=RA(Star2)
    R1=15*float(RA(Star1) or 0)
    R2=15*float(RA(Star2) or 0)
    D1=float(Dec(Star1) or 0)
    D2=float(Dec(Star2) or 0)
    P1=3.26*float(Dist(Star1) or 0)
    P2=3.26*float(Dist(Star2) or 0)
    if (R1==R2 and D1==D2 and P1==P2):
        return render_template('index.html', R1=R1, R2=R2)
    else:
     ans=acos(sin(D1*pi/180)*sin(D2*pi/180) + cos(D1*pi/180)*cos(D2*pi/180)*cos((R1-R2)*pi/180))
     distance=round((sqrt(pow(P1,2)+pow(P2,2)-2*P1*P2*cos(ans))),3)
     d=distance*9.461*pow(10,15)
     c= 300000000
     a=9.80665
     t = sqrt(pow((d/c),2) + 2*(d/a))
     T=c/a * acosh(a*d/pow(c,2) + 1)
     tyears=round(t/(31536000),3)
     Tyears=round(T/(3.156*pow(10,7)),3)
     t2 = sqrt(pow((d/c),2) + 4*(d/a))
     T2=2*(c/a) * acosh(a*d/pow(c,2) + 1)
     t2years=round(t2/(31536000),3)
     T2years=round(T2/(3.156*pow(10,7)),3)
     return render_template('index.html', X=X,Y=Y, distance=distance, tyears=tyears, Tyears=Tyears, t2years=t2years, T2years=T2years, Star1=str(Star1), Star2=str(Star2))


def RA(Name):
    Name = str(Name).lower()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT ra FROM star_distance WHERE proper=%s OR hip=%s OR hd=%s OR hr=%s OR gl=%s OR bf=%s OR alt1=%s OR alt2=%s OR alt3=%s",
        (Name, Name, Name, Name, Name, Name, Name, Name, Name))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    cur.close()

def Dist(Name):
    Name = str(Name).lower()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT dist FROM star_distance WHERE proper=%s OR hip=%s OR hd=%s OR hr=%s OR gl=%s OR bf=%s OR alt1=%s OR alt2=%s OR alt3=%s",(Name,Name,Name,Name,Name,Name,Name,Name,Name))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    cur.close()


def Dec(Name):
    Name = str(Name).lower()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT declination FROM star_distance WHERE proper=%s OR hip=%s OR hd=%s OR hr=%s OR gl=%s OR bf=%s OR alt1=%s OR alt2=%s OR alt3=%s",
        (Name, Name, Name, Name, Name, Name, Name, Name, Name))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    cur.close()

"""
#Original csv program

def RA(Name):
    Name=str(Name).lower()
    file = open('/home/vpsj/star catalog.csv')
    for row in csv.reader(file):
        if any(row[col].lower() == Name for col in range(1, 7)):
         return float(row[7])
    #return render_template('index.html', Name=str(Name))


def Dec(Name):

    Name=str(Name).lower()
    file = open('/home/vpsj/star catalog.csv')
    for row in csv.reader(file):
        if any(row[col].lower() == Name for col in range(1,7)):
            return float(row[8])



def Dist(Name):

    Name=str(Name).lower()
    file = open('/home/vpsj/star catalog.csv')
    for row in csv.reader(file):
        if any(row[col].lower() == Name for col in range(1, 7)):
            return float(row[9])


"""

if __name__ == "__main__":
    # Launch the Flask dev server
    app.run()