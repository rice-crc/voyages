function TreeselectVariable(varInfo, searchTerms, options) {
  this.type = "treeselect";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
    isMultiple: typeof options["isMultiple"] !== 'undefined' ? options["isMultiple"] : true,
    disableBranchNodes: typeof options["disableBranchNodes"] !== 'undefined' ? options["disableBranchNodes"] : false,
    maxLength: typeof options["maxLength"] !== 'undefined' ? options["maxLength"] : 0,
    caption: options["caption"],
    data: [{
      id: "0",
      label: gettext("Select all"),
      children: []
    }],
  };
  this.changed = false;
  this.activated = false;
}

function NumberVariable(varInfo, searchTerms, options) {
  this.type = "number";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm0: searchTerms["searchTerm0"],
    searchTerm1: searchTerms["searchTerm1"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm0: searchTerms["searchTerm0"],
    searchTerm1: searchTerms["searchTerm1"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
  };
  this.changed = false;
  this.activated = false;
}

function PercentageVariable(varInfo, searchTerms, options) {
  this.type = "number";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm0: searchTerms["searchTerm0"],
    searchTerm1: searchTerms["searchTerm1"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm0: searchTerms["searchTerm0"],
    searchTerm1: searchTerms["searchTerm1"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
  };
  this.changed = false;
  this.activated = false;
}

function DateVariable(varInfo, searchTerms, options, isPartial) {
  this.type = "number";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm0: searchTerms["searchTerm0"],
    searchTerm1: searchTerms["searchTerm1"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm0: searchTerms["searchTerm0"],
    searchTerm1: searchTerms["searchTerm1"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
  };
  this.changed = false;
  this.activated = false;
  this.isPartial = !!isPartial;
}

function YearVariable(varInfo, searchTerms, options) {
  this.type = "number";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm0: searchTerms["searchTerm0"],
    searchTerm1: searchTerms["searchTerm1"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm0: searchTerms["searchTerm0"],
    searchTerm1: searchTerms["searchTerm1"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
  };
  this.changed = false;
  this.activated = false;
}

function TextVariable(varInfo, searchTerms, options) {
  this.type = "text";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
  };
  this.changed = false;
  this.activated = false;
}

function PlaceVariable(varInfo, searchTerms, options) {
  this.type = "place";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
    isMultiple: typeof options["isMultiple"] !== 'undefined' ? options["isMultiple"] : true,
    disableBranchNodes: typeof options["disableBranchNodes"] !== 'undefined' ? options["disableBranchNodes"] : false,
    maxLength: typeof options["maxLength"] !== 'undefined' ? options["maxLength"] : 0,
    caption: options["caption"]
  };
  this.changed = false;
  this.activated = false;
}


function BooleanVariable(varInfo, searchTerms, options) {
  this.type = "boolean";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
    isToDo: typeof options["isToDo"] !== 'undefined' ? options["isToDo"] : false,
  };
  this.changed = false;
  this.activated = false;
}

function LanguageGroupVariable(varInfo, searchTerms, options) {
  this.type = "treeselect";
  this.varName = varInfo["varName"];
  this.label = varInfo["label"];
  this.description = varInfo["description"];
  this.default = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.value = {
    op: searchTerms["op"],
    searchTerm: searchTerms["searchTerm"],
  };
  this.options = {
    isImputed: options["isImputed"],
    isAdvanced: options["isAdvanced"],
    isMultiple: typeof options["isMultiple"] !== 'undefined' ? options["isMultiple"] : true,
    disableBranchNodes: typeof options["disableBranchNodes"] !== 'undefined' ? options["disableBranchNodes"] : false,
    maxLength: typeof options["maxLength"] !== 'undefined' ? options["maxLength"] : 0,
    caption: options["caption"],
    data: [{
      id: "0",
      label: gettext("Select all"),
      children: []
    }],
  };
  this.changed = false;
  this.activated = false;
}