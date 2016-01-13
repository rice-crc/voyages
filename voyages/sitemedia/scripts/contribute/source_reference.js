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
    };
};

var _bindTo = function(self) {
    return function() {
        $("#source_id_field").val(self.id);
        for (var key in self._fields) {
            var inputId = self._fields[key][0];
            $("#" + inputId).val(self[key]);
        }
    };
}

function validateMinLength(val, minLength) {
    return $.type(val) === 'string' && val.length >= minLength;
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
        "library": ["primary_name"],
        "location": ["primary_loc"],
        "series": ["primary_series"],
        "volume": ["primary_vol"],
        "detail": ["primary_detail"],
        "info": ["primary_info"],
        "url": ["primary_url"],
    };
    this.bindFromForm = _bindFrom(this);
    this.bindToForm = _bindTo(this);
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
        "author": ["article_author"],
        "title": ["article_title"],
        "journal": ["article_journal"],
        "volume": ["article_volume"],
        "year": ["article_year"],
        "pageStart": ["article_first_page"],
        "pageEnd": ["article_last_page"],
        "info": ["article_info"],
        "url": ["article_url"],
    };
    this.bindFromForm = _bindFrom(this);
    this.bindToForm = _bindTo(this);
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
        "author": ["book_author"],
        "title": ["book_title"],
        "publisher": ["book_publisher"],
        "place": ["book_pub_place"],
        "year": ["book_year"],
        "pageStart": ["book_first_page"],
        "pageEnd": ["book_last_page"],
        "info": ["book_info"],
        "url": ["book_url"],
    };
    this.bindFromForm = _bindFrom(this);
    this.bindToForm = _bindTo(this);
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
        if (!validateMinLength(self.information, 4)) {
            warnings.push(gettext("Information is a recommended field"));
        }
        if (!validateMinLength(self.url, 4)) {
            warnings.push(gettext("URL is a recommended field"));
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
        "author": ["book_author"],
        "title": ["book_title"],
        "publisher": ["book_publisher"],
        "place": ["book_pub_place"],
        "year": ["book_year"],
        "pageStart": ["book_first_page"],
        "pageEnd": ["book_last_page"],
        "info": ["book_info"],
        "url": ["book_url"],
    };
    this.bindFromForm = _bindFrom(this);
    this.bindToForm = _bindTo(this);
}