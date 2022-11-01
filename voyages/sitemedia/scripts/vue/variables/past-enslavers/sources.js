var_source = new TextVariable({
    varName: "source",
    label: gettext("Biographical Source"),
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
    var_source: var_source,

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
