var_source_1 = new TextVariable({
    varName: "source_1",
    label: gettext("Source 1"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_source_2 = new TextVariable({
    varName: "source_2",
    label: gettext("Source 2"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_source_3 = new TextVariable({
    varName: "source_3",
    label: gettext("Source 3"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

// all
sources = {
  sources: {
    var_source_1: var_source_1,
    var_source_2: var_source_2,
    var_source_3: var_source_3,

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
