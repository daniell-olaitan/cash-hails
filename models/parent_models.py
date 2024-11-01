import uuid
from models import db
from datetime import datetime
from typing import Dict, Any


class ParentModel:
    id = db.Column(
        db.String(60),
        primary_key=True,
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = str(uuid.uuid4())

    def to_dict(self) -> Dict:
        model_dict = {}
        model = vars(self)
        for key, value in model.items():
            if key == 'created_at':
                model_dict['created_at'] = self.created_at.isoformat()
            elif key == 'updated_at':
                model_dict['updated_at'] = self.updated_at.isoformat()
            elif key == '_sa_instance_state' or key == 'password':
                continue
            else:
                model_dict[key] = value

        return model_dict
