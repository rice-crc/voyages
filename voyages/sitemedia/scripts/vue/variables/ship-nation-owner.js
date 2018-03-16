var_voyage_id = new NumberVariable({
    varName: "voyage_id",
    label: "Voyage ID",
    description: "This is the unique ID number assigned in the Trans-Atlantic Slave Trade database",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_ship_name_plaintext = new TextVariable({
    varName: "ship_name_plaintext",
    label: "Vessel Name",
    description: "This could be a partial keyword",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_owner_plaintext = new TextVariable({
    varName: "owner_plaintext",
    label: "Vessel Owner",
    description: "This could be a partial keyword",
  },{
    op: "contains",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_year_of_construction = new NumberVariable({
    varName: "year_of_construction",
    label: "Year Constructed",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_vessel_construction_place_idnum = new PlaceVariable({
    varName: "vessel_construction_place_idnum",
    label: "Place Constructed",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: true
  });

var_registered_year = new NumberVariable({
    varName: "registered_year",
    label: "Year Registered",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_registered_place_idnum = new PlaceVariable({
    varName: "registered_place_idnum",
    label: "Place Registered",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: true
  });

var_nationality = new TreeselectVariable({
    varName: "nationality",
    label: "Flag",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: true
  });

var_imputed_nationality = new TreeselectVariable({
    varName: "imputed_nationality",
    label: "Flag Imputed",
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
    label: "Rig of Vessel",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: true
  });

var_tonnage = new NumberVariable({
    varName: "tonnage",
    label: "Tonnage",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_tonnage_mod = new NumberVariable({
    varName: "tonnage_mod",
    label: "Standardized Tonnage",
    description: "This is the standardized tonnage calculated by algorithms",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

var_guns_mounted = new NumberVariable({
    varName: "guns_mounted",
    label: "Guns Mounted",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

// all
shipNationOwner = {
  voyagesAndVessels: {
    var_voyage_id: var_voyage_id,
    var_ship_name_plaintext: var_ship_name_plaintext,
    var_owner_plaintext: var_owner_plaintext,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  constructionAndRegistration: {
    var_year_of_construction: var_year_of_construction,
    var_vessel_construction_place_idnum: var_vessel_construction_place_idnum,
    var_registered_year: var_registered_year,
    var_registered_place_idnum: var_registered_place_idnum,

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
