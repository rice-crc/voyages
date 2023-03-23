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
                { id: 2, varName: "voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__place", label: gettext("Principal place of purchase*") },
                { id: 3, varName: "voyage__voyage_itinerary__imp_principal_port_slave_dis__place", label: gettext("Principal place of landing*") },
                { id: 4, varName: "all_lang_groups", sourceVarName: "language", label: gettext("All language groups") }
            ],
        },
        column: {
            // currently selected value
            variable: "tabs.tables.column",
            value: 2,
            options: [
                { id: 0, varName: "voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__place", label: gettext("Principal place of purchase*") },
                { id: 1, varName: "voyage__voyage_itinerary__imp_principal_port_slave_dis__place", label: gettext("Principal place of landing*") },
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
                { id: 2, varName: "age_group", label: gettext("Age group (A: adult, C: child)") }
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
            value: 0,
            options: [
                { id: 0, varName: "age_5", label: gettext("Age (5-year steps)") },
                { id: 1, varName: "voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__place", label: gettext("Principal place of purchase*") }
            ],
        },
        column: {
            // currently selected value
            variable: "tabs.tables.column",
            value: 0,
            options: [
                { id: 0, varName: "gender_code", label: gettext("Gender") },
                { id: 1, varName: "voyage__voyage_itinerary__imp_principal_port_slave_dis__place", label: gettext("Principal place of landing*") },
            ],
        },
        cell: {
            // currently selected value
            variable: "tabs.tables.cell",
            value: 0,
            options: [
                { id: 0, varName: "number_of_captives", sourceVarName: "", label: gettext("Number of captives") },
            ]
        }
    }
};

const tabs = [tabAO, tabOoK];

const genderLabels = [gettext('Unspecified'), gettext('Male'), gettext('Female')];