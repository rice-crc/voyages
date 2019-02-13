var_captain = new TextVariable({
    varName: "captain",
    label: gettext("Captain's name"),
    description: gettext(""),
  },{
    op: "is equal to",
    searchTerm: null,
  },{
    isImputed: false,
    isAdvanced: false
  });

var_crew_voyage_outset = new NumberVariable({
    varName: "crew_voyage_outset",
    label: gettext("Crew at voyage outset"),
    description: gettext(""),
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_crew_first_landing = new NumberVariable({
    varName: "crew_first_landing",
    label: gettext("Crew at first landing of slaves"),
    description: gettext(""),
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isadvanced: false
  });

var_crew_died_complete_voyage = new NumberVariable({
    varName: "crew_died_complete_voyage",
    label: gettext("Crew deaths during voyage"),
    description: gettext(""),
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });


captainAndCrew = {
  captainAndCrew: {
    var_captain: var_captain,
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
