from app import db
from sqlalchemy.orm import relationship

from orm.entities.Election import ElectionParty, ElectionCandidate, InvalidVoteCategory
from util import get_paginated_query


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionName = db.Column(db.String(100), nullable=False)
    parties = relationship("ElectionPartyModel")
    invalidVoteCategories = relationship("InvalidVoteCategoryModel")

    def __init__(self, electionName):
        super(ElectionModel, self).__init__(electionName=electionName)

        db.session.add(self)
        db.session.flush()

    def add_invalid_vote_category(self, categoryDescription):
        return InvalidVoteCategory.create(
            electionId=self.electionId,
            categoryDescription=categoryDescription
        )

    def add_party(self, partyId):
        return ElectionParty.create(
            electionId=self.electionId,
            partyId=partyId
        )

    def add_candidate(self, partyId, candidateId):
        return ElectionCandidate.create(
            electionId=self.electionId,
            partyId=partyId,
            candidateId=candidateId
        )


Model = ElectionModel


def create(electionName):
    result = Model(electionName=electionName)

    return result


def get_all():
    query = Model.query

    result = get_paginated_query(query).all()

    return result


def get_by_id(electionId):
    result = Model.query.filter(
        Model.electionId == electionId
    ).one_or_none()

    return result


def create_tally_sheets(electionId, electionType):
    election = get_by_id(electionId=electionId)

    # if electionType == "Precidential":
