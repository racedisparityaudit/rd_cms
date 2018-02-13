from flask import render_template, current_app, abort, flash, url_for
from flask_login import login_required
from itsdangerous import SignatureExpired, BadTimeSignature
from sqlalchemy.orm.exc import NoResultFound

from application.cms.models import Page
from application.review import review_blueprint
from application.utils import decode_review_token, generate_review_token, internal_user_required
from application import db


@review_blueprint.route('/<review_token>')
def review_page(review_token):
    try:
        id, version = decode_review_token(review_token, current_app.config)
        page = Page.query.filter_by(guid=id, version=version, review_token=review_token).one()

        if page.status not in ['DEPARTMENT_REVIEW', 'APPROVED']:
            return render_template('static_site/not_ready_for_review.html', asset_path='/static/', preview=True)

        dimensions = [dimension.to_dict() for dimension in page.dimensions]

        return render_template('static_site/measure.html',
                               measure_page=page,
                               dimensions=dimensions,
                               asset_path='/static/',
                               preview=True)

    except SignatureExpired as e:
        current_app.logger.exception(e)
        return render_template('review/token_expired.html')

    except (BadTimeSignature, NoResultFound) as e:
        current_app.logger.exception(e)
        abort(404)


@review_blueprint.route('/new-review-url/<id>/<version>')
@internal_user_required
@login_required
def get_new_review_url(id, version):
    try:
        token = generate_review_token(id, version)
        page = Page.query.filter_by(guid=id, version=version).one()
        page.review_token = token
        db.session.add(page)
        db.session.commit()
        url = url_for('review.review_page', review_token=page.review_token, _external=True)
        expires = page.review_token_expires_in(current_app.config)
        days = 'days' if expires > 1 else 'day'
        return "<p>Department review link: expires in {expires} {days}<br>{url}</p>".format(expires=expires,
                                                                                              days=days,
                                                                                              url=url)
    except Exception as e:
        current_app.logger.exception(e)
        abort(500)
