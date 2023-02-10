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

var_year_range = new NumberVariable({
    varName: "year_range",
    label: gettext("Arrival Year"),
    description: "",
  },{
    op: "is between",
    searchTerm0: minVoyageYear,
    searchTerm1: 1866
  },{
    isImputed: false,
    isAdvanced: false
  });

var_enslaved_count = new NumberVariable({
    varName: "enslaved_count",
    label: gettext("Number of Captives"),
    description: "",
  },{
    op: "is at least",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_roles = new TreeselectVariable({
    varName: "roles",
    label: gettext("Enslaver Roles"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_voyage_datasets = new TreeselectVariable({
    varName: "voyage_datasets",
    label: gettext("Voyages Dataset"),
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

// all
itinerary = {
  itinerary: {
    var_voyage_id: var_voyage_id,
    var_ship_name: var_ship_name,
    var_year_range: var_year_range,
    var_enslaved_count: var_enslaved_count,
    var_voyage_datasets: var_voyage_datasets,
    var_roles: var_roles,

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
