// Definitions of source reference types.
// Each type should have:
// validate() method - yielding null if no validation errors are found,
//                     or a descriptive string in case of errors.
// toString() method - a descriptive string for the reference type which is
//                     used by the page to display a summary of the reference.

function PrimarySource(library, location, series, volume, detail, info, id) {
    this.type = 'Primary source';
    this.library = library;
    this.location = location;
    this.series = series;
    this.volume = volume;
    this.detail = detail;
    this.info = info;
    this.id = id;
    var self = this;
    this.validate = function () {
        return null;
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
}