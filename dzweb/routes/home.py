from flask import Blueprint, render_template, redirect, url_for, request, Response
from dzweb.db import get_db


bp = Blueprint('home', __name__)


@bp.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap.xml."""
    pages = []
    # Home (Priority 1.0)
    pages.append({'loc': url_for('home.index', _external=True), 'priority': 1.0})

    # Main categories (Priority 0.8)
    for rule in ['home.introduction', 'home.history', 'home.organization',
                 'home.strategy', 'home.performance', 'home.style',
                 'product.fixture', 'product.automation', 'product.non_standard', 'product.robotics',
                 'case.main', 'service.service', 'contact.contact_us', 
                 'contact.message_board', 'contact.mailbox', 'human.hire', 'human.idea']:
        pages.append({'loc': url_for(rule, _external=True), 'priority': 0.8})

    # Dynamic products (Priority 0.7)
    db = get_db()
    products = db.execute('SELECT id FROM products').fetchall()
    for product in products:
        pages.append({'loc': url_for('product.display', id=product['id'], _external=True), 'priority': 0.7})

    # Dynamic cases (Priority 0.7)
    from dzweb.db import get_case_modules
    case_modules = get_case_modules()
    for module in case_modules:
        pages.append({'loc': url_for('case.display_case', slug=module['slug'], _external=True), 'priority': 0.7})

    # Add language versions for each page
    all_pages = []
    for page in pages:
        loc = page['loc']
        prio = page['priority']

        # Original (default/zh)
        all_pages.append({'loc': loc, 'priority': prio})

        # Multilingual versions
        if '?' in loc:
            all_pages.append({'loc': f"{loc}&lang=en", 'priority': prio})
            all_pages.append({'loc': f"{loc}&lang=ja", 'priority': prio})
        else:
            all_pages.append({'loc': f"{loc}?lang=en", 'priority': prio})
            all_pages.append({'loc': f"{loc}?lang=ja", 'priority': prio})

    sitemap_xml = render_template('home/sitemap.xml', pages=all_pages)
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