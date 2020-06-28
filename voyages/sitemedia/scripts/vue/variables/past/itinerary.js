var_voyage_id = new NumberVariable({
    varName: "voyage_id",
    label: gettext("Voyage ID"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

// all
itinerary = {
  voyageId: {
    var_voyage_id: var_voyage_id,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  shipAndPorts: {
    

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