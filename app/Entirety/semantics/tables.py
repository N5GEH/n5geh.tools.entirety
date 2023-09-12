from django_tables2 import tables, CheckBoxColumn, TemplateColumn

class CheckBoxColumnWithName(tables.columns.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name
    
class PrefixTable(tables.Table):
    name = tables.columns.Column()  
    value = tables.columns.Column()
    include = tables.columns.Column()   
    # include = CheckBoxColumnWithName(
    #     # verbose_name="Include",
    #     accessor="pk",
    #     # attrs={
    #     #     "td__input": {
    #     #         "value": lambda record: record.name,
    #     #         "type": "checkbox",
    #     #     },
    #     # },
    #     orderable=False,
    # )
    # include = TemplateColumn('<input type="checkbox" value="{{ attributes.include }}" />', verbose_name="Include")

    # include = CheckBoxColumn(accessor='pk')

    def get_prefix_set(self):
        return [{"name": "mvf", "value":"1244"}]