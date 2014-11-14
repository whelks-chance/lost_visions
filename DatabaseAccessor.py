import pprint
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, LostVisionsMachinematching, Image

__author__ = 'ubuntu'


# {'descriptor': '.lbp',
#   'descriptor_1': '/scratch/lost-visions/descriptors/maps/11307086946_59a8cab98b_o.jpg/desc.lbp',
#   'descriptor_2': '/scratch/lost-visions/descriptors/maps/11249985415_a18fd70e66_o.jpg/desc.lbp',
#   'img_a': './maps/11307086946_59a8cab98b_o.jpg',
#   'img_b': './maps/11249985415_a18fd70e66_o.jpg',
#   'match_settings': 'CV_COMP_CORREL',
#   'weight': 0.9844214439492431}


def save_to_db(weights):
    engine = create_engine('sqlite:////home/ubuntu/PycharmProjects/Lost-Visions/db.sqlite3')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    session = DBSession()

    for match in weights:
        machine_match = LostVisionsMachinematching()
        machine_match.metric = match['match_settings']
        machine_match.metric_value = match['weight']
        machine_match.metric_data = pprint.pformat(match)
        machine_match.execution_run = datetime.datetime.utcnow().isoformat()

        image_a_id = match['img_a'].split('/')[-1].split('_')[0]
        image_b_id = match['img_b'].split('/')[-1].split('_')[0]

        machine_match.image_a_flickr_id = image_a_id
        machine_match.image_b_flickr_id = image_b_id

        # image_a = session.query(Image).filter(Image.flickr_id==image_a_id).one()
        # image_b = session.query(Image).filter(Image.flickr_id==image_b_id).one()

        image_a = session.query(Image).filter(Image.id == 1).one()
        image_b = session.query(Image).filter(Image.id == 2).one()

        if image_a and image_b:

            machine_match.image_a = image_a
            machine_match.image_b = image_b

        session.add(machine_match)
        session.commit()