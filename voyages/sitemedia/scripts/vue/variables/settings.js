var_search_settings = new BooleanVariable({
    varName: "search_settings",
    label: gettext("Show advanced variables in search filters"),
    description: gettext("Advanced variables are additional parameters not frequently used. Enabling them does not change current search behavior."),
  },{
    op: "equals",
    searchTerm: true,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_display_settings = new BooleanVariable({
  varName: "display_settings",
  label: gettext("Display in compact mode"),
  description: gettext("Compact mode reduces white space and font size of the display."),
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
