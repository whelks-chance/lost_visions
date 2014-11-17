# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AccountEmailaddres(Base):
    __tablename__ = 'account_emailaddress'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'auth_user.id'), nullable=False, index=True)
    email = Column(String(75), nullable=False)
    verified = Column(Boolean, nullable=False)
    primary = Column(Boolean, nullable=False)

    user = relationship(u'AuthUser')


class AccountEmailconfirmation(Base):
    __tablename__ = 'account_emailconfirmation'

    id = Column(Integer, primary_key=True)
    email_address_id = Column(ForeignKey(u'account_emailaddress.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False)
    sent = Column(DateTime)
    key = Column(String(64), nullable=False)

    email_address = relationship(u'AccountEmailaddres')


class AdminToolsDashboardPreference(Base):
    __tablename__ = 'admin_tools_dashboard_preferences'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'auth_user.id'), nullable=False, index=True)
    data = Column(Text, nullable=False)
    dashboard_id = Column(String(100), nullable=False)

    user = relationship(u'AuthUser')


class AdminToolsMenuBookmark(Base):
    __tablename__ = 'admin_tools_menu_bookmark'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'auth_user.id'), nullable=False, index=True)
    url = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)

    user = relationship(u'AuthUser')


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, index=True)
    permission_id = Column(ForeignKey(u'auth_permission.id'), nullable=False, index=True)

    permission = relationship(u'AuthPermission')


class AuthPermission(Base):
    __tablename__ = 'auth_permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    content_type_id = Column(Integer, nullable=False, index=True)
    codename = Column(String(100), nullable=False)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(75), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime, nullable=False)


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    group_id = Column(ForeignKey(u'auth_group.id'), nullable=False, index=True)

    group = relationship(u'AuthGroup')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    permission_id = Column(ForeignKey(u'auth_permission.id'), nullable=False, index=True)

    permission = relationship(u'AuthPermission')


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    volume = Column(String(120), nullable=False)
    publisher = Column(String(256), nullable=False)
    title = Column(String(256), nullable=False)
    first_author = Column(String(120), nullable=False)
    BL_DLS_ID = Column(String(120), nullable=False)
    pubplace = Column(String(120), nullable=False)
    book_identifier = Column(String(120), nullable=False)
    ARK_id_of_book = Column(String(120), nullable=False)
    date = Column(String(120), nullable=False)


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'

    id = Column(Integer, primary_key=True)
    action_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    content_type_id = Column(Integer, index=True)
    object_id = Column(Text)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(Integer, nullable=False)
    change_message = Column(Text, nullable=False)


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(Text, nullable=False)
    expire_date = Column(DateTime, nullable=False, index=True)


class DjangoSite(Base):
    __tablename__ = 'django_site'

    id = Column(Integer, primary_key=True)
    domain = Column(String(100), nullable=False)
    name = Column(String(50), nullable=False)


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    volume = Column(String(256), nullable=False)
    publisher = Column(String(256), nullable=False)
    title = Column(String(256), nullable=False)
    first_author = Column(String(256), nullable=False)
    BL_DLS_ID = Column(String(256), nullable=False)
    pubplace = Column(String(256), nullable=False)
    book_identifier = Column(String(256), nullable=False)
    ARK_id_of_book = Column(String(256), nullable=False)
    date = Column(String(256), nullable=False)
    flickr_url = Column(String(256), nullable=False)
    image_idx = Column(String(256), nullable=False)
    page = Column(String(256), nullable=False)
    flickr_id = Column(String(256), nullable=False)
    flickr_small_source = Column(String(256), nullable=False)
    flickr_small_height = Column(String(256), nullable=False)
    flickr_small_width = Column(String(256), nullable=False)
    flickr_medium_source = Column(String(256), nullable=False)
    flickr_medium_height = Column(String(256), nullable=False)
    flickr_medium_width = Column(String(256), nullable=False)
    flickr_large_source = Column(String(256), nullable=False)
    flickr_large_height = Column(String(256), nullable=False)
    flickr_large_width = Column(String(256), nullable=False)
    flickr_original_source = Column(String(256), nullable=False)
    flickr_original_height = Column(String(256), nullable=False)
    flickr_original_width = Column(String(256), nullable=False)
    views_begun = Column(Integer, server_default=text("0"))
    views_completed = Column(Integer, server_default=text("0"))


class LostVisionsBookillustrator(Base):
    __tablename__ = 'lost_visions_bookillustrator'

    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey(u'book.id'), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    technique = Column(String(120), nullable=False)

    book = relationship(u'Book')


class LostVisionsCategory(Base):
    __tablename__ = 'lost_visions_category'

    id = Column(Integer, primary_key=True)
    term = Column(String(256), nullable=False)


class LostVisionsDescriptorlocation(Base):
    __tablename__ = 'lost_visions_descriptorlocation'

    id = Column(Integer, primary_key=True)
    location = Column(Text, nullable=False)
    image_id = Column(ForeignKey(u'image.id'), index=True)
    book_id = Column(Text, nullable=False)
    volume = Column(Text, nullable=False)
    page = Column(Text, nullable=False)
    idx = Column(Text, nullable=False)
    descriptor_type = Column(Text, nullable=False)
    descriptor_settings = Column(Text, nullable=False)
    timestamp = Column(DateTime)

    image = relationship(u'Image')


class LostVisionsExpertlevel(Base):
    __tablename__ = 'lost_visions_expertlevel'

    id = Column(Integer, primary_key=True)
    description = Column(String(256), nullable=False)


class LostVisionsGeotag(Base):
    __tablename__ = 'lost_visions_geotag'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'lost_visions_lostvisionuser.id'), nullable=False, index=True)
    image_id = Column(ForeignKey(u'image.id'), nullable=False, index=True)
    north_east_x = Column(String(256), nullable=False)
    north_east_y = Column(String(256), nullable=False)
    south_west_x = Column(String(256), nullable=False)
    south_west_y = Column(String(256), nullable=False)
    timestamp = Column(DateTime)
    tag_order = Column(Integer)

    image = relationship(u'Image')
    user = relationship(u'LostVisionsLostvisionuser')


class LostVisionsImagecategory(Base):
    __tablename__ = 'lost_visions_imagecategories'

    id = Column(Integer, primary_key=True)


class LostVisionsImagecollection(Base):
    __tablename__ = 'lost_visions_imagecollection'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    user_id = Column(ForeignKey(u'lost_visions_lostvisionuser.id'), nullable=False, index=True)
    public = Column(Boolean, nullable=False)
    timestamp = Column(DateTime)

    user = relationship(u'LostVisionsLostvisionuser')


class LostVisionsImagelocation(Base):
    __tablename__ = 'lost_visions_imagelocation'

    id = Column(Integer, primary_key=True)
    location = Column(Text, nullable=False)
    book_id = Column(Text, nullable=False)
    volume = Column(Text, nullable=False)
    page = Column(Text, nullable=False)
    idx = Column(Text, nullable=False)


class LostVisionsImagemapping(Base):
    __tablename__ = 'lost_visions_imagemapping'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey(u'image.id'), nullable=False, index=True)
    collection_id = Column(ForeignKey(u'lost_visions_imagecollection.id'), nullable=False, index=True)
    timestamp = Column(DateTime)

    collection = relationship(u'LostVisionsImagecollection')
    image = relationship(u'Image')


class LostVisionsImagetext(Base):
    __tablename__ = 'lost_visions_imagetext'

    id = Column(Integer, primary_key=True)
    caption = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime)
    user_id = Column(ForeignKey(u'lost_visions_lostvisionuser.id'), nullable=False, index=True)
    image_id = Column(ForeignKey(u'image.id'), nullable=False, index=True)

    image = relationship(u'Image')
    user = relationship(u'LostVisionsLostvisionuser')


class LostVisionsLinkedimage(Base):
    __tablename__ = 'lost_visions_linkedimage'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey(u'image.id'), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    file_name = Column(String(120), nullable=False)
    location = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    image = relationship(u'Image')


class LostVisionsLostvisionuser(Base):
    __tablename__ = 'lost_visions_lostvisionuser'

    id = Column(Integer, primary_key=True)
    username_id = Column(ForeignKey(u'auth_user.id'), nullable=False, index=True)
    expert_level = Column(Integer, nullable=False)
    self_description = Column(String(256), nullable=False)
    sign_up_timestamp = Column(DateTime)
    last_login = Column(DateTime)
    number_logins = Column(Integer, nullable=False)

    username = relationship(u'AuthUser')


class LostVisionsMachinematching(Base):
    __tablename__ = 'lost_visions_machinematching'

    id = Column(Integer, primary_key=True)
    image_a_id = Column(ForeignKey(u'image.id'), nullable=False, index=True)
    image_a_flickr_id = Column(Text, nullable=False)
    image_b_id = Column(ForeignKey(u'image.id'), nullable=False, index=True)
    image_b_flickr_id = Column(Text, nullable=False)
    metric_value = Column(Float, nullable=False)
    metric = Column(Text, nullable=False)
    metric_data = Column(Text, nullable=False)
    execution_run = Column(Integer, nullable=False)
    timestamp = Column(DateTime)

    image_a = relationship(u'Image', primaryjoin='LostVisionsMachinematching.image_a_id == Image.id')
    image_b = relationship(u'Image', primaryjoin='LostVisionsMachinematching.image_b_id == Image.id')


class LostVisionsSavedimagecaption(Base):
    __tablename__ = 'lost_visions_savedimagecaption'

    id = Column(Integer, primary_key=True)
    image_mapping_id = Column(ForeignKey(u'lost_visions_imagemapping.id'), nullable=False, index=True)
    caption = Column(Text, nullable=False)
    timestamp = Column(DateTime)

    image_mapping = relationship(u'LostVisionsImagemapping')


class LostVisionsSavedimage(Base):
    __tablename__ = 'lost_visions_savedimages'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'lost_visions_lostvisionuser.id'), nullable=False, index=True)
    image_id = Column(ForeignKey(u'image.id'), nullable=False, index=True)
    timestamp = Column(DateTime)

    image = relationship(u'Image')
    user = relationship(u'LostVisionsLostvisionuser')


class LostVisionsSearchquery(Base):
    __tablename__ = 'lost_visions_searchquery'

    id = Column(Integer, primary_key=True)
    search_term = Column(String(256), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    user_id = Column(ForeignKey(u'lost_visions_lostvisionuser.id'), nullable=False, index=True)

    user = relationship(u'LostVisionsLostvisionuser')


class LostVisionsTag(Base):
    __tablename__ = 'lost_visions_tag'

    id = Column(Integer, primary_key=True)
    tag = Column(String(256), nullable=False)
    user_id = Column(ForeignKey(u'lost_visions_lostvisionuser.id'), nullable=False, index=True)
    image_id = Column(ForeignKey(u'image.id'), nullable=False, index=True)
    x_percent = Column(String(256), nullable=False)
    y_percent = Column(String(256), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    tag_order = Column(Integer, nullable=False)

    image = relationship(u'Image')
    user = relationship(u'LostVisionsLostvisionuser')


class LostVisionsUserinterest(Base):
    __tablename__ = 'lost_visions_userinterests'

    id = Column(Integer, primary_key=True)


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)


class SocialaccountSocialaccount(Base):
    __tablename__ = 'socialaccount_socialaccount'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'auth_user.id'), nullable=False, index=True)
    provider = Column(String(30), nullable=False)
    uid = Column(String(255), nullable=False)
    last_login = Column(DateTime, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    extra_data = Column(Text, nullable=False)

    user = relationship(u'AuthUser')


class SocialaccountSocialapp(Base):
    __tablename__ = 'socialaccount_socialapp'

    id = Column(Integer, primary_key=True)
    provider = Column(String(30), nullable=False)
    name = Column(String(40), nullable=False)
    client_id = Column(String(100), nullable=False)
    secret = Column(String(100), nullable=False)
    key = Column(String(100), nullable=False)


class SocialaccountSocialappSite(Base):
    __tablename__ = 'socialaccount_socialapp_sites'

    id = Column(Integer, primary_key=True)
    socialapp_id = Column(Integer, nullable=False, index=True)
    site_id = Column(ForeignKey(u'django_site.id'), nullable=False, index=True)

    site = relationship(u'DjangoSite')


class SocialaccountSocialtoken(Base):
    __tablename__ = 'socialaccount_socialtoken'

    id = Column(Integer, primary_key=True)
    app_id = Column(ForeignKey(u'socialaccount_socialapp.id'), nullable=False, index=True)
    account_id = Column(ForeignKey(u'socialaccount_socialaccount.id'), nullable=False, index=True)
    token = Column(Text, nullable=False)
    token_secret = Column(Text, nullable=False)
    expires_at = Column(DateTime)

    account = relationship(u'SocialaccountSocialaccount')
    app = relationship(u'SocialaccountSocialapp')
