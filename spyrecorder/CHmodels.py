from infi.clickhouse_orm import models as md
from infi.clickhouse_orm import fields as fd
from infi.clickhouse_orm import engines as en
import datetime
class Actions(md.Model):
    # describes datatypes and fields
    user_id = fd.UInt64Field()
    user_name=fd.StringField()
    time=fd.StringField()
    event_type=fd.StringField()
    screen_name=fd.StringField()
    app_name=fd.StringField()
    app_productname=fd.StringField()
    app_version=fd.StringField()
    app_publisher=fd.StringField()
    app_file=fd.StringField()
    app_copyright=fd.StringField()
    app_language=fd.StringField()
    file_versioninfo=fd.StringField()
    file_description=fd.StringField()
    file_internalname=fd.StringField()
    file_originalname=fd.StringField()
    Date = fd.DateField(default=datetime.date.today())
    engine = en.MergeTree('Date', ('user_id','user_name','time','event_type','screen_name','app_name',
                                   'app_productname','app_version','app_publisher','app_file',
                                   'app_copyright','app_language','file_versioninfo','file_description',
                                   'file_internalname','file_originalname'))
