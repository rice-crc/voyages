var_sources_plaintext = new TextVariable({
    varName: "sources_plaintext",
    label: pgettext("filter select label", "SOURCE"),
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
