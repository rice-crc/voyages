var var_imp_arrival_at_port_of_dis = new YearVariable({
    varName: "imp_arrival_at_port_of_dis",
    label: gettext("Year range"),
    description: "",
  },{
    op: "is between",
    searchTerm0: 1514,
    searchTerm1: 1866
  },{
    isImputed: true,
    isAdvanced: false
  });

year = {
  year: {
    var_imp_arrival_at_port_of_dis: var_imp_arrival_at_port_of_dis,
    count: {
      changed: 0,
      activated: 0,
    }
  },
  count: {
    changed: 0,
    activated: 0,
  },
};
