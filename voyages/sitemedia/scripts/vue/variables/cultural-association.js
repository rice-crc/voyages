var_register_country = new PlaceVariable({
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

var_modern_country = new PlaceVariable({
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

// all
culturalAssociation = {
  name: {
    var_register_country: var_register_country,
    var_modern_country: var_modern_country,
    // var_ethnicity: var_ethnicity,
    // var_language_group: var_language_group,

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
