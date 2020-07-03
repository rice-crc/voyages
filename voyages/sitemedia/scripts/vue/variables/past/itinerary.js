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

var_embarkation_port = new PlaceVariable({
    varName: "embarkation_port",
    label: gettext("Embarkation Port"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_disembarkation_port = new PlaceVariable({
    varName: "disembarkation_port",
    label: gettext("Disembarkation Port"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
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

var_voyage_arrived = new DateVariable({
    varName: "voyage_arrived",
    label: gettext("Date that voyage arrived"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isadvanced: false
  },
  true);

var_intended_disembarkation_port = new PlaceVariable({
    varName: "intended_disembarkation_port",
    label: gettext("Intended Disembarkation Port"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
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

  shipPortsAndDate: {
    var_ship_name: var_ship_name,
    var_embarkation_port: var_embarkation_port,
    var_disembarkation_port: var_disembarkation_port,
    var_geocode: var_geocode,
    var_voyage_arrived: var_voyage_arrived,
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