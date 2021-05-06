var_post_disembarkation_location = new PlaceVariable({
    varName: "post_disembarkation_location",
    label: gettext("Post Disembarkation Location"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

// all
fate = {
  fate: {
    var_post_disembarkation_location: var_post_disembarkation_location,

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
