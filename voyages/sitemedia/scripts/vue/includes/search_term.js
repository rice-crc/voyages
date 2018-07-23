function VariableInfo(varName, varGroup, label) {
	var self = this;
	self.varGroup = varGroup;
	self.varName = varName;
	self.label = label;
}

function SearchTerm(varInfo, operatorLabel, initialSearchTerm, description, validationFunction) {
	var self = this;
	self.varInfo = varInfo;
	self.description = description || '';
	self.__searchTerm = initialSearchTerm || '';
	self.label = varInfo.label;
	self.group = varInfo.varGroup;
	self.varName = varInfo.varName;
	self.operatorLabel = operatorLabel || ' = ';
	self.validate = function() {
		return validationFunction ? validationFunction(self.__searchTerm) : [];
	};
	self.getSearchTerm = function() { return self.__searchTerm; };
	self.setSearchTerm = function(term) {
		self.__searchTerm = term;
	};
	self.inputControlId = 'TextSearchTerm_' + self.varName;
	self.linkText = function(escape) {
		return self.operatorLabel + ' "' + escape(self.__searchTerm) + '"';
	};
	self.linkId = '__search_var_link_' + self.varName;
	self.render = function(escape) {
		return '<div class="item" data-var_name="' + self.varName + '"><em>' + self.label + '</em>&nbsp;<a id="' + self.linkId + '" class="search_query_link" href="#">' + self.linkText(escape) + '</a></div>';
	};
	self.inputId = "__search_input_entry";
	self.inputFocus = function() {
		$("#" + self.inputId).focus();
	};
	self.inputHtml = function(escape) {
		return '<div class="form-group"><label for="' + self.inputId + '" class="control-label">' + self.label + '&nbsp;' + self.operatorLabel + ':&nbsp;&nbsp;</label><input type="text" class="form-control" id="' + self.inputId + '" value="' + escape(self.__searchTerm) + '"></div>';
	};
	self.initInput = function() {
	};
	self.updateFromHtmlInput = function() {
		var text = $("#" + self.inputId).val();
		self.setSearchTerm(text);
		return text;
	};
	self.enterKeyPress = function() { return true; };
	self.serialize = function() {
		return {varName: self.varName, op: self.operatorLabel, searchTerm: self.__searchTerm};
	};
	self.deserialize = function(data, callback) {
		self.operatorLabel = data.op;
		self.setSearchTerm(data.searchTerm);
		if (callback) callback(self);
	};
}
//
// Selectize.define('places', function(options) {
// 	var self = this;
// 	self.onOptionSelect = (function() {
// 		var original = self.onOptionSelect;
// 		return function(e) {
// 			if (e.preventDefault) {
// 				e.preventDefault();
// 				e.stopPropagation();
// 			}
// 			if (e.originalEvent && e.originalEvent.originalTarget) {
// 				// Check if this is the link to add region or broad region.
// 				if ($(e.originalEvent.originalTarget).hasClass('option_add_all')) {
// 					original.apply(this, arguments);
// 					return;
// 				}
// 			}
// 			if (e.type && e.type == 'mousedown') return false;
// 			var target = $(e.currentTarget);
// 			var className = "expanded";
// 			if (this.$control_input.val() != '' && !this.options.create) {
// 				// Clear search if user selected an option.
// 				id = target.attr('id');
// 				this.$control_input.val('');
// 				this.refreshOptions();
// 				if (id) {
// 					target = $("#" + id);
// 				}
// 			}
// 			var nextActive = null;
// 			if (target.hasClass("broad_region")) {
// 				nextActive = ".broad_region_" + target.data('pk');
// 				var isExpanded = $(nextActive + ":first").hasClass(className);
// 				$(".broad_region,.region,.port").removeClass(className);
// 				$(".tree_expanded").removeClass('tree_expanded').addClass("tree_collapsed");
// 				if (isExpanded) return false;
// 				target.removeClass("tree_collapsed").addClass("tree_expanded").addClass(className);
// 				$(".broad_region_" + target.data('pk')).addClass(className);
// 				this.setTextboxValue('');
// 			} else if (target.hasClass("region")) {
// 				nextActive = ".region_" + target.data('pk');
// 				var isExpanded = $(nextActive + ":first").hasClass(className);
// 				$(".port").removeClass(className);
// 				$(".region.tree_expanded").removeClass('tree_expanded').addClass("tree_collapsed");
// 				if (isExpanded) return false;
// 				target.removeClass("tree_collapsed").addClass("tree_expanded").addClass(className);;
// 				$(".region_" + target.data('pk')).addClass(className);
// 				this.setTextboxValue('');
// 			} else {
// 				original.apply(this, arguments);
// 			}
// 		};
// 	})();
// });

function PlacesData() {
	var self = this;
	self.all = [];
	self.allDict = {};
	self.broadRegions = {};
	self.regions = {};
	self.ports = {};
	self.isLoaded = false;
	self.initAsync = function(callback) {
		if (!self.isLoaded) {
			$.get('/contribute/places_ajax', function(data) {
				// Process data.
				// Here we assume that the data is properly
				// order so that each port appears after the
				// region that it belongs to and the region
				// appears after the broad region it belongs to.
				var broadRegions = {};
				var regions = {};
				var ports = {};
				var allDict = {};
				for (var i = 0; i < data.length; ++i) {
					var item = data[i];
					if (item.type == "port") {
						item.region = regions[item.parent];
						item.pk = item.value;
						item.label = item.port;
						ports[item.value] = item;
					} else if (item.type == "region") {
						item.broad_region = broadRegions[item.parent];
						item.label = item.region;
						item.ports = []
						regions[item.pk] = item;
					} else if (item.type == "broad_region") {
						item.label = item.broad_region;
						item.ports = []
						broadRegions[item.pk] = item;
					}
					allDict[item.value] = item;
				}
				for (var key in ports) {
					var p = ports[key];
					var r = p.region;
					var b = r.broad_region;
					r.ports.push(p.code);
					b.ports.push(p.code);
				}
				self.isLoaded = true;
				self.all = data;
				self.allDict = allDict;
				self.broadRegions = broadRegions;
				self.regions = regions;
				self.ports = ports;
				callback(self);
			});
		} else {
			callback(self);
		}
	};
	return self;
}

// Store places data in a shared variable so that
// we only need one AJAX call to fill it.
var placesData = new PlacesData();

function PlaceSearchTerm(varInfo, operatorLabel, initialSearchTerm, description, validationFunction) {
	var self = new SearchTerm(varInfo, operatorLabel, initialSearchTerm, description, validationFunction);
	var oldInputHtml = self.inputHtml;
	self.inputHtml = function(escape) {
		return oldInputHtml(escape).replace('<input ', '<input class="select_port" ');
	};
	self.selectize = null;
	self.initInput = function() {
		self.selectize = null;
		placesData.initAsync(function(data) {
			$('#' + self.inputId).selectize({
				plugins: {
					'places': true,
					'dropdown_header': {
						'title': 'Select the ports that should be included in the search. You may select entire regions or broad regions (not yet implemented).'
					},
				},
				maxItems: 10000,
				options: data.all,
				valueField: 'value',
				searchField: ['port', 'region', 'broad_region'],
				selectOnTab: false,
				sortField: 'order',
				render: {
					option: function(data, escape) {
						if (data.type == 'port') {
							return '<div class="port region_' + data.parent + '">' + escape(data.port) + '</div>';
						}
						if (data.type == 'region') {
							return '<div id="r_' + data.pk + '" data-pk="' + data.pk + '" class="mouse_transparent tree_collapsed region broad_region_' + data.parent + '">' + escape(data.region) + ' (<a class="option_add_all">add all</a>)</div>';
						}
						return '<div id="br_' + data.pk + '" data-pk="' + data.pk + '" class="mouse_transparent broad_region tree_collapsed">' + escape(data.broad_region) + ' (<a class="option_add_all">add all</a>)</div>';
					},
					item: function(data, escape) {
						if (data.type == "broad_region") {
							return '<div>' + escape(data.broad_region) + '</div>';
						}
						if (data.type == "region") {
							return '<div><span class="geo_complement">' + escape(data.broad_region.broad_region) + ' &raquo;&nbsp;</span>' + escape(data.region) + '</div>';
						}
						var region = data.region;
						var broad_region = region.broad_region;
						return '<div><span class="geo_complement">' + escape(broad_region.broad_region) + ' &raquo; ' + escape(region.region) + ' &raquo; </span>' + escape(data.port) + '</div>';
					},
				},
				onInitialize: function() {
					self.selectize = $("#" + self.inputId)[0].selectize;
					items = self.getSearchTerm();
					for (var i = 0; i < items.length; ++i) {
						self.selectize.addItem(items[i].value);
					}
				}
			});
		});
	};
	self.inputFocus = function() {
		if (self.selectize) {
			self.selectize.focus();
		}
	};
	self.linkText = function(escape) {
		var items = self.getSearchTerm();
		var text = '';
		var MAX_TEXT_LENGTH = 65;
		for (var i = 0; i < items.length; ++i) {
			if (text.length > 0) text += ', ';
			var next = items[i].label;
			if (text.length + next.length > MAX_TEXT_LENGTH) {
				text = text + next + ' and ' + (items.length - i - 1) + ' more...';
				break;
			} else {
				text += next;
			}
		}
		return self.operatorLabel + ' "' + escape(text) + '"';
	};
	self.updateFromHtmlInput = function() {
		var selection = $.map(
			self.selectize.items,
			function(value) {
				return self.selectize.options[value];
			}
		);
		self.setSearchTerm(selection);
		return selection;
	};
	self.getBackendSearchTerm = function() {
		return $.map(
			self.getSearchTerm(),
			function(item) {
				return item.type == 'port' ? item.code : item.ports;
			}
		)
	};
	self.serialize = function() {
		return {varName: self.varName, items: self.selectize ? $.makeArray(self.selectize.items) : []};
	}
	self.deserialize = function(serialized, callback) {
		placesData.initAsync(function(data) {
			self.setSearchTerm($.map(serialized.items, function(value) { return data.allDict[parseInt(value)]; }));
			if (callback) callback(self);
		});
	}
	return self;
}

function RangeSearchTerm(varInfo, operatorLabel, initialSearchTerm, description, validationFunction, initialRangeMode) {
	var self = new SearchTerm(varInfo, operatorLabel, initialSearchTerm, description, validationFunction);
	var isValidSearchTermVal = function() {
		return self.__searchTerm.constructor === Array && self.__searchTerm.length == 2;
	};
	var rangeOptionLabels = ['equals', 'is at most', 'is at least', 'is between'];
	self.rangeMode = initialRangeMode || 0;
	self.inputHtml = function(escape) {
		if (!isValidSearchTermVal()) {
			self.__searchTerm = [null, null];
		}
		var rangeOptions = '<select class="form-control" id="__range_search_mode">';
		for (var i = 0; i < rangeOptionLabels.length; ++i) {
			rangeOptions += '<option value="' + i + '"' + (i == self.rangeMode ? ' selected>' : '>') + rangeOptionLabels[i] + '</option>';
		}
		rangeOptions += '</select>';
		return '<div class="form-group"><label for="' + self.inputId + '" class="control-label">' + self.label + '&nbsp;' + rangeOptions + '&nbsp;:&nbsp;&nbsp;</label><input type="number" class="form-control number-input" id="' + self.inputId + '" value="' + escape(self.__searchTerm[0] || '') + '">' +
		'<span id="__range_split_span" style="display:none">&nbsp;-&nbsp;</span><input type="number" class="form-control number-input" id="' + self.inputId + '_right" style="display:none;" value="' + escape(self.__searchTerm[1] || '') + '"></div>';
	};
	self.initInput = function() {
		var updateControls = function() {
			var operatorValue = $('#__range_search_mode').val();
			var isRange = operatorValue == 3;
			$('#' + self.inputId + '_right').toggle(isRange);
			$('#__range_split_span').toggle(isRange);
			self.operatorLabel = rangeOptionLabels[operatorValue];
		};
		$('#__range_search_mode').change(updateControls);
		updateControls();
	};
	self.linkText = function(escape) {
		var text = self.__searchTerm[0] || '';
		if (self.rangeMode == 3) {
			text += ' - ' + (self.__searchTerm[1] || '');
		}
		return rangeOptionLabels[self.rangeMode] + ' "' + escape(text) + '"';
	};
	self.updateFromHtmlInput = function() {
		var rangeModeVal = $("#__range_search_mode").val();
		if (rangeModeVal < 0 || rangeOptionLabels >= rangeOptionLabels.length) {
			rangeModeVal = -1;
		}
		var first = $("#" + self.inputId).val();
		var arr = [parseInt(first), null];
		if (rangeModeVal == 3) {
			arr[1] = parseInt($("#" + self.inputId + '_right').val());
		}
		self.rangeMode = rangeModeVal;
		self.setSearchTerm(arr);
		return arr;
	};
	self.validate = function() {
		var errors = [];
		if (self.rangeMode < 0 || self.rangeMode >= rangeOptionLabels.length) {
			errors.push('Invalid range mode selection');
		}
		if (!isValidSearchTermVal() || isNaN(parseInt(self.__searchTerm[0])) || (self.rangeMode == 3 && isNaN(parseInt(self.__searchTerm[1])))) {
			errors.push('Missing or invalid value or range');
		}
		if (self.rangeMode == 3) {
			var v1 = parseInt(self.__searchTerm[0]);
			var v2 = parseInt(self.__searchTerm[1]);
			if (v1 > v2) {
				errors.push('Invalid range');
			}
		}
		if (validationFunction) {
			errors = errors.concat(validationFunction(self.__searchTerm));
		}
		return errors;
	};
	self.serialize = function() {
		return {varName: self.varName, rangeMode: self.rangeMode, searchTerm: self.__searchTerm};
	};
	self.deserialize = function(data, callback) {
		self.rangeMode = data.rangeMode;
		self.operatorLabel = rangeOptionLabels[data.rangeMode];
		self.setSearchTerm(data.searchTerm);
		if (callback) callback(self);
	};
	return self;
}

function TextSearchTerm(varInfo, operatorLabel, initialSearchTerm, description, validationFunction) {
	return new SearchTerm(varInfo, operatorLabel, initialSearchTerm, description, validationFunction);
}
