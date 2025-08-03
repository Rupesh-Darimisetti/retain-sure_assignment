# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need
from flask import Blueprint,request,jsonify,redirect
from app.model.shorturl import insert_url, get_url,increment_click_count
import string
import random
from urllib.parse import urlparse

bp = Blueprint('routes',__name__)

def generate_short_url(length = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

@bp.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@bp.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@bp.route('/api/shorten',methods=['POST'])
def url_shorten():
    data = request.get_json()
    original_url = data.get('original_url')
    
    if not original_url or not is_valid_url(original_url):
        return jsonify({'error':'Original URL is required'}),400
    
    short_code = generate_short_url()
    insert_url(short_code,original_url)
    return jsonify({
        'original_url':original_url,
        'short_code':short_code, 
        }),201

@bp.route('/<string:short_code>',methods=['GET'])
def redirect_code(short_code):
    long_url = get_url(short_code)
    print(long_url)
    if not long_url:
        return jsonify({'error':'Short URL not found'}),404
    increment_click_count(short_code)
    print(long_url)
    return redirect(long_url['original_url'])


@bp.route('/api/stats/<short_code>')
def analytics_endpoint(short_code):
    url_entry = get_url(short_code)
    if not url_entry:
        return jsonify({'error': 'Short URL not found'}), 404
    return jsonify({
        'original_url': url_entry['original_url'],
        'short_code': url_entry['short_code'],
        'click_count': url_entry['click_count']
    }), 200

