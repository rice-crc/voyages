var_post_disembark_location = new PlaceVariable({
    varName: "post_disembark_location",
    label: gettext("Post Disembarkation Location"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_vessel_fate = new TreeselectVariable({
    varName: "vessel_fate",
    label: gettext("Vessel Fate"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

// all
fate = {
  fate: {
    var_post_disembark_location: var_post_disembark_location,
    var_vessel_fate: var_vessel_fate,

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
