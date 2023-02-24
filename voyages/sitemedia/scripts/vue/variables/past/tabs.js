const tabAO = {
    // Tables Tab
    tables: {
        row: {
            // currently selected value
            variable: "tabs.tables.row",
            value: 1,
            options: [
                { id: 0, varName: "year", label: gettext("Year") },
                { id: 1, varName: "year_5", label: gettext("Five-Year") },
                { id: 2, varName: "voyage__voyage_itinerary__principal_place_slave_embark", label: gettext("Principal place of purchase*") },
                { id: 3, varName: "voyage__voyage_itinerary__principal_place_slave_disembark", label: gettext("Principal place of landing*") },
                { id: 4, varName: "all_lang_groups", sourceVarName: "language", label: gettext("All language groups") }
            ],
        },
        column: {
            // currently selected value
            variable: "tabs.tables.column",
            value: 2,
            options: [
                { id: 0, varName: "voyage__voyage_itinerary__principal_place_slave_embark", label: gettext("Principal place of purchase*") },
                { id: 1, varName: "voyage__voyage_itinerary__principal_place_slave_disembark", label: gettext("Principal place of landing*") },
                { id: 2, varName: "top7_lang_groups", sourceVarName: "language", maxResults: 7, label: gettext("Top 7 language groups") }
            ],
        },
        cell: {
            // currently selected value
            variable: "tabs.tables.cell",
            value: 0,
            options: [
                { id: 0, varName: "number_of_captives", sourceVarName: "", label: gettext("Number of captives") },
                { id: 1, varName: "gender_code", label: gettext("Gender") },
                { id: 2, varName: "age_group", label: gettext("Age group") }
            ]
        }
    }
};

const tabOoK = {
    // Tables Tab
    tables: {
        row: {
            // currently selected value
            variable: "tabs.tables.row",
            value: 4,
            options: [
                { id: 0, varName: "var_imputed_nationality_idnum", label: gettext("Flag*") },
                { id: 4, varName: "var_imp_principal_region_of_slave_purchase_idnum", label: gettext("Embarkation regions")},
                { id: 5, varName: "var_imp_principal_place_of_slave_purchase_idnum", label: gettext("Principal place of purchase*")},
            ],
        },
        column: {
            // currently selected value
            variable: "tabs.tables.column",
            value: 7,
            options: [
                { id: 8, varName: "var_imp_principal_port_slave_dis_idnum", label: gettext("Principal place of landing*") }
            ],
        },
        cell: {
            // currently selected value
            variable: "tabs.tables.cell",
            value: 1,
            options: [
                { id: 0, label: gettext("Number of voyages"), functions: { "cell": "unique(var_voyage_id)" } }
            ]
        }
    }
};

const tabs = [tabAO, tabOoK];