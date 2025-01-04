from .db_config import db, ma
from datetime import datetime

class QueryLog(db.Model):
    __tablename__ = "query_log"

    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(10))     # "admin" o "client"
    user_id = db.Column(db.Integer)          # id del admin/cliente
    query_text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(200))
    ip = db.Column(db.String(50))
    browser = db.Column(db.String(100))
    so = db.Column(db.String(100))           # Sistema Operativo
    timestamp = db.Column(db.DateTime, default=datetime.now)

class QueryLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QueryLog
        load_instance = True

query_log_schema = QueryLogSchema()
query_logs_schema = QueryLogSchema(many=True)
