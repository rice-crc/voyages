var_sources_plaintext_search = new TextVariable({
    varName: "sources_plaintext_search",
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
    var_sources_plaintext_search: var_sources_plaintext_search,
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
