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
    label: gettext("Gender"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

// all
personalData = {
  personalData: {
    var_age_range: var_age_range,
    var_gender: var_gender,

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
