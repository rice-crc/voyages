// Definitions of source reference types.
// Each type should have:
// validate() method - returns a ValidationResult object.
// toString() method - a descriptive string for the reference type which is
//                     used by the page to display a summary of the reference.

function ValidationResult(warnings, errors) {
    this.warnings = warnings || [];
    this.errors = errors || [];
    var self = this;
    this.hasErrors = function () {
        return self.errors.length > 0;
    };
    this.hasWarnings = function () {
        return self.warnings.length > 0;
    };
    this.toString = function() {
        var result = '';
        if (self.warnings.length != 0) {
            result = gettext('Warnings: ') + "\n" + self.warnings.join("\n");
        }
        if (self.errors.length != 0) {
            if (result != '') result += "\n";
            result += gettext('Errors: ') + "\n" + self.errors.join("\n");
        }
        return result;
    };
}

var _bindFrom = function(self) {
    return function() {
        self.id = $("#source_id_field").val();
        for (var key in self._fields) {
            var inputId = self._fields[key][0];
            self[key] = $("#" + inputId).val();
        }
        return self;
    };
};

var _bindTo = function(self) {
    return function() {
        $("#source_id_field").val(self.id);
        for (var key in self._fields) {
            var inputId = self._fields[key][0];
            $("#" + inputId).val(self[key]);
        }
        return self;
    };
}

var _fromModel = function(self) {
    return function(model) {
        for (var key in self._fields) {
            var fieldName = self._fields[key][1];
            self[key] = model[fieldName];
        }
        return self;
    };
};

var _toModel = function(self) {
    return function() {
        var model = {};
        for (var key in self._fields) {
            var fieldName = self._fields[key][1];
            model[fieldName] = self[key];
        }
        model['type'] = self.type;
        return model;
    };
}

function validateMinLength(val, minLength) {
    return $.type(val) === 'string' && val.length >= minLength;
}

function validateInt(val, minValue, maxValue, notNull) {
    minValue = minValue || Number.MIN_VALUE;
    maxValue = maxValue || Number.MAX_VALUE;
    if ($.type(val) === 'string') {
        if (val == '') return notNull ? false : true;
        val = parseInt(val);
    }
    if (val.isNaN()) return false;
    return val >= minValue && val <= maxValue;
}

function validateYear(val, notNull) {
    return validateInt(val, 1500, 1867, notNull);
}

function PrimarySource(library, location, series, volume, detail, info, url, id) {
    this.type = 'Primary source';
    this.library = library;
    this.location = location;
    this.series = series;
    this.volume = volume;
    this.detail = detail;
    this.info = info;
    this.url = url;
    this.id = id;
    var self = this;
    this.validate = function () {
        var errors = [];
        if (!validateMinLength(self.library, 4)) {
            errors.push(gettext("Library or archive name is mandatory"));
        }
        return new ValidationResult([], errors);
    };
    this.toString = function () {
        var result = self.library + ', ' + self.location;
        if (self.series) {
            result += ' - ' + self.series;
        }
        if (self.volume) {
            result += ', v. ' + self.volume;
        }
        return result;
    };
    this._fields = {
        "library": ["primary_name", "name_of_library_or_archive"],
        "location": ["primary_loc", "location_of_library_or_archive"],
        "series": ["primary_series", "series_or_collection"],
        "volume": ["primary_vol", "volume_or_box_or_bundle"],
        "detail": ["primary_detail", "document_detail"],
        "info": ["primary_info", "information"],
        "url": ["primary_url", "url"],
    };
    this.bindFromForm = _bindFrom(this);
    this.bindToForm = _bindTo(this);
    this.fromModel = _fromModel(this);
    this.toModel = _toModel(this);
}

function ArticleSource(author, title, journal, volume, year, pageStart, pageEnd, info, url, id) {
    this.type = 'Article source';
    this.author = author;
    this.title = title;
    this.journal = journal;
    this.volume = volume;
    this.year = year;
    this.pageStart = pageStart;
    this.pageEnd = pageEnd;
    this.info = info;
    this.url = url;
    this.id = id;
    var self = this;
    this.validate = function () {
        var errors = [];
        var warnings = [];
        if (!validateMinLength(self.author, 4)) {
            errors.push(gettext("Author name is mandatory"));
        }
        if (!validateMinLength(self.title, 4)) {
            errors.push(gettext("Title is mandatory"));
        }
        if (!validateMinLength(self.journal, 4)) {
            warnings.push(gettext("Journal is a recommended field"));
        }
        if (parseInt(self.year) < 1500) {
            errors.push(gettext('Reference year cannot be earlier than 1500'))
        }
        return new ValidationResult(warnings, errors);
    };
    this.toString = function () {
        var result = self.author + ', ' + self.title;
        if (self.journal) {
            result += ' - ' + self.journal;
        }
        if (self.volume) {
            result += ', v. ' + self.volume;
        }
        return result;
    };
    this._fields = {
        "author": ["article_author", "authors"],
        "title": ["article_title", "article_title"],
        "journal": ["article_journal", "journal"],
        "volume": ["article_volume", "volume_number"],
        "year": ["article_year", "year"],
        "pageStart": ["article_first_page", "page_start"],
        "pageEnd": ["article_last_page", "page_end"],
        "info": ["article_info", "information"],
        "url": ["article_url", "url"],
    };
    this.bindFromForm = _bindFrom(this);
    this.bindToForm = _bindTo(this);
    this.fromModel = _fromModel(this);
    this.toModel = _toModel(this);
}

function BookSource(author, title, publisher, place, year, pageStart, pageEnd, info, url, id) {
    this.type = 'Book source';
    this.author = author;
    this.title = title;
    this.publisher = publisher;
    this.place = place;
    this.year = year;
    this.pageStart = pageStart;
    this.pageEnd = pageEnd;
    this.info = info;
    this.url = url;
    this.id = id;
    var self = this;
    this.validate = function () {
        var errors = [];
        var warnings = [];
        if (!validateMinLength(self.author, 4)) {
            errors.push(gettext("Author name is mandatory"));
        }
        if (!validateMinLength(self.title, 4)) {
            errors.push(gettext("Title is mandatory"));
        }
        if (!validateMinLength(self.publisher, 4)) {
            warnings.push(gettext("Publisher is a recommended field"));
        }
        if (parseInt(self.year) < 1500) {
            errors.push(gettext('Reference year cannot be earlier than 1500'))
        }
        return new ValidationResult(warnings, errors);
    };
    this.toString = function () {
        var result = self.author + ', ' + self.title;
        if (self.publisher) {
            result += ' - ' + self.publisher;
        }
        if (self.place) {
            result += ', ' + self.place;
        }
        return result;
    };
    this._fields = {
        "author": ["book_author", "authors"],
        "title": ["book_title", "book_title"],
        "publisher": ["book_publisher", "publisher"],
        "place": ["book_pub_place", "place_of_publication"],
        "year": ["book_year", "year"],
        "pageStart": ["book_first_page", "page_start"],
        "pageEnd": ["book_last_page", "page_end"],
        "info": ["book_info", "information"],
        "url": ["book_url", "url"],
    };
    this.bindFromForm = _bindFrom(this);
    this.bindToForm = _bindTo(this);
    this.fromModel = _fromModel(this);
    this.toModel = _toModel(this);
}

function OtherSource(title, location, page, info, url, id) {
    this.type = 'Other source';
    this.title = title;
    this.location = location;
    this.page = page;
    this.info = info;
    this.url = url;
    this.id = id;
    var self = this;
    this.validate = function () {
        var errors = [];
        var warnings = [];
        if (!validateMinLength(self.title, 4)) {
            errors.push(gettext("Title is mandatory"));
        }
        if (!validateMinLength(self.info, 4)) {
            warnings.push(gettext("Information is a recommended field"));
        }
        if (!validateMinLength(self.url, 4)) {
            warnings.push(gettext("URL is a recommended field"));
        }
        return new ValidationResult(warnings, errors);
    };
    this.toString = function () {
        var result = self.title;
        if (self.publisher) {
            result += ' - ' + self.location;
        }
        return result;
    };
    this._fields = {
        "title": ["other_title", "title"],
        "location": ["other_location", "location"],
        "page": ["other_page", "page"],
        "info": ["other_info", "information"],
        "url": ["other_url", "url"],
    };
    this.bindFromForm = _bindFrom(this);
    this.bindToForm = _bindTo(this);
    this.fromModel = _fromModel(this);
    this.toModel = _toModel(this);
}

function sourceFactory(data, id) {
    var source = null;
    var fields = null;
    if (data.model && data.fields) {
        // Construct object based on Django model's JSON representation.
        if (data.model == 'contribute.interimprimarysource') {
            source = new PrimarySource();
        } else if (data.model == 'contribute.interimarticlesource') {
            source = new ArticleSource();
        } else if (data.model == 'contribute.interimbooksource') {
            source = new BookSource();
        } else if (data.model == 'contribute.interimothersource') {
            source = new OtherSource();
        }
        fields = data.fields;
    } else if (data.type) {
        // Construct object based on JS object's JSON representation.
        if (data.type == 'Primary source') {
            source = new PrimarySource();
        } else if (data.type == 'Article source') {
            source = new ArticleSource();
        } else if (data.type == 'Book source') {
            source = new BookSource();
        } else if (data.type == 'Other source') {
            source = new OtherSource();
        }
        fields = data;
    }
    if (source != null && fields != null) {
        source.fromModel(fields);
        if (id) {
            source.id = id;
        }
    }
    return source;
}

// Form utility functions.
function parseDateValue(val) {
    var items = val.split(',');
    var year = null;
    var month = null;
    var day = null;
    for (var i = 0; i < items.length; ++i) {
        var item = items[i];
        if (item.startsWith('y')) {
            year = parseInt(item.substring(1));
        } else if (item.startsWith('m')) {
            month = parseInt(item.substring(1));
        } else if (item.startsWith('d')) {
            day = parseInt(item.substring(1));
        }
    }
    if (year != null && isNaN(year)) {
        year = null;
    }
    if (month != null && isNaN(month)) {
        month = null;
    }
    if (day != null && isNaN(day)) {
        day = null;
    }
    var result = { year: year, month: month, day: day };
    result.isValid = function() {
        // Date is considered valid if it has at least a year.
        // If it has a day, it must have a month as well.
        return result.year != null && (result.day == null || result.month != null);
    };
    result.toMMDDYYY = function() {
        return (result.month || '') + ',' + (result.day || '') + ',' + (result.year || '');
    };
    return result;
};

function optionIntCompare(a, b) {
    if (a != null && b != null) {
        return a - b;
    }
    return null;
}

function dateCompare(a, b) {
    var yc = optionIntCompare(a.year, b.year);
    if (yc == null) return null;
    if (yc != 0) return yc;
    var mc = optionIntCompare(a.month, b.month);
    if (mc == null) return 0;
    if (mc != 0) return mc;
    var dc = optionIntCompare(a.day, b.day);
    if (dc == null) return 0;
    return dc;
}

// Validate the form.
function validatePreSubmit(sources, preSources) {
    var warnings = [];
    var errors = [];
    // Validate dates - must be in order and years within limits.
    var allDateFields = [
        'date_departure',
        'date_slave_purchase_began',
        'date_vessel_left_last_slaving_port',
        'date_first_slave_disembarkation',
        'date_second_slave_disembarkation',
        'date_third_slave_disembarkation',
        'date_return_departure',
        'date_voyage_completed',
    ];
    var dates = $.map(allDateFields, function(field, i) {
        var date = parseDateValue($("input[name='" + field + "']").val());
        if (date.isValid()) return {
            field: field,
            date: date,
        };
    });
    for (var i = 0; i < dates.length - 1; ++i) {
        var a = dates[i];
        var b = dates[i + 1];
        var cmp = dateCompare(a.date, b.date);
        if (cmp > 0) {
            errors.push('Dates are out of order: ' + a.field + ', ' + b.field);
        }
    }
    // Ton type can only be set if tonnage is set.
    var tonType = $("select[name='ton_type']").val();
    var tonnage = $("input[name='tonnage_of_vessel']").val();
    if (!isNaN(parseInt(tonType)) && isNaN(parseInt(tonnage))) {
        errors.push(gettext('Tonnage type is set without a tonnage value.'));
    }
    var yearConstructed = parseInt($("input[name='year_ship_constructed']").val());
    var yearRegistered = parseInt($("input[name='year_ship_registered']").val());
    if (!isNaN(yearConstructed) && !isNaN(yearRegistered) && yearRegistered < yearConstructed) {
        errors.push(gettext('Year of ship registration cannot precede year of ship construction.'));
    }
    // Validate sources - at least one.
    if (sources.length == 0 && preSources.length == 0) {
        errors.push(gettext('The contribution has to specify at least one source reference.'));
    }
    for (var i = 0; i < preSources.length; ++i) {
        var ps = preSources[i];
        if (ps.action != 0 && ps.action != 1 && ps.action != 2) {
            errors.push('Unrecognized action!'); // Should never get here.
        }
        if ((ps.action == 1 || ps.action == 2) && (!ps.notes || ps.notes.length < 3)) {
            errors.push(gettext('Any pre-existing source marked for editing or deletion requires a comment.'));
        }
    }
    return new ValidationResult(warnings, errors);
}

function getVoyagesValues(voyages, name) {
    var values = {};
    var length = 0;
    for (var id in voyages) {
        var v = voyages[id];
        if (v.hasOwnProperty(name)) {
            var value = v[name];
            if (value != null) {
                if (!values.hasOwnProperty(value)) {
                    values[value] = [];
                    ++length;
                }
                values[value].push(id);
            }
        }
    }
    return length > 0 ? values : null;
}

function getGroupName(ids) {
    return (ids.length > 1 ? gettext('Voyages') : gettext('Voyage')) +
            ' ' + ids.join(', ');
};

function getMonthLocaleName(locale, i) {
    var date = new Date(i + "/01/2015");
    return date.toLocaleString(locale, { month: "long" });
};

// Some common constants.
var NUMBERS_KEY_PREFIX = 'interim_slave_number_';
var DEMOGRAPHICS_COLUMN_HEADERS = ['MEN', 'WOMEN', 'BOY', 'GIRL', 'MALE', 'FEMALE', 'ADULT', 'CHILD', 'INFANT'];
var DEMOGRAPHICS_ROW_INDICES = [ 1, 4, 5, 2, 3, 6 ];

function getDemographicsRows(id) {
    return $.map(
        $("#" + id).find("tbody").find("tr"),
        function(row, i) {
            return $(row).find("td");
        }
    );
};

var regex = new RegExp('^' + NUMBERS_KEY_PREFIX + '([A-Z]+)([0-9])$');
function fillDemograhicsTable(id, numbers, editable) {
    demographics_rows = getDemographicsRows(id);
    for (var key in numbers) {
        var match = regex.exec(key);
        var found = false;
        if (match) {
            var col = DEMOGRAPHICS_COLUMN_HEADERS.indexOf(match[1]);
            var row = DEMOGRAPHICS_ROW_INDICES.indexOf(parseInt(match[2]));
            if (col >= 0 && row >= 0 && row < 6) {
                $(demographics_rows[row][col]).html(numbers[key]);
                found = true;
            }
        }
        if (editable && !found) {
            $("input[name='" + key + "']").each(function() {
                $(this).val(numbers[key]);
            });
        }
    }
}
