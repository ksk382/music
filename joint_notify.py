from joint_build_database import monther, gig, band
from email.mime.text import MIMEText
import datetime as dt
import smtplib
from joint_music_utilities import cleandb, cleanish
from joint_quotes import get_a_quote
import json

tdelta = 60

def notify(Session, ttotm, live_mode):
    session = Session()
    cleandb(Session)
    targets = session.query(monther)
    quote = get_a_quote()
    if live_mode == True:
        for target in targets:
            print(target.email)
            message = prepmsg(Session, target, quote)
            send_email(Session, target, message, ttotm, True)
    else:
        for target in targets:
            message = prepmsg(Session, target, quote)
            send_email(Session, target, message, ttotm, False)

def prepmsg(Session, target, quote):
    session = Session()
    listofbands = session.query(band)
    message = quote + '\n\n'
    message = message + "Shows happening in the next {2} days within {0} miles of {1}:".format(target.radius, target.city, tdelta)
    message = message + "\n" + "(Checked {0} bands)".format(listofbands.count()) + '\n'
    allshows = session.query(gig).order_by(gig.date.asc()).filter(gig.queryby == target.sig)
    message_lines = []
    try:
        for show in allshows:
            theband = session.query(band).filter(band.cleanname == show.cleanname).first()
            cleandate = show.date[5:7].lstrip('0') + '/' + show.date[8::]
            combo_show = False
            source = theband.appeared
            for i in message_lines:
                if i[0] == cleandate and cleanish(i[2]) == cleanish(show.venue):
                    combo_show = True
                    i[1] = i[1] + ' and ' + show.name
                    if i[4] != source:
                        i[4] = i[4] + ', ' + source
            if combo_show == False:
                line = [cleandate, show.name, show.venue, show.city, source, theband.comment]
                message_lines.append(line)
        for i in message_lines:
            print(i)
            line = '{0} {1} @ {2}, {3}'.format(i[0], i[1], i[2], i[3])
            message = message + '\n' + line + '\n' + '   ({0})'.format(i[4]) + '\n'
            if i[5] != None:
                comment = 'Comment: ' + i[5]
                message = message + '   ({0})'.format(comment) + '\n'

    except Exception as e:
        print((str(e)))
        print((show.cleanname))

    print('\n\n\n\n')
    print(message)
    return message


def send_email(Session, target, message, ttotm, live_mode):
    hidden_vals = '../showtime_creds/ajsonhidden_vals.json'
    try:
        jfile = open(hidden_vals)
    except:
        print('Need a file named ajsonhidden_vals.json in the ../showtime_creds/ directory with login information.')
        sys.exit()
    jstr = jfile.read()
    jdata = json.loads(jstr)
    email = jdata['dev email']['email']

    if live_mode:
        email = target.email

    sender = jdata['Group email']['email']
    pw = jdata['Group email']['password']
    msg = MIMEText(message)#.encode('utf-8'))

    a = dt.date.today()

    filler = ttotm
    msg['Subject'] = '{2} Shows for {0} ({1})'.format(target.city, a.strftime("%m/%d").lstrip('0'), filler)
    msg['From'] = sender
    msg['To'] = email

    s = smtplib.SMTP('smtp.gmail.com', 587)  # port 465 or 587
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(sender, pw)
    s.sendmail(sender, email, msg.as_string())
    s.close()