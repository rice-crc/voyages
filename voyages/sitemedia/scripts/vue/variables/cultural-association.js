var_register_country = new PlaceVariable({
    varName: "age",
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

var_modern_country = new PlaceVariable({
    varName: "age",
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
    label: gettext("Gender"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_stature = new NumberVariable({
    varName: "stature",
    label: gettext("Stature"),
    description: "",
  },{
    op: "is between",
    searchTerm0: 60,
    searchTerm1: 80
  },{
    isImputed: false,
    isAdvanced: false
  });

// all
culturalAssociation = {
  name: {
    var_register_country: var_register_country,
    var_modern_country: var_modern_country,
    var_ethnicity: var_ethnicity,
    var_language_group: var_language_group,

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
