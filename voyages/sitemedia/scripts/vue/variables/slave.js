var_imp_total_num_slaves_purchased = new NumberVariable({
    varName: "imp_total_num_slaves_purchased",
    label: gettext("Total embarked (imputed)"),
    description: gettext(""),
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
    label: gettext("Total embarked"),
    description: gettext(""),
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
    label: gettext("Total disembarked"),
    description: gettext(""),
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
    label: gettext("Slaves intended at 1st place"),
    description: gettext(""),
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
    label: gettext("Slaves carried from 1st port"),
    description: gettext(""),
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
    label: gettext("Slaves carried from 2nd port"),
    description: gettext(""),
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
    label: gettext("Slaves carried from 3rd port"),
    description: gettext(""),
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
    label: gettext("Slaves arrived at 1st port"),
    description: gettext(""),
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
    label: gettext("Slaves landed at 1st port"),
    description: gettext(""),
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
    label: gettext("Slaves landed at 2nd port"),
    description: gettext(""),
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
    label: gettext("Slaves landed at 3rd port"),
    description: gettext(""),
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
    label: gettext("Percent men"),
    description: gettext(""),
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
    label: gettext("Percent women"),
    description: gettext(""),
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
    label: gettext("Percent boys"),
    description: gettext(""),
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
    label: gettext("Percent girls"),
    description: gettext(""),
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
    label: gettext("Percent males"),
    description: gettext(""),
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
    label: gettext("Percent children"),
    description: gettext(""),
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
    label: gettext("Sterling cash price in Jamaica"),
    description: gettext("Average price paid for men in the Americas as they were sold from the vessel"),
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
    label: gettext("Slaves died during middle passage"),
    description: gettext(""),
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
    label: gettext("Mortality rate"),
    description: gettext("Percent died at sea. Please enter as an integer. e.g. 75"),
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
