import os
import pprint
import datetime
from random import randint
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from file_utils import downloadImage
from models import Base, LostVisionsMachinematching, Image, LostVisionsDescriptorlocation, LostVisionsImagelocation

__author__ = 'ubuntu'


class DatabaseAccessor():
    def __init__(self):
        engine = create_engine('sqlite:////home/ubuntu/PycharmProjects/Lost-Visions/db.sqlite3')

        # engine = create_engine('postgresql://local_user:l0c4l111@localhost:5432/local_db')


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
        self.session = DBSession()


def get_azure_url(metadata):
    return u"http://blmc.blob.core.windows.net/{0[date]}/{0[book_identifier]}_{0[volume]}_{0[page]}_{0[image_idx]}_{0[date]}_embellishments.jpg".format(metadata)


def find_files_from_db(max_files=10, session=None):
    if session is None:
        session = DatabaseAccessor().session

    number_of_Images = session.query(func.Count(Image.id)).one()[0]

    print number_of_Images

    complete= 0

    image_locations = []

    locations_dict = dict()


    while complete < max_files:
        rand_image_pk = randint(1, number_of_Images)

        try:
            found_image = session.query(Image).filter(Image.id == rand_image_pk).one()

            try:
                image_location = session.query(LostVisionsImagelocation) \
                    .filter(LostVisionsImagelocation.book_id==found_image.book_identifier,
                            LostVisionsImagelocation.volume==found_image.volume,
                            LostVisionsImagelocation.page==found_image.page,
                            LostVisionsImagelocation.idx==found_image.image_idx).one()

                if os.path.isfile(image_location.location):
                    image_locations.append(image_location.location)
                    locations_dict[found_image.flickr_id] = image_location.location
                else:
                    raise Exception

            #Either a db error with the ID or the db returned a file location with missing file
            except:

                url = get_azure_url({
                    'date': found_image.date,
                    'book_identifier': found_image.book_identifier,
                    'volume': found_image.volume,
                    'page': found_image.page,
                    'image_idx': found_image.image_idx
                })

                download_folder = '/scratch/lost-visions/images-found/embellishments/{}/'.format(found_image.date)

                try:
                    image_file_location = downloadImage(url, download_folder)

                    image_location = LostVisionsImagelocation()
                    image_location.book_id = found_image.book_identifier
                    image_location.volume = found_image.volume
                    image_location.page = found_image.page
                    image_location.idx = found_image.image_idx
                    image_location.location = image_file_location

                    session.add(image_location)

                    image_locations.append(image_file_location)
                    locations_dict[found_image.flickr_id] = image_file_location

                    complete += 1
                except Exception as e:
                    print e
        except:
            pass

    session.commit()

    # for f in image_locations[:max_files]:
    #     locations_dict[int(len(locations_dict))] = f

    return locations_dict


def save_descriptor_path_to_db(descriptor_data, session=None):

    if session is None:
        session = DatabaseAccessor().session

    found_image = session.query(Image).filter(Image.flickr_id == str(descriptor_data['img_id'])).one()

    descriptor_location_model = LostVisionsDescriptorlocation()
    descriptor_location_model.image = found_image
    descriptor_location_model.timestamp = datetime.datetime.utcnow()

    descriptor_location_model.book_id = found_image.book_identifier
    descriptor_location_model.volume = found_image.volume
    descriptor_location_model.page = found_image.page
    descriptor_location_model.idx = found_image.image_idx

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

def save_weights_to_db(weights, session= None):

    if session is None:
        session = DatabaseAccessor().session

    for match in weights:

        machine_match = LostVisionsMachinematching()
        machine_match.metric = match.get('match_settings', '')

        machine_match.metric_value = match['weight']
        machine_match.metric_data = pprint.pformat(match)
        machine_match.timestamp = datetime.datetime.utcnow()
        machine_match.execution_run = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()

        image_a_id = str(match['img_a_id'])
        image_b_id = str(match['img_b_id'])

        # Flip it so that image a has the lower flickr id
        # Not enforced, but handy convention.
        if int(image_a_id) < int(image_b_id):

            machine_match.image_a_flickr_id = image_a_id
            machine_match.image_b_flickr_id = image_b_id

            image_a = session.query(Image).filter(Image.flickr_id == image_a_id).one()
            image_b = session.query(Image).filter(Image.flickr_id == image_b_id).one()

            # image_a = session.query(Image).filter(Image.flickr_id==image_a_id).one()
            # image_b = session.query(Image).filter(Image.flickr_id==image_b_id).one()
        else:
            machine_match.image_a_flickr_id = image_b_id
            machine_match.image_b_flickr_id = image_a_id

            image_a = session.query(Image).filter(Image.flickr_id == image_b_id).one()
            image_b = session.query(Image).filter(Image.flickr_id == image_a_id).one()

            # image_a = session.query(Image).filter(Image.flickr_id==image_a_id).one()
            # image_b = session.query(Image).filter(Image.flickr_id==image_b_id).one()

        if image_a and image_b:
            machine_match.image_a = image_a
            machine_match.image_b = image_b

        session.add(machine_match)
    session.commit()
