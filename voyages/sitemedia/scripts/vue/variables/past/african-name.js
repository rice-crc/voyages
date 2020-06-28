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

// all
africanName = {
  name: {
    var_searched_name: var_searched_name,
    var_exact_name_search: var_exact_name_search,

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
