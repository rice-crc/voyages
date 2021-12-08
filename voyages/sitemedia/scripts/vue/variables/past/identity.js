var_searched_name = new TextVariable({
    varName: "searched_name",
    label: gettext("Name"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_exact_name_search = new BooleanVariable({
    varName: "exact_name_search",
    label: gettext("Exact Search"),
    description: "",
  },{
    op: "equals",
    searchTerm: false,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_age_range = new NumberVariable({
    varName: "age_range",
    label: gettext("Age"),
    description: "",
  },{
    op: "is between",
    searchTerm0: 0,
    searchTerm1: 80
  },{
    isImputed: false,
    isAdvanced: false
  });

var_gender = new TreeselectVariable({
    varName: "gender",
    label: gettext("Sex"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_enslaved_id = new NumberVariable({
    varName: "enslaved_id",
    label: gettext("Unique ID"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_height_range = new NumberVariable({
    varName: "height_range",
    label: gettext("Height (in.)"),
    description: "",
  },{
    op: "is between",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_skin_color = new TextVariable({
    varName: "skin_color",
    label: gettext("Racial Descriptor"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

// all
identity = {
  name: {
    var_searched_name: var_searched_name,
    var_exact_name_search: var_exact_name_search,
    var_age_range: var_age_range,
    var_enslaved_id: var_enslaved_id,
    var_height_range: var_height_range,
    var_gender: var_gender,
    var_skin_color: var_skin_color,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  count: {
    changed: 0,
    activated: 0,
  },
}
