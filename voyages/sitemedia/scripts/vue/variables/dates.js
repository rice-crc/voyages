var_imp_length_home_to_disembark = new NumberVariable({
    varName: "imp_length_home_to_disembark",
    label: "Voyage Length, Homeport to Slaves Landing (days)",
    description: "Enter the number of crew at voyage outset. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

var_length_middle_passage_days = new NumberVariable({
    varName: "length_middle_passage_days",
    label: "Middle Passage (days)",
    description: "Enter the number of crew at first landing of slaves. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

dates = {
  dates: {
    var_imp_length_home_to_disembark: var_imp_length_home_to_disembark,
    var_length_middle_passage_days: var_length_middle_passage_days,
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
