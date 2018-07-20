var_length_middle_passage_days = new NumberVariable({
    varName: "length_middle_passage_days",
    label: "Middle Passage (days)",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

var_voyage_began = new DateVariable({
    varName: "voyage_began",
    label: "Date Voyage Began",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_slave_purchase_began = new DateVariable({
    varName: "slave_purchase_began",
    label: "Date Trade Began in Africa",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_date_departed_africa = new DateVariable({
    varName: "date_departed_africa",
    label: "Date Vessel Departed Africa",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_first_dis_of_slaves = new DateVariable({
    varName: "first_dis_of_slaves",
    label: "Date Vessel Arrived with Slaves",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_departure_last_place_of_landing = new DateVariable({
    varName: "departure_last_place_of_landing",
    label: "Date Vessel Departed for Homeport",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: true
  });

var_voyage_completed = new DateVariable({
    varName: "voyage_completed",
    label: "Date Voyage Completed",
    description: "",
  },{
    op: "is equal to",
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
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

dates = {
  overallDates: {
    var_length_middle_passage_days: var_length_middle_passage_days,
    var_imp_length_home_to_disembark: var_imp_length_home_to_disembark,
    count: {
      changed: 0,
      activated: 0,
    }
  },
  durationDates: {
    var_voyage_began: var_voyage_began,
    var_slave_purchase_began: var_slave_purchase_began,
    var_date_departed_africa: var_date_departed_africa,
    var_first_dis_of_slaves: var_first_dis_of_slaves,
    var_departure_last_place_of_landing: var_departure_last_place_of_landing,
    var_voyage_completed: var_voyage_completed,
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
