var_register_country = new TreeselectVariable({
    varName: "register_country",
    label: gettext("Register Country"),
    description: "",
  },{
    op: "is one of",
    searchTerm0: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_modern_country = new TreeselectVariable({
    varName: "modern_country",
    label: gettext("Modern Country"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_ethnicity = new TreeselectVariable({
    varName: "ethnicity",
    label: gettext("Ethnicity"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });


var_language_group = new TreeselectVariable({
    varName: "language_group",
    label: gettext("Language Group"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

// all
culturalAssociation = {
  country: {
    var_register_country: var_register_country,
    var_modern_country: var_modern_country,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  ethnicityAndLanguage: {
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
