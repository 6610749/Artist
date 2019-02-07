from flask import request , render_template , flash , redirect, url_for , session
from app.models import Artist , Performance , Omgevinf
from app import app , db
from datetime import datetime 

@app.route("/", methods=['GET','POST'])
def hello():
    artists = Artist.query.all() 
    omgevings = Omgevinf.query.all() 
    return render_template('index.html',artists=artists,omgevings=omgevings)

@app.route("/zoeken")
def zoeken():
    artiestId = request.args.get('artiest',default=None)
    datumStart = request.args.get('datumStart',default=None)
    datumEnd = request.args.get('datumEnd',default=None)
    datumOne = request.args.get('datumOne',default=None)
    omgevingId = request.args.get('omgeving',default=None)
    dateType = request.args.get('customRadio',default='oneDate')



    # Convert html Date to Python Date
    dateOne = None
    dateStart = None
    dateEnd = None

    if dateType == 'oneDate':
        try:
            dateOne = datetime.strptime(datumOne, "%d/%m/%Y").date()
        except: 
            pass
    elif dateType == 'rangeDate':
        try:
            dateStart = datetime.strptime(datumStart, "%d/%m/%Y").date()
        except: 
            pass
        
        try:
            dateEnd = datetime.strptime(datumEnd, "%d/%m/%Y").date()
        except:
            pass
    # End convert

    
    performances = Performance.query.filter()
    if artiestId :
        performances = performances.filter(Performance.artists.any(Artist.id == artiestId))
    if dateType == 'oneDate' and dateOne:
        performances = performances.filter_by(date = dateOne )
    else:
        if dateStart and dateEnd:
            performances = performances.filter(Performance.date >= dateStart ).filter(Performance.date <= dateEnd)

    if omgevingId :
        performances = performances.filter(Performance.omgevinf==Omgevinf.query.get(omgevingId) )


    # Pagination 
    page = request.args.get('page' , 1 , type=int)
    next_url = None
    prev_url = None

    total = 0  
    
    if performances : 
        total = len(performances.all())
        performances = performances.paginate(
        page , app.config['RESULT_PER_PAGE'] , False  )

        next_url = url_for('zoeken' ,artiestId=artiestId,datumStart=datumStart,datumEnd=datumEnd,omgevingId=omgevingId,dateOne=dateOne,  page=performances.next_num) if performances.has_next else None
        prev_url = url_for('zoeken' ,artiestId=artiestId,datumStart=datumStart,datumEnd=datumEnd,omgevingId=omgevingId,datumOne=dateOne , page=performances.prev_num)  if performances.has_prev else None
    
    # End Pagination
    artiest = None
    if artiestId :
        artiest = Artist.query.get(artiestId)

    return render_template('zoeken.html',performances=performances.items,
                artiest=artiest,total=total ,
                 next_url=next_url,
                 prev_url=prev_url)

@app.route('/artist/<int:artiestId>')
def getPerformances(artiestId):
    
    artiest = Artist.query.filter_by(id=artiestId).first_or_404() 
    performances = Performance.query.filter(Performance.artists.any(Artist.id == artiestId))

    total = len(performances.all())

    # Pagination 
    page = request.args.get('page' , 1 , type=int)
    next_url = None
    prev_url = None

    performances = performances.paginate(
    page , app.config['RESULT_PER_PAGE'] , False  )

    next_url = url_for('getPerformances' ,artiestId=artiestId, page=performances.next_num) if performances.has_next else None
    prev_url = url_for('getPerformances' ,artiestId=artiestId, page=performances.prev_num)  if performances.has_prev else None

    # End Pagination
    return render_template('artistPerformances.html',performances=performances.items,
                                                    artiest=artiest,
                                                    total=total,
                                                     next_url=next_url,
                                                     prev_url=prev_url)

# admin login 
@app.route('/dashboard_login',methods=['GET' , 'POST'])
def dashboard_login():
    if request.method == 'POST':
        email = request.form["email"] 
        password = request.form["password"]
        if not ( email == app.config["ADMIN_EMAIL"] and password == app.config["ADMIN_PASSWORD"] ) :
            flash ("Admin email or password incorrect")
            return redirect(url_for('dashboard_login'))
        else : 
            session["admin"] = True 
            return redirect('/admin')
    return render_template("dashboard_login.html")


@app.route('/admin_logout')
def admin_logout():
    if "admin" in session :
        session.pop("admin",None) 
    return redirect(url_for('dashboard_login'))

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found"

