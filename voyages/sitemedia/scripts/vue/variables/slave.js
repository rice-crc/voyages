var_imp_total_num_slaves_purchased = new NumberVariable({
    varName: "imp_total_num_slaves_purchased",
    label: "Total Slaves Embarked Imputed",
    description: "The total number of slaves embarked before departure. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

var_total_num_slaves_purchased = new NumberVariable({
    varName: "total_num_slaves_purchased",
    label: "Total Slaves Embarked",
    description: "The total number of slaves embarked before departure. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_imp_total_slaves_disembarked = new NumberVariable({
    varName: "imp_total_slaves_disembarked",
    label: "Total Slaves Disembarked Imputed",
    description: "The total number of slaves disembarked after arrival. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });


var_num_slaves_intended_first_port = new NumberVariable({
    varName: "num_slaves_intended_first_port",
    label: "Number of Slaves Intended at First Place of Purchase",
    description: "Number of slaves intended at first place of purchase. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_num_slaves_carried_first_port = new NumberVariable({
    varName: "num_slaves_carried_first_port",
    label: "Slaves Carried from 1st Port of Purchase",
    description: "Number of slaves carried from 1st port of purchase. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_num_slaves_carried_second_port = new NumberVariable({
    varName: "num_slaves_carried_second_port",
    label: "Slaves Carried from 2nd Port of Purchase",
    description: "Number of slaves carried from 2nd port of purchase. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });
var_num_slaves_carried_third_port = new NumberVariable({
    varName: "num_slaves_carried_third_port",
    label: "Slaves Carried from 3rd Port of Purchase",
    description: "Number of slaves carried from 3rd port of purchase. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_total_num_slaves_arr_first_port_embark = new NumberVariable({
    varName: "total_num_slaves_arr_first_port_embark",
    label: "Number of Slaves Arriving at 1st Place of Landing",
    description: "Number of slaves arrived at first place of landing. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_num_slaves_disembark_first_place = new NumberVariable({
    varName: "num_slaves_disembark_first_place",
    label: "Number of Slaves Disembarked at 1st Place of Landing",
    description: "Number of slaves disembarked from 1st port of landing. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });
var_num_slaves_disembark_second_place = new NumberVariable({
    varName: "num_slaves_disembark_second_place",
    label: "Number of Slaves Disembarked at 2nd Place of Landing",
    description: "Number of slaves disembarked from 2nd port of landing. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_num_slaves_disembark_third_place = new NumberVariable({
    varName: "num_slaves_disembark_third_place",
    label: "Number of Slaves Disembarked at 3rd Place of Landing",
    description: "Number of slaves disembarked from 3rd port of landing. This could be a range.",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });


var_imputed_percentage_men = new NumberVariable({
    varName: "imputed_percentage_men",
    label: "Percentage Men",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false
  });

var_imputed_percentage_women = new NumberVariable({
    varName: "imputed_percentage_women",
    label: "Percentage Women",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false
  });

var_imputed_percentage_boys = new NumberVariable({
    varName: "imputed_percentage_boys",
    label: "Percentage Boys",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false
  });

var_imputed_percentage_girls = new NumberVariable({
    varName: "imputed_percentage_girls",
    label: "Percentage Girls",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false
  });

var_imputed_percentage_male = new NumberVariable({
    varName: "imputed_percentage_male",
    label: "Percentage Males",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false
  });

var_imputed_percentage_child = new NumberVariable({
    varName: "imputed_percentage_child",
    label: "Percentage Children",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: false
  });

var_imputed_sterling_cash = new NumberVariable({
    varName: "imputed_sterling_cash",
    label: "Sterling Cash Price in Jamaica",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

var_imputed_death_middle_passage = new NumberVariable({
    varName: "imputed_death_middle_passage",
    label: "Slave Deaths during Middle Passage",
    description: "",
  },{
    op: "equals to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: true,
    isAdvanced: true
  });

var_imputed_mortality = new NumberVariable({
    varName: "imputed_mortality",
    label: "Mortality Rate",
    description: "",
  },{
    op: "equals to",
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
