var_imp_port_voyage_begin_id = new PlaceVariable({
    varName: "imp_port_voyage_begin_id",
    label: "Place where Voyage Began",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: true,
    isAdvanced: false
  });

var_imp_principal_place_of_slave_purchase_id = new PlaceVariable({
    varName: "imp_principal_place_of_slave_purchase_id",
    label: "Principal Place of Purchase",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: true,
    isAdvanced: false
  });

var_first_place_slave_purchase_id = new PlaceVariable({
    varName: "first_place_slave_purchase_id",
    label: "1st Place of Purchase",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_second_place_slave_purchase_id = new PlaceVariable({
    varName: "second_place_slave_purchase_id",
    label: "2nd Place of Purchase",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_third_place_slave_purchase_id = new PlaceVariable({
    varName: "third_place_slave_purchase_id",
    label: "3rd Place of Purchase",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_port_of_call_before_atl_crossing_id = new PlaceVariable({
    varName: "port_of_call_before_atl_crossing_id",
    label: "Places of Call before Atlantic Crossing",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_imp_principal_port_slave_dis_id = new PlaceVariable({
    varName: "imp_principal_port_slave_dis_id",
    label: "Principal Place of Slave Landing",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: true,
    isAdvanced: false
  });

var_first_landing_place_id = new PlaceVariable({
    varName: "first_landing_place_id",
    label: "1st Place of Slave Landing",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_second_landing_place_id = new PlaceVariable({
    varName: "second_landing_place_id",
    label: "2nd Place of Slave Landing",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_third_landing_place_id = new PlaceVariable({
    varName: "third_landing_place_id",
    label: "3rd Place of Slave Landing",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isadvanced: false
  });

var_place_voyage_ended_id = new PlaceVariable({
    varName: "place_voyage_ended_id",
    label: "Place where Voyage Ended",
    description: "",
  },{
    op: "is one of",
    searchTerm: [],
  },{
    isImputed: false,
    isAdvanced: false
  });

itinerary = {
  departure: {
    var_imp_port_voyage_begin_id: var_imp_port_voyage_begin_id,
    count: {
      changed: 0,
      activated: 0,
    }
  },

  purchase: {
    var_imp_principal_place_of_slave_purchase_id: var_imp_principal_place_of_slave_purchase_id,
    var_first_place_slave_purchase_id: var_first_place_slave_purchase_id,
    var_second_place_slave_purchase_id: var_second_place_slave_purchase_id,
    var_third_place_slave_purchase_id: var_third_place_slave_purchase_id,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  call: {
    var_port_of_call_before_atl_crossing_id: var_port_of_call_before_atl_crossing_id,
    count: {
      changed: 0,
      activated: 0,
    }
  },

  landing: {
    var_imp_principal_port_slave_dis_id: var_imp_principal_port_slave_dis_id,
    var_first_landing_place_id: var_first_landing_place_id,
    var_second_landing_place_id: var_second_landing_place_id,
    var_third_landing_place_id: var_third_landing_place_id,

    count: {
      changed: 0,
      activated: 0,
    }
  },

  destination: {
    var_place_voyage_ended_id: var_place_voyage_ended_id,
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
