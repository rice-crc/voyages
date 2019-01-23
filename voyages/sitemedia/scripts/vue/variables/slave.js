var_imp_total_num_slaves_purchased = new NumberVariable({
    varName: "imp_total_num_slaves_purchased",
    label: "Total embarked (imputed)",
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
    label: "Total embarked",
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
    label: "Total disembarked",
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
    label: "Captives intended",
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
    label: "Captives from 1st port",
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
    label: "Captives from 2nd port",
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
    label: "Captives from 3rd port",
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
    label: "Captives arrived 1st port",
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
    label: "Captives landed 1st port",
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
    label: "Captives landed 2nd port",
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
    label: "Captives landed 3rd port",
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
    label: "Percent men",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_imputed_percentage_women = new PercentageVariable({
    varName: "imputed_percentage_women",
    label: "Percent women",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_imputed_percentage_boys = new PercentageVariable({
    varName: "imputed_percentage_boys",
    label: "Percent boys",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_imputed_percentage_girls = new PercentageVariable({
    varName: "imputed_percentage_girls",
    label: "Percent girls",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_imputed_percentage_male = new PercentageVariable({
    varName: "imputed_percentage_male",
    label: "Percent males",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_imputed_percentage_child = new PercentageVariable({
    varName: "imputed_percentage_child",
    label: "Percent children",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false,
  });

var_imputed_sterling_cash = new NumberVariable({
    varName: "imputed_sterling_cash",
    label: "Sterling cash price in Jamaica",
    description: "Average price paid for men in the Americas as they were sold from the vessel",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isadvanced: false
  });

var_imputed_death_middle_passage = new NumberVariable({
    varName: "imputed_death_middle_passage",
    label: "Captives died during middle passage",
    description: "",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isadvanced: false
  });

var_imputed_mortality = new PercentageVariable({
    varName: "imputed_mortality",
    label: "Mortality rate",
    description: "Percent died at sea. Please enter a Percentage in integer. e.g. 75",
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
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
