function getBadgeFormattedValue(value) {
  return '<span class="h6 pr-2"><span class="badge badge-pill badge-secondary tooltip-pointer" data-toggle="tooltip" data-placement="top"> ' +
        value +
        " </span></span>";
}

// get formated cargo by parsing through the backend response
function getFormattedCargo(cargoArray) {
  var value = ""; // empty value string
  if (cargoArray) {
    cargoArray.forEach(function(item) {
      let cargoText = ""; // empty cargoText string
      let parts = item.split(": ");
      let type = '';
      let ammount = null;
      let unitName = null;
      type = parts[0];
      if (parts.length > 1) {
        parts = parts[1].split(' ');
        ammount = parts[0];
        cargoText += ammount + " ";
        if (parts.length > 1) {
          unitName = parts[1];
          cargoText += unitName + " of ";
        }
      }
      cargoText += type;

      value += getBadgeFormattedValue(cargoText);
    });
  }
  return value;
}

// get formated african info by parsing through the backend response
function getFormattedAfricanInfo(africanInfoArray) {
  var value = ""; // empty value string
  if (africanInfoArray) {
    africanInfoArray.forEach(function(item) {
      value += getBadgeFormattedValue(item);
    });
  }
  return value;
}