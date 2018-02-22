var_imp_port_voyage_begin = new PlaceVariable({
    varName: "imp_port_voyage_begin",
    label: "Place where Voyage Began",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_imp_principal_place_of_slave_purchase = new PlaceVariable({
    varName: "imp_principal_place_of_slave_purchase",
    label: "Principal Place of Purchase",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_first_place_slave_purchase = new PlaceVariable({
    varName: "first_place_slave_purchase",
    label: "1st Place of Purchase",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_second_place_slave_purchase = new PlaceVariable({
    varName: "second_place_slave_purchase",
    label: "2nd Place of Purchase",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_third_place_slave_purchase = new PlaceVariable({
    varName: "third_place_slave_purchase",
    label: "3rd Place of Purchase",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_port_of_call_before_atl_crossing = new PlaceVariable({
    varName: "port_of_call_before_atl_crossing",
    label: "Places of Call before Atlantic Crossing",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_port_of_call_before_atl_crossing = new PlaceVariable({
    varName: "port_of_call_before_atl_crossing",
    label: "Places of Call before Atlantic Crossing",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_imp_principal_port_slave_dis = new PlaceVariable({
    varName: "imp_principal_port_slave_dis",
    label: "Principal Place of Slave Landing",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_first_landing_place = new PlaceVariable({
    varName: "first_landing_place",
    label: "1st Place of Slave Landing",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_second_landing_place = new PlaceVariable({
    varName: "second_landing_place",
    label: "2nd Place of Slave Landing",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_third_landing_place = new PlaceVariable({
    varName: "third_landing_place",
    label: "3rd Place of Slave Landing",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

var_place_voyage_ended = new PlaceVariable({
    varName: "place_voyage_ended",
    label: "Place where Voyage Ended",
    description: "description",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

itinerary = {
  departure: {
    var_imp_port_voyage_begin: var_imp_port_voyage_begin,
    count: {
      changed: 0,
      activated: 0,
    }
  },

  purchase: {
    var_imp_principal_place_of_slave_purchase: var_imp_principal_place_of_slave_purchase,
    var_first_place_slave_purchase: var_first_place_slave_purchase,
    var_second_place_slave_purchase: var_second_place_slave_purchase,
    var_third_place_slave_purchase: var_third_place_slave_purchase,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  call: {
    var_port_of_call_before_atl_crossing: var_port_of_call_before_atl_crossing,
    count: {
      changed: 0,
      activated: 0,
    }
  },

  landing: {
    var_imp_principal_port_slave_dis: var_imp_principal_port_slave_dis,
    var_first_landing_place: var_first_landing_place,
    var_second_landing_place: var_second_landing_place,
    var_third_landing_place: var_third_landing_place,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  destination: {
    var_place_voyage_ended: var_place_voyage_ended,
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
