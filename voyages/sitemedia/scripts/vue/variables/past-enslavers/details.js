var_enslaved_count = new NumberVariable({
    varName: "enslaved_count",
    label: gettext("Number of Captives"),
    description: "",
  },{
    op: "is at least",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_roles = new TreeselectVariable({
    varName: "roles",
    label: gettext("Enslaver Roles"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

  
// all
enslaver_details = {
    enslaver_details: {
      var_enslaved_count: var_enslaved_count,
      var_roles: var_roles,
  
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
  