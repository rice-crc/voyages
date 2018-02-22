var_sources_plaintext_search = new TextVariable({
    varName: "sources_plaintext_search",
    label: "Source",
    description: "This is the source of the data. This could be a partial keyword.",
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
