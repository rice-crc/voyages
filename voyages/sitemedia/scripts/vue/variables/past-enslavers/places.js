var_embarkation_ports = new PlaceVariable({
    varName: "embarkation_ports",
    label: gettext("Embarkation Port"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_disembarkation_ports = new PlaceVariable({
    varName: "disembarkation_ports",
    label: gettext("Disembarkation Port"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_departure_ports = new PlaceVariable({
    varName: "departure_ports",
    label: gettext("Departure Port"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });


// all
places = {
  places: {
    var_embarkation_ports: var_embarkation_ports,
    var_disembarkation_ports: var_disembarkation_ports,
    var_departure_ports: var_departure_ports,

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
