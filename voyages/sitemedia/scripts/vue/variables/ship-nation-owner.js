var_voyage_id = new NumberVariable({
    varName: "voyage_id",
    label: "Voyage Identification Number",
    description: "Each voyage in the database has a unique identification number. This could be a range.",
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
    description: "The name of the vessels. This could be a partial keyword.",
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
    description: "The name of the vessel owners. This could be a partial keyword.",
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
    description: "Enter the year when the ships were constructed. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_registered_year = new NumberVariable({
    varName: "registered_year",
    label: "Year Registered",
    description: "Enter the year when the ships were registered. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_nationality = new TreeselectVariable({
    varName: "nationality",
    label: "Flag",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_imputed_nationality = new TreeselectVariable({
    varName: "imputed_nationality",
    label: "Flag Imputed",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_rig_of_vessel = new TreeselectVariable({
    varName: "rig_of_vessel",
    label: "Rig of Vessel",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_tonnage = new NumberVariable({
    varName: "tonnage",
    label: "Tonnage",
    description: "The tonnage of the ships. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_tonnage_mod = new NumberVariable({
    varName: "tonnage_mod",
    label: "Standardized Tonnage",
    description: "This is the standardized tonnage calculated by the algorithms. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_guns_mounted = new NumberVariable({
    varName: "guns_mounted",
    label: "Guns Mounted",
    description: "This is the guns mounted on the ship. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

// all
shipNationOwner = {
  voyagesAndVessels: {
    var_voyage_id: var_voyage_id,

    // var_voyage_in_cd_rom: {
    //   varName: 'var_voyage_in_cd_rom',
    //   value: {
    //     op: "equals to",
    //     searchTerm0: null,
    //     searchTerm1: null,
    //   },
    //   changed: false,
    //   activated: false,
    // },

    var_ship_name_plaintext: var_ship_name_plaintext,
    var_owner_plaintext: var_owner_plaintext,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  constructionAndRegistration: {
    var_year_of_construction: var_year_of_construction,

    // var_vessel_construction_place: {
    //   varName: 'vessel_construction_place',
    //   value: {
    //     op: "equals to",
    //     searchTerm0: null,
    //     searchTerm1: null,
    //   },
    //   changed: false,
    //   activated: false,
    // },

    var_registered_year: var_registered_year,

    // var_registered_place: {
    //   varName: 'registered_place',
    //   value: {
    //     op: "equals to",
    //     searchTerm0: null,
    //     searchTerm1: null,
    //   },
    //   changed: false,
    //   activated: false,
    // },

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
