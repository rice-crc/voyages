var_captain_plaintext = new TextVariable({
    varName: "captain_plaintext",
    label: "Captain's Name",
    description: "The name of the captain. This could a partial keyword.",
  },{
    op: "equals to",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_crew_voyage_outset = new NumberVariable({
    varName: "crew_voyage_outset",
    label: "Crew at Voyage Outset",
    description: "Enter the number of crew at voyage outset. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_crew_first_landing = new NumberVariable({
    varName: "crew_first_landing",
    label: "Crew at First Landing of Slaves",
    description: "Enter the number of crew at first landing of slaves. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_crew_died_complete_voyage = new NumberVariable({
    varName: "crew_died_complete_voyage",
    label: "Crew Deaths during Voyage",
    description: "Enter the number of crew death during voyages. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });


captainAndCrew = {
  captainAndCrew: {
    var_captain_plaintext: var_captain_plaintext,
    var_crew_voyage_outset: var_crew_voyage_outset,
    var_crew_first_landing: var_crew_first_landing,
    var_crew_died_complete_voyage: var_crew_died_complete_voyage,
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
