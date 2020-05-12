#!/usr/bin/env python

from application import db
from application.cms.models import Organisation, TypeOfOrganisation
from application.config import Config
from application.factory import create_app
import sys

sys.path.insert(0, ".")  # noqa

if __name__ == "__main__":
    app = create_app(Config())
    with app.app_context():
        ofs_org = Organisation(
            id="PB1253",
            name="Office for Students",
            other_names=[],
            abbreviations=["OfS"],
            organisation_type=TypeOfOrganisation.EXECUTIVE_NON_DEPARTMENTAL_PUBLIC_BODY,
        )

        db.session.add(ofs_org)
        db.session.flush()

        db.session.commit()
