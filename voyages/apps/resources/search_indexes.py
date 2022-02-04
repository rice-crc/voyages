from haystack import indexes
from .models import Image, AfricanName, Country


class ImagesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    imgtext = indexes.NgramField(use_template=True)
    file = indexes.CharField(model_attr="file")
    ready_to_go = indexes.BooleanField(model_attr="ready_to_go", default=False)
    date = indexes.IntegerField(model_attr="date", null=True)
    language = indexes.CharField(model_attr="language", null=True)
    title = indexes.CharField(model_attr="title")
    description = indexes.CharField(model_attr="description", null=True)
    source = indexes.CharField(model_attr="source", null=True)
    category_label = indexes.CharField()
    voyage_id = indexes.IntegerField(null=True)
    voyage_vessel_name = indexes.CharField(null=True)
    voyage_imp_voyage_began = indexes.CharField(null=True)
    voyage_year = indexes.CharField(null=True)

    def get_model(self):
        return Image

    def prepare_category_label(self, obj):
        return obj.category.label

    def prepare_voyage_id(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_id
        else:
            return None

    def prepare_voyage_vessel_name(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_ship.ship_name
        else:
            return None

    def prepare_voyage_imp_voyage_began(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_dates.imp_voyage_began
        else:
            return None

    def prepare_voyage_year(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_dates.imp_voyage_began
        else:
            return None

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class AfricanNamesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    slave_id = indexes.IntegerField(model_attr="slave_id")
    slave_name = indexes.NgramField(model_attr="name", null=True)
    slave_name_sort = indexes.CharField(model_attr="name", null=True)
    slave_age = indexes.IntegerField(model_attr="age", null=True)
    slave_height = indexes.FloatField(model_attr="height", null=True)
    slave_source = indexes.CharField(model_attr="source", null=True)
    slave_date_arrived = indexes.IntegerField(model_attr="date_arrived", null=True)
    slave_ship_name = indexes.NgramField(model_attr="ship_name", null=True)
    slave_ship_name_sort = indexes.CharField(model_attr="ship_name", null=True)
    slave_voyage_number = indexes.CharField(model_attr="voyage_number")
    slave_voyage = indexes.CharField(model_attr="voyage", null=True)
    slave_sex_age = indexes.CharField()
    slave_country = indexes.CharField(null=True)
    slave_country_sort = indexes.CharField(null=True)
    slave_embarkation_port = indexes.CharField(null=True)
    slave_embarkation_port_sort = indexes.CharField(null=True)
    slave_disembarkation_port = indexes.CharField(null=True)
    slave_disembarkation_port_sort = indexes.CharField(null=True)

    def get_model(self):
        return AfricanName

    def prepare_slave_voyage(self, obj):
        if obj.voyage is not None:
            return obj.voyage.voyage_id
        else:
            return None

    def prepare_slave_sex_age(self, obj):
        if obj.sex_age is not None:
            return obj.sex_age.name
        else:
            return None

    def prepare_slave_country(self, obj):
        if obj.country is not None:
            return obj.country.country_id
        else:
            return None

    def prepare_slave_country_sort(self, obj):
        if obj.country is not None:
            return obj.country.name
        else:
            return None

    def prepare_slave_embarkation_port(self, obj):
        if obj.embarkation_port is not None:
            return obj.embarkation_port.value
        else:
            return None

    def prepare_slave_embarkation_port_sort(self, obj):
        if obj.embarkation_port is not None:
            return obj.embarkation_port.place
        else:
            return None

    def prepare_slave_disembarkation_port(self, obj):
        if obj.disembarkation_port is not None:
            return obj.disembarkation_port.value
        else:
            return None

    def prepare_slave_disembarkation_port_sort(self, obj):
        if obj.disembarkation_port is not None:
            return obj.disembarkation_port.place
        else:
            return None

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class CountryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    country_id = indexes.IntegerField(model_attr="country_id")
    country_name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Country

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()