var fieldMap = {
  "Flag*": "var_imputed_nationality_idnum",
  "Broad region where voyage began": "var_imp_broad_region_voyage_begin_idnum",
  "Region where voyage began": "var_imp_region_voyage_begin_idnum",
  "Port where voyage began": "var_imp_port_voyage_begin_idnum",
  "Embarkation Regions": "var_imp_principal_region_of_slave_purchase_idnum",
  "Embarkation Ports": "var_imp_principal_place_of_slave_purchase_idnum",
  "Specific regions of disembarkation": "var_imp_principal_region_slave_dis_idnum",
  "Broad regions of disembarkation": "var_imp_principal_broad_region_disembark_idnum",
  "Disembarkation Ports": "var_imp_principal_port_slave_dis_idnum",
  "Individual Years": "var_imp_arrival_at_port_of_dis",
  "5-year periods": "var_imp_arrival_at_port_of_dis",
  "10-year periods": "var_imp_arrival_at_port_of_dis",
  "25-year periods": "var_imp_arrival_at_port_of_dis",
  "50-year periods": "var_imp_arrival_at_port_of_dis",
  "100-year periods": "var_imp_arrival_at_port_of_dis",
};

function makeYearRange(interval) {
  return { start: 1501, gap: interval, end: 2000 };
}

var otherGraphsXAxes = [
  { id: 0, varName: 'var_imputed_nationality', label: 'Flag*' },
  { id: 1, varName: 'var_rig_of_vessel', label: 'Rig' },
  { id: 2, varName: 'var_outcome_voyage', label: 'Particular outcome of the voyage' },
  { id: 3, varName: 'var_outcome_slaves', label: 'Outcome for slaves*' },
  { id: 4, varName: 'var_outcome_owner', label: 'Outcome for owner*' },
  { id: 5, varName: 'var_outcome_ship_captured', label: 'Outcome if ship captured*' },
  { id: 6, varName: 'var_resistance', label: 'African resistance' },
  { id: 7, varName: 'var_imp_port_voyage_begin', label: 'Place where voyage began*' },
  { id: 8, varName: 'var_imp_region_voyage_begin', label: 'Region where voyage began*' },
  { id: 9, varName: 'var_imp_principal_place_of_slave_purchase', label: 'Principal place of slave purchase*' },
  { id: 10, varName: 'var_imp_principal_region_of_slave_purchase', label: 'Principal region of slave purchase*' },
  { id: 11, varName: 'var_imp_principal_port_slave_dis', label: 'Principal place of slave landing*' },
  { id: 12, varName: 'var_imp_principal_region_slave_dis', label: 'Principal region of slave landing*' },
  { id: 13, varName: 'var_imp_principal_broad_region_disembark', label: 'Broad region of slave landing*' },
  { id: 14, varName: 'var_place_voyage_ended', label: 'Place where voyage ended' },
  { id: 15, varName: 'var_region_voyage_ended', label: 'Region where voyage ended' },
  { id: 16, varName: 'var_voyage_began', label: 'Month voyage began' },
  { id: 17, varName: 'var_slave_purchase_began', label: 'Month trade began in Africa' },
  { id: 18, varName: 'var_date_departed_africa', label: 'Month vessel departed Africa' },
  { id: 19, varName: 'var_first_dis_of_slaves', label: 'Month vessel arrived with slaves' },
  { id: 20, varName: 'var_departure_last_place_of_landing', label: 'Month vessel departed for home port' },
  { id: 21, varName: 'var_voyage_completed', label: 'Month voyage completed' },
  { id: 22, varName: 'var_imp_arrival_at_port_of_dis_mod_5', label: 'Year arrived with slaves (5 year periods)' },
  { id: 23, varName: 'var_imp_arrival_at_port_of_dis_mod_10', label: 'Year arrived with slaves (10 year periods)' },
  { id: 24, varName: 'var_imp_arrival_at_port_of_dis_mod_25', label: 'Year arrived with slaves (25 year periods)' },
];

var graphsYAxes = [
  { id:0, varName: 'var_voyage_id', label: 'Number of voyages' },
  { id:1, varName: 'var_imp_length_home_to_disembark', label: 'Average voyage length, home port to slaves landing (days)*' },
  { id:2, varName: 'var_length_middle_passage_days', label: 'Average middle passage (days)*' },
  { id:3, varName: 'var_tonnage_mod', label: 'Standardized tonnage*' },
  { id:4, varName: 'var_crew_voyage_outset', label: 'Average crew at voyage outset' },
  { id:5, varName: 'var_crew_first_landing', label: 'Average crew at first landing of slaves' },
  { id:6, varName: 'var_crew_voyage_outset', label: 'Total crew at voyage outset' },
  { id:7, varName: 'var_crew_first_landing', label: 'Total crew at first landing of slaves' },
  { id:8, varName: 'var_imp_total_num_slaves_purchased', label: 'Average number of slaves embarked' },
  { id:9, varName: 'var_imp_total_slaves_disembarked', label: 'Average number of slaves disembarked' },
  { id:10, varName: 'var_imp_total_num_slaves_purchased', label: 'Total number of slaves embarked' },
  { id:11, varName: 'var_imp_total_slaves_disembarked', label: 'Total number of slaves disembarked' },
  { id:12, varName: 'var_imputed_percentage_men', label: 'Percentage men*' },
  { id:13, varName: 'var_imputed_percentage_women', label: 'Percentage women*' },
  { id:14, varName: 'var_imputed_percentage_boys', label: 'Percentage boys*' },
  { id:15, varName: 'var_imputed_percentage_girls', label: 'Percentage girls*' },
  { id:16, varName: 'var_imputed_percentage_child', label: 'Percentage children*' },
  { id:17, varName: 'var_imputed_percentage_male', label: 'Percentage male*' },
  { id:18, varName: 'var_imputed_sterling_cash', label: 'Sterling cash price in Jamaica*' },
  { id:19, varName: 'var_resistance', label: 'Rate of resistance' },
  { id:20, varName: 'var_imputed_mortality', label: 'Percentage of slaves embarked who died during voyage*' },
];

var tabs = {
  // Tables Tab
  tables: {
    row: {
      // currently selected value
      variable: "tabs.tables.row",
      value: 12,
      options: [{id: 0, label: "Flag*"},
      {id: 1, label: "Broad region where voyage began"},
      {id: 2, label: "Region where voyage began"},
      {id: 3, label: "Port where voyage began"},
      {id: 4, label: "Embarkation Regions"},
      {id: 5, label: "Embarkation Ports"},
      {id: 6, label: "Specific regions of disembarkation"},
      {id: 7, label: "Broad regions of disembarkation"},
      {id: 8, label: "Disembarkation Ports"},
      {id: 9, label: "Individual Years"},
      {id: 10, label: "5-year periods", range: makeYearRange(5)},
      {id: 11, label: "10-year periods", range: makeYearRange(10)},
      {id: 12, label: "25-year periods", range: makeYearRange(25)},
      {id: 13, label: "50-year periods", range: makeYearRange(50)},
      {id: 14, label: "100-year periods", range: makeYearRange(100)}],
    },
    column: {
      // currently selected value
      variable: "tabs.tables.column",
      value: 6,
      options: [{id: 0, label: "Flag*"},
        {id: 1, label: "Broad region where voyage began"},
        {id: 2, label: "Region where voyage began"},
        {id: 3, label: "Port where voyage began"},
        {id: 4, label: "Embarkation Regions"},
        {id: 5, label: "Embarkation Ports"},
        {id: 6, label: "Specific regions of disembarkation"},
        {id: 7, label: "Broad regions of disembarkation"},
        {id: 8, label: "Disembarkation Ports"}],
    },
    cell: {
      // currently selected value
      variable: "tabs.tables.cell",
      value: 1,
      options: [{id: 0, label: "Number of Voyages", functions: {"cell": "unique(var_voyage_id)"}},
      {id: 1, label: "Sum of embarked slaves", functions: {"cell": "sum(var_imp_total_num_slaves_purchased)"}},
      {id: 2, label: "Average number of embarked slaves", avg: true, functions: {"cell": "avg(var_imp_total_num_slaves_purchased)"}},
      {id: 3, label: "Number of voyages - embarked slaves", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_imp_total_num_slaves_purchased:[* TO *]"}},
      {id: 4, label: "Percent of embarked slaves (row total)", processing: 'perc_row_total', functions: {"cell": "sum(var_imp_total_num_slaves_purchased)"}},
      {id: 5, label: "Percent of embarked slaves (column total)", processing: 'perc_col_total', functions: {"cell": "sum(var_imp_total_num_slaves_purchased)"}},
      {id: 6, label: "Sum of disembarked slaves", functions: {"cell": "sum(var_imp_total_slaves_disembarked)"}},
      {id: 7, label: "Average number of disembarked slaves", avg: true, functions: {"cell": "avg(var_imp_total_slaves_disembarked)"}},
      {id: 8, label: "Number of voyages - disembarked slaves", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_imp_total_slaves_disembarked:[* TO *]"}},
      {id: 9, label: "Percent of disembarked slaves (row total)", processing: 'perc_row_total', functions: {"cell": "sum(var_imp_total_slaves_disembarked)"}},
      {id: 10, label: "Percent of disembarked slaves (column total)", processing: 'perc_col_total', functions: {"cell": "sum(var_imp_total_slaves_disembarked)"}},
      {id: 11, label: "Sum of embarked/disembarked slaves", functions: {"Embarked": "sum(var_imp_total_num_slaves_purchased)", "Disembarked": "sum(var_imp_total_slaves_disembarked)"}},
      {id: 12, label: "Average number of embarked/disembarked slaves", avg: true, functions: {"Embarked": "avg(var_imp_total_num_slaves_purchased)", "Disembarked": "avg(var_imp_total_slaves_disembarked)"}},
      {id: 13, label: "Number of voyages - embarked/disembarked slaves", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_imp_total_num_slaves_purchased:[* TO *] AND var_imp_total_slaves_disembarked:[* TO *]"}},
      {id: 14, label: "Average percentage male", avg: true, format: 'percent', functions: {"cell": "avg(var_imputed_percentage_male)"}},
      {id: 15, label: "Number of voyages - percentage male", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_imputed_percentage_male:[* TO *]"}},
      {id: 16, label: "Average percentage children", avg: true, format: 'percent', functions: {"cell": "avg(var_imputed_percentage_child)"}},
      {id: 17, label: "Number of voyages - percentage children", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_imputed_percentage_child:[* TO *]"}},
      {id: 18, label: "Average percentage of slaves embarked who died during voyage", avg: true, format: 'percent', functions: {"cell": "avg(var_imputed_mortality)"}},
      {id: 19, label: "Number of voyages - percentage of slaves embarked who died during voyage", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_imputed_mortality:[* TO *]"}},
      {id: 20, label: "Average middle passage (days)", avg: true, functions: {"cell": "avg(var_length_middle_passage_days)"}},
      {id: 21, label: "Number of voyages - middle passage (days)", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_length_middle_passage_days:[* TO *]"}},
      {id: 22, label: "Average standarized tonnage", avg: true, functions: {"cell": "avg(var_tonnage_mod)"}},
      {id: 23, label: "Number of voyages - standarized tonnage", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_tonnage_mod:[* TO *]"}},
      {id: 24, label: "Sterling cash price in Jamaica", avg: true, functions: {"cell": "avg(var_imputed_sterling_cash)"}},
      {id: 25, label: "Number of voyages - sterling cash price in Jamaica", functions: {"cell": "unique(var_voyage_id)", "_filter": "var_imputed_sterling_cash:[* TO *]"}},],
    },
  },

  // Data Visualization Tab
  visualization: {
    scatter: {
      x: {
        // currently selected value
        variable: "tabs.visualization.scatter.x",
        value: [0],
        options: [{ id: 0, varName: 'var_imp_arrival_at_port_of_dis', label: 'Year arrived with slaves*' },
        { id: 1, varName: 'var_imp_length_home_to_disembark', label: 'Voyage length, home port to slaves landing (days)*' },
        { id: 2, varName: 'var_length_middle_passage_days', label: 'Middle passage (days)*' },
        { id: 3, varName: 'var_crew_voyage_outset', label: 'Crew at voyage outset' },
        { id: 4, varName: 'var_crew_first_landing', label: 'Crew at first landing of slaves' },
        { id: 5, varName: 'var_imp_total_num_slaves_purchased', label: 'Slaves embarked' },
        { id: 6, varName: 'var_imp_total_slaves_disembarked', label: 'Slaves disembarked' }],
      },
      y: {
        // currently selected value
        variable: "tabs.visualization.scatter.y",
        value: [0],
        options: graphsYAxes,
      },
    },
    bar: {
      x: {
        // currently selected value
        variable: "tabs.visualization.bar.x",
        value: [0],
        options: otherGraphsXAxes,
      },
      y: {
        // currently selected value
        variable: "tabs.visualization.bar.y",
        value: [0],
        options: graphsYAxes,
      },
    },
    donut: {
      sectors: {
        // currently selected value
        variable: "tabs.visualization.donut.sectors",
        value: [0],
        options: otherGraphsXAxes,
      },
      values: {
        // currently selected value
        variable: "tabs.visualization.donut.values",
        value: 0,
        options: graphsYAxes,
      },
    },
  },

  // Timeline Tab
  timeline: {
    chart: {
      // currently selected value
      variable: "tabs.timeline.chart",
      value: 15,
      options: [
        { id: 0, varName: "var_imp_arrival_at_port_of_dis", label: "Number of voyages" },
        { id: 1, varName: "var_tonnage", label: "Average tonnage" },
        { id: 2, varName: "var_tonnage_mod", label: "Average tonnage (standardized)" },
        { id: 3, varName: "var_guns_mounted", label: "Average number of guns" },
        { id: 4, varName: "var_resistance_idnum", label: "Rate of resistance" },
        { id: 5, varName: "var_imp_length_home_to_disembark", label: "Average duration of voyage from home port to disembarkation (days)" },
        { id: 6, varName: "var_length_middle_passage_days", label: "Average duration of middle passage (days)" },
        { id: 7, varName: "var_crew_voyage_outset", label: "Average crew at outset" },
        { id: 8, varName: "var_crew_first_landing", label: "Average crew at first landing of slaves" },
        { id: 9, varName: "var_crew_died_complete_voyage", label: "Number of crew deaths" },
        { id: 10, varName: "var_crew_died_complete_voyage", label: "Average crew deaths" },
        { id: 11, varName: "var_num_slaves_intended_first_port", label: "Intended number of purchases" },
        { id: 12, varName: "var_num_slaves_intended_first_port", label: "Average intended purchases" },
        { id: 13, varName: "var_imp_total_num_slaves_purchased", label: "Total number of captives embarked" },
        { id: 14, varName: "var_imp_total_num_slaves_purchased", label: "Average number of captives embarked" },
        { id: 15, varName: "var_imp_total_slaves_disembarked", label: "Total number of captives disembarked" },
        { id: 16, varName: "var_imp_total_slaves_disembarked", label: "Average number of captives disembarked" },
        { id: 17, varName: "var_imputed_percentage_men", label: "Percentage men (among captives)" },
        { id: 18, varName: "var_imputed_percentage_women", label: "Percentage women (among captives)" },
        { id: 19, varName: "var_imputed_percentage_boys", label: "Percentage boys (among captives)" },
        { id: 20, varName: "var_imputed_percentage_girls", label: "Percentage girls (among captives)" },
        { id: 21, varName: "var_imputed_percentage_female", label: "Percentage female (among captives)" },
        { id: 22, varName: "var_imputed_percentage_male", label: "Percentage male (among captives)" },
        { id: 23, varName: "var_imputed_sterling_cash", label: "Sterling cash price in Jamaica*" },
        { id: 24, varName: "var_imputed_death_middle_passage", label: "Number of slave deaths" },
        { id: 25, varName: "var_imputed_death_middle_passage", label: "Average slave deaths" },
        { id: 26, varName: "var_imputed_mortality", label: "Average percentage of slaves embarked who died during the voyage" }
      ],
    },
  },
}
