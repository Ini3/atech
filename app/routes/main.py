from flask import Blueprint, render_template

main = Blueprint('main', __name__)

<<<<<<< HEAD:app.py
@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/euskera')
=======
@main.route('/')
>>>>>>> fee1b2003d72065a2e162aa29aef015516352cb8:app/routes/main.py
def euskera():
    return render_template('euskera.html',
        active_page='euskera',
        lang_icon='🇪🇺',
        lang_name='EUSKERA',
        current_lang_icon='🇪🇸'
    )

@main.route('/espanol')
def espanol():
    return render_template('esp.html',
    active_page='espanol',
    lang_icon='🇪s',
    lang_name='ESPANOL',
    current_lang_icon='🇪🇸'
    )
<<<<<<< HEAD:app.py

@app.route('/sobre-mi')
def sobre_mi():
    return render_template('sobre_mi.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')



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

if __name__ == '__main__':
    app.run(debug=True)
=======
>>>>>>> fee1b2003d72065a2e162aa29aef015516352cb8:app/routes/main.py
