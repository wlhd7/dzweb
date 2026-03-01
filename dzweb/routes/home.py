from flask import Blueprint, render_template, redirect, url_for, request, Response
from dzweb.db import get_db


bp = Blueprint('home', __name__)


@bp.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap.xml."""
    pages = []
    # Static pages from different blueprints
    # Home
    for rule in ['home.index', 'home.introduction', 'home.history', 'home.organization', 
                 'home.strategy', 'home.performance', 'home.style']:
        pages.append(url_for(rule, _external=True))
    
    # Product list pages
    for rule in ['product.fixture', 'product.automation', 'product.non_standard', 'product.robotics']:
        pages.append(url_for(rule, _external=True))
    
    # Case pages
    for rule in ['case.extruder', 'case.assembly_line', 'case.ass', 'case.robot_welding']:
        pages.append(url_for(rule, _external=True))
    
    # Service
    pages.append(url_for('service.service', _external=True))
    
    # Contact
    for rule in ['contact.contact_us', 'contact.message_board', 'contact.mailbox']:
        pages.append(url_for(rule, _external=True))
    
    # Human
    for rule in ['human.hire', 'human.idea']:
        pages.append(url_for(rule, _external=True))

    # Dynamic products
    db = get_db()
    products = db.execute('SELECT id FROM products').fetchall()
    for product in products:
        pages.append(url_for('product.display', id=product['id'], _external=True))

    # Add language versions for each page
    all_urls = []
    for page in pages:
        all_urls.append(page) # Default (zh usually)
        if '?' in page:
            all_urls.append(f"{page}&lang=en")
            all_urls.append(f"{page}&lang=ja")
        else:
            all_urls.append(f"{page}?lang=en")
            all_urls.append(f"{page}?lang=ja")

    sitemap_xml = render_template('home/sitemap.xml', urls=all_urls)
    return Response(sitemap_xml, mimetype='application/xml')


@bp.route('/')
def index():
    products = get_db().execute(
        'SELECT id, productname, filename FROM products'
        ' ORDER BY id DESC LIMIT 16',
    ).fetchall()

    return render_template('home/index.html', products=products)


@bp.route('/introduction')
def introduction():
    return render_template('home/introduction.html')


@bp.route('/history')
def history():
    return render_template('home/history.html')


@bp.route('/organization')
def organization():
    return render_template('home/organization.html')


@bp.route('/strategy')
def strategy():
    return render_template('home/strategy.html')


@bp.route('/performance')
def performance():
    return render_template('home/performance.html')


@bp.route('/style')
def style():
    return render_template('home/style.html')