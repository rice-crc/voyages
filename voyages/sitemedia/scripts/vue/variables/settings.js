var_search_settings = new BooleanVariable({
    varName: "search_settings",
    label: "Show Advanced Variables in Search Filters",
    description: "Advanced variables are additional parameters that are not frequently used. Enabling them does not change current search behavior.",
  },{
    op: "equals",
    searchTerm: false,
  },{
    isImputed: false,
    isAdvanced: false
  });

settings = {
  settings: {
    var_search_settings: var_search_settings,
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
