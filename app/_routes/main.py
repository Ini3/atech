from flask import Blueprint, render_template

app = Blueprint('main', __name__)

@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/euskera')
def euskera():
    return render_template('euskera.html',
        active_page='euskera',
        lang_icon='🇪🇺',
        lang_name='EUSKERA',
        current_lang_icon='🇪🇸'
    )

@app.route('/espanol')
def espanol():
    return render_template('esp.html',
    active_page='espanol',
    lang_icon='🇪s',
    lang_name='ESPANOL',
    current_lang_icon='🇪🇸'
    )

@app.route('/sobre-mi')
def sobre_mi():
    return render_template('sobre_mi.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/teacher')
def teacher_calendar():
    return render_template('calendar.html')


#@payments.route('/subscribe')
#def subscribe_page():
#    return render_template('payment.html', STRIPE_PUBLISHABLE_KEY=os.environ.get('STRIPE_PUBLISHABLE_KEY'))

#@app.route('/')
#def euskera():
#    return render_template('base.html', 
#        language='euskera',
#        logo='img/logo-tree.png',
#        headline1='APRENDE EUSKERA',
#        headline2='APRENDE ESPAÑOL',
#        content_title='MINTZAPRAKTIKA',
#        lang_icon='🇪🇺', 
#        lang_name='EUSKERA'
#    )

#@app.route('/espanol')
#def espanol():
#    return render_template('index.html', 
#        language='espanol',
#        logo='img/logo-tree-white.png',
#        headline1='APRENDE ESPAÑOL',
#        headline2='APRENDE ESPAÑOL',
#        content_title='ESPAÑOL',
#        lang_icon='🇪🇸',
#        lang_name='ESPAÑOL'
#    )
