var_search_settings = new BooleanVariable({
    varName: "search_settings",
    label: "Show Advanced Variables in Search Filters",
    description: "Advanced variables are additional parameters that are not frequently used. Enabling them does not change current search behavior.",
  },{
    op: "equals",
    searchTerm: true,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_display_settings = new BooleanVariable({
  varName: "display_settings",
  label: "Display in Compact Mode",
  description: "Compact mode reduces white space and font size of the display. (This is a demo - if we do like the small font version, this will be enabled.)",
},{
  op: "equals",
  searchTerm: true,
},{
  isImputed: false,
  isAdvanced: false
});

settings = {
  settings: {
    var_search_settings: var_search_settings,
    var_display_settings: var_display_settings,
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
