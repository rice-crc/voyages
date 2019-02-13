var_outcome_voyage = new TreeselectVariable({
    varName: "outcome_voyage",
    label: gettext("Particular outcome of voyage"),
    description: gettext(""),
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false,
  });

var_outcome_slaves = new TreeselectVariable({
    varName: "outcome_slaves",
    label: gettext("Outcome of voyage for slaves"),
    description: gettext(""),
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_outcome_ship_captured = new TreeselectVariable({
    varName: "outcome_ship_captured",
    label: gettext("Outcome of voyage if ship captured"),
    description: gettext(""),
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false,
  });

var_outcome_owner = new TreeselectVariable({
    varName: "outcome_owner",
    label: gettext("Outcome of voyage for owner"),
    description: gettext(""),
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_resistance = new TreeselectVariable({
    varName: "resistance",
    label: gettext("African resistance"),
    description: gettext(""),
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false,
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
