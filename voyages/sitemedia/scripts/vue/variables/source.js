var_sources_plaintext = new TextVariable({
    varName: "sources_plaintext",
    label: "Source",
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

source = {
  source: {
    var_sources_plaintext: var_sources_plaintext,
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
