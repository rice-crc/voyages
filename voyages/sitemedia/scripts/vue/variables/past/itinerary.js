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

var_ship_name = new TextVariable({
    varName: "ship_name",
    label: gettext("Ship Name"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_embarkation_ports = new PlaceVariable({
    varName: "embarkation_ports",
    label: gettext("Embarkation Port"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: true,
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
    isImputed: true,
    isAdvanced: false
  });

var_geocode = new TextVariable({
    varName: "geocode",
    label: gettext("Geocode"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_year_range = new NumberVariable({
    varName: "year_range",
    label: gettext("Date that voyage arrived"),
    description: "",
  },{
    op: "is between",
    searchTerm0: 1514,
    searchTerm1: 1866
  },{
    isImputed: false,
    isAdvanced: false
  });

var_intended_disembarkation_port = new PlaceVariable({
    varName: "intended_disembarkation_port",
    label: gettext("Intended Disembarkation Port"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: true,
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

  shipPortsAndDate: {
    var_ship_name: var_ship_name,
    var_embarkation_ports: var_embarkation_ports,
    var_disembarkation_ports: var_disembarkation_ports,
    var_geocode: var_geocode,
    var_year_range: var_year_range,
    var_intended_disembarkation_port: var_intended_disembarkation_port,

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