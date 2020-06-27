var_age = new NumberVariable({
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
personalData = {
  personalData: {
    var_age: var_age,
    var_gender: var_gender,
    var_stature: var_stature,

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
