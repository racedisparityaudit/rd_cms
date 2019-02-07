import pytest

from bs4 import BeautifulSoup
from flask import url_for
from itsdangerous import SignatureExpired, BadSignature

from application.utils import decode_review_token
from tests.models import MeasureVersionFactory, MeasureVersionWithDimensionFactory


def test_review_link_returns_page(test_app_client):

    measure_version = MeasureVersionFactory(status="DEPARTMENT_REVIEW")
    resp = test_app_client.get(url_for("review.review_page", review_token=measure_version.review_token))

    assert resp.status_code == 200
    page = BeautifulSoup(resp.data.decode("utf-8"), "html.parser")
    assert page.find("h1").text.strip() == measure_version.title


def test_review_page_does_not_include_status_bar(test_app_client):

    measure_version = MeasureVersionFactory(status="DEPARTMENT_REVIEW")
    resp = test_app_client.get(url_for("review.review_page", review_token=measure_version.review_token))

    page = BeautifulSoup(resp.data.decode("utf-8"), "html.parser")
    assert not page.find("div", class_="status")


def test_review_link_returns_404_if_token_incomplete(test_app_client):

    measure_version = MeasureVersionFactory(status="DEPARTMENT_REVIEW")
    broken_token = measure_version.review_token.replace(".", " ")
    resp = test_app_client.get(url_for("review.review_page", review_token=broken_token))

    assert resp.status_code == 404

    broken_token = "this will not work"

    resp = test_app_client.get(url_for("review.review_page", review_token=broken_token))

    assert resp.status_code == 404


def test_review_token_decoded_if_not_expired(app):

    measure_version = MeasureVersionFactory(status="DEPARTMENT_REVIEW", guid="test-measure-page")

    expires_tomorrow = 1
    decoded_guid, decoded_version = decode_review_token(
        measure_version.review_token,
        {"SECRET_KEY": app.config["SECRET_KEY"], "PREVIEW_TOKEN_MAX_AGE_DAYS": expires_tomorrow},
    )

    assert decoded_guid == measure_version.guid
    assert decoded_version == measure_version.version


def test_review_token_expired_throws_signature_expired(app):

    measure_version = MeasureVersionFactory(status="DEPARTMENT_REVIEW")
    expired_yesterday = -1

    with pytest.raises(SignatureExpired):
        decode_review_token(
            measure_version.review_token,
            {"SECRET_KEY": app.config["SECRET_KEY"], "PREVIEW_TOKEN_MAX_AGE_DAYS": expired_yesterday},
        )


def test_review_token_messed_up_throws_bad_signature(app):

    measure_version = MeasureVersionFactory(status="DEPARTMENT_REVIEW")

    broken_token = measure_version.review_token.replace(".", " ")

    expires_tomorrow = 1

    with pytest.raises(BadSignature):
        decode_review_token(
            broken_token, {"SECRET_KEY": app.config["SECRET_KEY"], "PREVIEW_TOKEN_MAX_AGE_DAYS": expires_tomorrow}
        )

    broken_token = "this will not work"

    with pytest.raises(BadSignature):
        decode_review_token(
            broken_token, {"SECRET_KEY": app.config["SECRET_KEY"], "PREVIEW_TOKEN_MAX_AGE_DAYS": expires_tomorrow}
        )


def test_page_main_download_available_without_login(
    test_app_client, mock_get_measure_download, mock_get_csv_data_for_download
):
    measure_version = MeasureVersionFactory(
        status="DEPARTMENT_REVIEW", uploads__title="test file", uploads__file_name="test-file.csv"
    )

    resp = test_app_client.get(
        url_for(
            "static_site.measure_version_file_download",
            topic_slug=measure_version.measure.subtopic.topic.slug,
            subtopic_slug=measure_version.measure.subtopic.slug,
            measure_slug=measure_version.measure.slug,
            version=measure_version.version,
            filename=measure_version.uploads[0].file_name,
        )
    )

    mock_get_measure_download.assert_called_with(measure_version.uploads[0], "test-file.csv", "source")
    mock_get_csv_data_for_download.assert_called_with("test-file.csv")

    assert resp.status_code == 200
    assert resp.content_type == "text/csv; charset=utf-8"
    assert resp.headers["Content-Disposition"] == "attachment; filename=test-file.csv"


def test_page_dimension_download_available_without_login(test_app_client):

    measure_version = MeasureVersionWithDimensionFactory(dimensions__title="stub dimension")

    resp = test_app_client.get(
        url_for(
            "static_site.dimension_file_download",
            topic_slug=measure_version.measure.subtopic.topic.slug,
            subtopic_slug=measure_version.measure.subtopic.slug,
            measure_slug=measure_version.measure.slug,
            version=measure_version.version,
            dimension_guid=measure_version.dimensions[0].guid,
        )
    )

    assert resp.status_code == 200
    assert resp.content_type == "text/csv"
    assert resp.headers["Content-Disposition"] == 'attachment; filename="stub-dimension.csv"'
