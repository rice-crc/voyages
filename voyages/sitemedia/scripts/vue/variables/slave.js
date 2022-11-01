var_imp_total_num_slaves_purchased = new NumberVariable({
    varName: "imp_total_num_slaves_purchased",
    label: gettext("Total embarked"),
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
    label: gettext("Total embarked"),
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
    label: gettext("Total disembarked"),
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
    label: pgettext("filter select label", "SLINTEND"),
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
    label: pgettext("filter select label", "NCAR13"),
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
    label: pgettext("filter select label", "NCAR15"),
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
    label: pgettext("filter select label", "NCAR17"),
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
    label: pgettext("filter select label", "SLAARRIV"),
    description: pgettext("filter select description", "SLAARRIV"),
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
    label: pgettext("filter select label", "SLAS32"),
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
    label: pgettext("filter select label", "SLAS36"),
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
    label: pgettext("filter select label", "SLAS39"),
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
    label: gettext("Percent men"),
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
    label: gettext("Percent women"),
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
    label: gettext("Percent boys"),
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
    label: gettext("Percent girls"),
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
    label: gettext("Percent males"),
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
    label: gettext("Percent children"),
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
    label: pgettext("filter select label", "VYMRTIMP"),
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
    label: pgettext("filter select label", "VYMRTRAT"),
    description: pgettext("filter select description", "VYMRTRAT"),
  },{
    op: "is equal to",
    searchTerm0: null,
    searchTerm1: null
  },{
    isImputed: false,
    isAdvanced: false
  });

var_afrinfo = new TreeselectVariable({
    varName: "afrinfo",
    label: pgettext("filter select label", "AFRINFO"),
    description: pgettext("filter select description", "AFRINFO"),
  },{
    op: "is one of",
    searchTerm: [],
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

  africanInfo: {
    var_afrinfo: var_afrinfo,
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
