var_documented_name = new TextVariable({
    varName: "documented_name",
    label: gettext("Documented name"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

// all
africanName = {
  name: {
    var_documented_name: var_documented_name,

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