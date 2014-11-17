import pprint
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, LostVisionsMachinematching, Image, LostVisionsDescriptorlocation

__author__ = 'ubuntu'




def save_descriptor_path_to_db(descriptor_data):
    engine = create_engine('sqlite:////home/ubuntu/PycharmProjects/Lost-Visions/db.sqlite3')
    # engine = create_engine('postgresql://local_user:l0c4l111@localhost:5432/local_db')

    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    found_image = session.query(Image).filter(Image.flickr_id == descriptor_data['img_id']).one()

    print found_image

    descriptor_location_model = LostVisionsDescriptorlocation()
    descriptor_location_model.image = found_image
    descriptor_location_model.location = descriptor_data['descriptor_path']
    descriptor_location_model.descriptor_type = descriptor_data['descriptor']
    descriptor_location_model.descriptor_settings = pprint.pformat(descriptor_data)

    session.add(descriptor_location_model)

    session.commit()


# {'descriptor': '.lbp',
#   'descriptor_1': '/scratch/lost-visions/descriptors/maps/11307086946_59a8cab98b_o.jpg/desc.lbp',
#   'descriptor_2': '/scratch/lost-visions/descriptors/maps/11249985415_a18fd70e66_o.jpg/desc.lbp',
#   'img_a': './maps/11307086946_59a8cab98b_o.jpg',
#   'img_b': './maps/11249985415_a18fd70e66_o.jpg',
#   'match_settings': 'CV_COMP_CORREL',
#   'weight': 0.9844214439492431}

def save_weights_to_db(weights):
    # engine = create_engine('sqlite:////home/ubuntu/PycharmProjects/Lost-Visions/db.sqlite3')

    engine = create_engine('postgresql://local_user:l0c4l111@localhost:5432/local_db')


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
        machine_match.metric = match.get('match_settings', '')

        machine_match.metric_value = match['weight']
        machine_match.metric_data = pprint.pformat(match)
        machine_match.execution_run = datetime.datetime.utcnow().isoformat()

        image_a_id = match['img_a'].split('/')[-1].split('_')[0]
        image_b_id = match['img_b'].split('/')[-1].split('_')[0]

        # Flip it so that image a has the lower flickr id
        # Not enforced, but handy convention.
        if int(image_a_id) < int(image_b_id):

            machine_match.image_a_flickr_id = image_a_id
            machine_match.image_b_flickr_id = image_b_id

            image_a = session.query(Image).filter(Image.id == 1).one()
            image_b = session.query(Image).filter(Image.id == 2).one()

            # image_a = session.query(Image).filter(Image.flickr_id==image_a_id).one()
            # image_b = session.query(Image).filter(Image.flickr_id==image_b_id).one()
        else:
            machine_match.image_a_flickr_id = image_b_id
            machine_match.image_b_flickr_id = image_a_id

            image_a = session.query(Image).filter(Image.id == 1).one()
            image_b = session.query(Image).filter(Image.id == 2).one()

            # image_a = session.query(Image).filter(Image.flickr_id==image_a_id).one()
            # image_b = session.query(Image).filter(Image.flickr_id==image_b_id).one()

        if image_a and image_b:

            machine_match.image_a = image_a
            machine_match.image_b = image_b

        session.add(machine_match)
    session.commit()