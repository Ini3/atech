from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def euskera():
    return render_template('index.html', 
        language='euskera',
        logo='img/logo-tree.png',
        headline1='APRENDE EUSKERA',
        headline2='APRENDE ESPAÑOL',
        content_title='MINTZAPRAKTIKA',
        lang_icon='🇪🇺', 
        lang_name='EUSKERA'
    )

@main.route('/espanol')
def espanol():
    return render_template('index.html', 
        language='espanol',
        logo='img/logo-tree-white.png',
        headline1='APRENDE ESPAÑOL',
        headline2='APRENDE ESPAÑOL',
        content_title='ESPAÑOL',
        lang_icon='🇪🇸',
        lang_name='ESPAÑOL'
    )
