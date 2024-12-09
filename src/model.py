class Property:
    def __init__(
        self,
        index=None,
        depth=None,
        id_short=None,
        semantic_id=None,
        model_type=None,
        description=None,
        value=None,
        reference=None,
        parent=None,
    ):
        self._index = index
        self._depth = depth
        self._id_short = id_short
        self._semantic_id = semantic_id
        self._model_type = model_type
        self._description = description
        self._value = value
        self._reference = reference
        self._parent = parent

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, depth):
        self._depth = depth

    @property
    def id_short(self):
        return self._id_short

    @id_short.setter
    def id_short(self, id_short):
        self._id_short = id_short

    @property
    def semantic_id(self):
        return self._semantic_id

    @semantic_id.setter
    def semantic_id(self, semantic_id):
        self._semantic_id = semantic_id

    @property
    def model_type(self):
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        self._model_type = model_type

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, reference):
        self._reference = reference

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def is_allocated(self, input_value):
        return any([input_value]) if input_value is not None else False

    def to_json(self):
        return {
            "index": self._index,
            "depth": self._depth,
            "idShort": self._id_short,
            "semanticId": self._semantic_id,
            "modelType": self._model_type,
            "description": self._description,
            "value": self._value,
            "reference": self._reference,
            "parent": self._parent,
        }


class SubModelCollection:
    def __init__(self, id_short=None, model_type=None, children=[]):
        self._id_short = id_short
        self._model_type = model_type
        self._children = children

    @property
    def id_short(self):
        return self._id_short

    @id_short.setter
    def id_short(self, id_short):
        self._id_short = id_short

    @property
    def model_type(self):
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        self._model_type = model_type

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    def filled(self):
        return any([self._id_short, self._model_type, self._children])

    def to_json(self):
        return {
            "idShort": self._id_short,
            "modelType": self._model_type,
            "children": self._children,
        }
