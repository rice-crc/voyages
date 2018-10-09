var_imp_total_num_slaves_purchased = new NumberVariable({
    varName: "imp_total_num_slaves_purchased",
    label: "Total Embarked Imputed",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isadvanced: false
  });

var_total_num_slaves_purchased = new NumberVariable({
    varName: "total_num_slaves_purchased",
    label: "Total Embarked",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_imp_total_slaves_disembarked = new NumberVariable({
    varName: "imp_total_slaves_disembarked",
    label: "Total Disembarked",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isadvanced: false
  });


var_num_slaves_intended_first_port = new NumberVariable({
    varName: "num_slaves_intended_first_port",
    label: "Slaves Intended",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_num_slaves_carried_first_port = new NumberVariable({
    varName: "num_slaves_carried_first_port",
    label: "Slaves from 1st Port",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_num_slaves_carried_second_port = new NumberVariable({
    varName: "num_slaves_carried_second_port",
    label: "Slaves from 2nd Port",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });
var_num_slaves_carried_third_port = new NumberVariable({
    varName: "num_slaves_carried_third_port",
    label: "Slaves from 3rd Port",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_total_num_slaves_arr_first_port_embark = new NumberVariable({
    varName: "total_num_slaves_arr_first_port_embark",
    label: "Slaves Arrived 1st Port",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_num_slaves_disembark_first_place = new NumberVariable({
    varName: "num_slaves_disembark_first_place",
    label: "Slaves Landed 1st Port",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });
var_num_slaves_disembark_second_place = new NumberVariable({
    varName: "num_slaves_disembark_second_place",
    label: "Slaves Landed 2nd Port",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_num_slaves_disembark_third_place = new NumberVariable({
    varName: "num_slaves_disembark_third_place",
    label: "Slaves Landed 3rd Port",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });


var_imputed_percentage_men = new PercentageVariable({
    varName: "imputed_percentage_men",
    label: "Percentage Men",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false,
  });

var_imputed_percentage_women = new PercentageVariable({
    varName: "imputed_percentage_women",
    label: "Percentage Women",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false,
  });

var_imputed_percentage_boys = new PercentageVariable({
    varName: "imputed_percentage_boys",
    label: "Percentage Boys",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false,
  });

var_imputed_percentage_girls = new PercentageVariable({
    varName: "imputed_percentage_girls",
    label: "Percentage Girls",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false,
  });

var_imputed_percentage_male = new PercentageVariable({
    varName: "imputed_percentage_male",
    label: "Percentage Males",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false,
  });

var_imputed_percentage_child = new PercentageVariable({
    varName: "imputed_percentage_child",
    label: "Percentage Children",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false,
  });

var_imputed_sterling_cash = new NumberVariable({
    varName: "imputed_sterling_cash",
    label: "Sterling Cash Price in Jamaica",
    description: "Average price paid for men in the Americas as they were sold from the vessel",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isadvanced: false
  });

var_imputed_death_middle_passage = new NumberVariable({
    varName: "imputed_death_middle_passage",
    label: "Slave Deaths during Middle Passage",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isadvanced: false
  });

var_imputed_mortality = new PercentageVariable({
    varName: "imputed_mortality",
    label: "Mortality Rate",
    description: "Please enter a percentage in integer. e.g. 75",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false
  });

slave = {
  overallNumbers: {
    var_imp_total_num_slaves_purchased: var_imp_total_num_slaves_purchased,
    var_total_num_slaves_purchased: var_total_num_slaves_purchased,
    var_imp_total_slaves_disembarked: var_imp_total_slaves_disembarked,
    count: {
      changed: 0,
      activated: 0,
    }
  },

  purchaseNumbers: {
    var_num_slaves_intended_first_port: var_num_slaves_intended_first_port,
    var_num_slaves_carried_first_port: var_num_slaves_carried_first_port,
    var_num_slaves_carried_second_port: var_num_slaves_carried_second_port,
    var_num_slaves_carried_third_port: var_num_slaves_carried_third_port,
    count: {
      changed: 0,
      activated: 0,
    }
  },

  landingNumbers: {
    var_total_num_slaves_arr_first_port_embark: var_total_num_slaves_arr_first_port_embark,
    var_num_slaves_disembark_first_place: var_num_slaves_disembark_first_place,
    var_num_slaves_disembark_second_place: var_num_slaves_disembark_second_place,
    var_num_slaves_disembark_third_place: var_num_slaves_disembark_third_place,
    count: {
      changed: 0,
      activated: 0,
    }
  },

  percentageBySexAndAgeGroup: {
    var_imputed_percentage_men: var_imputed_percentage_men,
    var_imputed_percentage_women: var_imputed_percentage_women,
    var_imputed_percentage_boys: var_imputed_percentage_boys,
    var_imputed_percentage_girls: var_imputed_percentage_girls,
    var_imputed_percentage_male: var_imputed_percentage_male,
    var_imputed_percentage_child: var_imputed_percentage_child,
    count: {
      changed: 0,
      activated: 0,
    }
  },

  otherCharacteristics: {
    var_imputed_sterling_cash: var_imputed_sterling_cash,
    var_imputed_death_middle_passage: var_imputed_death_middle_passage,
    var_imputed_mortality: var_imputed_mortality,
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
