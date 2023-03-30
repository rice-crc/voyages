const tabs = {
    // Tables Tab
    tables: {
        row: {
            // currently selected value
            variable: "tabs.tables.row",
            value: 1,
            options: [
                { id: 0, varName: "voyage_ship__imputed_nationality__label", label: gettext("Flag*")},
                { id: 1, varName: "voyage_itinerary__imp_region_voyage_begin__region", label: gettext("Region where voyage began")},
                { id: 2, varName: "voyage_itinerary__imp_port_voyage_begin__place", label: gettext("Port where voyage began*")},
                { id: 3, varName: "voyage_itinerary__imp_principal_region_of_slave_purchase__region", label: gettext("Embarkation regions")},
                { id: 4, varName: "voyage_itinerary__imp_principal_place_of_slave_purchase__place", label: gettext("Principal place of purchase*")},
                { id: 5, varName: "voyage_itinerary__imp_principal_region_slave_dis__region", label: gettext("Specific regions of disembarkation")},
                { id: 6, varName: "voyage_itinerary__imp_principal_port_slave_dis__place", label: gettext("Principal place of landing*")},
                { id: 7, varName: "year", label: gettext("Year") },
                { id: 8, varName: "year_5", label: gettext("Five-Year") }
            ],
        },
        column: {
            // currently selected value
            variable: "tabs.tables.column",
            value: 0,
            options: [
                { id: 0, varName: "voyage_ship__imputed_nationality__label", label: gettext("Flag*")},
                { id: 1, varName: "voyage_itinerary__imp_region_voyage_begin__region", label: gettext("Region where voyage began")},
                { id: 2, varName: "voyage_itinerary__imp_port_voyage_begin__place", label: gettext("Port where voyage began*")},
                { id: 3, varName: "voyage_itinerary__imp_principal_region_of_slave_purchase__region", label: gettext("Embarkation regions")},
                { id: 4, varName: "voyage_itinerary__imp_principal_place_of_slave_purchase__place", label: gettext("Principal place of purchase*")},
                { id: 5, varName: "voyage_itinerary__imp_principal_region_slave_dis__region", label: gettext("Specific regions of disembarkation")},
                { id: 6, varName: "voyage_itinerary__imp_principal_port_slave_dis__place", label: gettext("Principal place of landing*")}
            ],
        },
        cell: {
            // currently selected value
            variable: "tabs.tables.cell",
            value: 0,
            options: [
                { id: 0, varName: "pk", label: gettext("Number of voyages") },
                { id: 1, varName: "voyage_slaves_numbers__imp_total_num_slaves_embarked", label: gettext("Sum of embarked captives*"), agg_mode: "SUM" },
                { id: 2, varName: "voyage_slaves_numbers__imp_total_num_slaves_disembarked", label: gettext("Sum of disembarked captives*"), agg_mode: "SUM" }
            ]
        }
    },    
    visualization: {
        scatter: {
            x: {
                // currently selected value
                variable: "tabs.visualization.scatter.x",
                value: 0,
                options: [
                    { id: 0, varName: "year", label: gettext("Year") },
                    { id: 1, varName: "language", label: gettext("Language groups") }
                ]
            },
            y: {
                // currently selected value
                variable: "tabs.visualization.scatter.y",
                value: 0,
                options: [
                    { id: 0, varName: "enslaved_id", sourceVarName: "enslaved_id", label: gettext("Number of captives") },
                    { id: 1, varName: "voyage_id", label: gettext("Number of voyages") },
                    { id: 2, varName: "gender_code", label: gettext("Percent female") },
                    { id: 3, varName: "gender_code", label: gettext("Percent male") },
                    { id: 4, varName: "age_group", label: gettext("Percent under 16 years of age") }
                ]
            },
        }
    }
};