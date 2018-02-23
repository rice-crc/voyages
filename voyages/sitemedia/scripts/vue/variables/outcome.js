var_outcome_voyage = new TreeselectVariable({
    varName: "outcome_voyage",
    label: "Particular Outcome of Voyage",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_outcome_slaves = new TreeselectVariable({
    varName: "outcome_slaves",
    label: "Outcome of Voyage for Slaves",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_outcome_ship_captured = new TreeselectVariable({
    varName: "outcome_ship_captured",
    label: "Outcome of Voyage if Ship Captured",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_outcome_owner = new TreeselectVariable({
    varName: "outcome_owner",
    label: "Outcome of Voyage for Owner",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_resistance = new TreeselectVariable({
    varName: "resistance",
    label: "African Resistance",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

outcome = {
  outcome: {
    var_outcome_voyage: var_outcome_voyage,
    var_outcome_slaves: var_outcome_slaves,
    var_outcome_ship_captured: var_outcome_ship_captured,
    var_outcome_owner: var_outcome_owner,
    var_resistance: var_resistance,

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
