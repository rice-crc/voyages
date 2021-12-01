var_enslaved_id = new NumberVariable({
    varName: "enslaved_id",
    label: gettext("African ID"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

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
    var_enslaved_id: var_enslaved_id,

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
