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

// all
fate = {
  fate: {
    var_post_disembark_location: var_post_disembark_location,

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
