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