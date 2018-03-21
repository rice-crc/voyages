var_length_middle_passage_days = new NumberVariable({
    varName: "length_middle_passage_days",
    label: "Middle Passage (days)",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

var_voyage_began = new DateVariable({
    varName: "voyage_began",
    label: "Year Voyage Began",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_slave_purchase_began = new DateVariable({
    varName: "slave_purchase_began",
    label: "Year Trade Began in Africa",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_date_departed_africa = new DateVariable({
    varName: "date_departed_africa",
    label: "Year Vessel Departed Africa",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_first_dis_of_slaves = new DateVariable({
    varName: "first_dis_of_slaves",
    label: "Year Vessel Arrived with Slaves",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_departure_last_place_of_landing = new DateVariable({
    varName: "departure_last_place_of_landing",
    label: "Year Vessel Departed for Homeport",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_voyage_completed = new DateVariable({
    varName: "voyage_completed",
    label: "Year Voyage Completed",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_imp_length_home_to_disembark = new NumberVariable({
    varName: "imp_length_home_to_disembark",
    label: "Voyage Length, Homeport to Slaves Landing (days)",
    description: "",
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
    var_length_middle_passage_days: var_length_middle_passage_days,
    var_voyage_began: var_voyage_began,
    var_slave_purchase_began: var_slave_purchase_began,
    var_date_departed_africa: var_date_departed_africa,
    var_first_dis_of_slaves: var_first_dis_of_slaves,
    var_departure_last_place_of_landing: var_departure_last_place_of_landing,
    var_voyage_completed: var_voyage_completed,
    var_imp_length_home_to_disembark: var_imp_length_home_to_disembark,
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
