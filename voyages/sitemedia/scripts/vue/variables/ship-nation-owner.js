var_voyage_id = new NumberVariable({
    varName: "voyage_id",
    label: gettext("Voyage ID"),
    description: gettext("This is the unique ID number assigned to a voyage"),
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
    label: gettext("Vessel name"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_owner = new TextVariable({
    varName: "owner",
    label: gettext("Vessel owner"),
    description: "",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_year_of_construction = new NumberVariable({
    varName: "year_of_construction",
    label: gettext("Year constructed"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isadvanced: false
  });

var_vessel_construction_place_idnum = new PlaceVariable({
    varName: "vessel_construction_place_idnum",
    label: gettext("Place constructed"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_registered_year = new NumberVariable({
    varName: "registered_year",
    label: gettext("Year registered"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isadvanced: false
  });

var_registered_place_idnum = new PlaceVariable({
    varName: "registered_place_idnum",
    label: gettext("Place registered"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_nationality = new TreeselectVariable({
    varName: "nationality",
    label: gettext("Flag"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_imputed_nationality = new TreeselectVariable({
    varName: "imputed_nationality",
    label: gettext("Flag (imputed)"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: true,
    isAdvanced: false
  });

var_rig_of_vessel = new TreeselectVariable({
    varName: "rig_of_vessel",
    label: gettext("Rig of vessel"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_tonnage = new NumberVariable({
    varName: "tonnage",
    label: gettext("Tonnage"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isadvanced: false
  });

var_tonnage_mod = new NumberVariable({
    varName: "tonnage_mod",
    label: gettext("Standardized tonnage"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isadvanced: false
  });

var_guns_mounted = new NumberVariable({
    varName: "guns_mounted",
    label: gettext("Guns mounted"),
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isadvanced: false
  });

// all
shipNationOwner = {
  voyagesAndVessels: {
    var_voyage_id: var_voyage_id,
    var_ship_name: var_ship_name,
    var_owner: var_owner,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  flag: {
    var_nationality: var_nationality,
    var_imputed_nationality: var_imputed_nationality,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  constructionAndRegistration: {
    var_vessel_construction_place_idnum: var_vessel_construction_place_idnum,
    var_year_of_construction: var_year_of_construction,
    var_registered_place_idnum: var_registered_place_idnum,
    var_registered_year: var_registered_year,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  rigTonnageAndGunsMounted: {
    var_rig_of_vessel: var_rig_of_vessel,
    var_tonnage: var_tonnage,
    var_tonnage_mod: var_tonnage_mod,
    var_guns_mounted: var_guns_mounted,

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
