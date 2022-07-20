const offensiveTextDisclaimer = (value) => {
  const customWarning = pgettext("possibly-offensive-label", value);
  return customWarning === value
    ? gettext("Note: this term was used in historical records and appears here in this form to accurately represent the historical sources.")
    : customWarning;
}

function getBadgeFormattedValue(value, maybeOffensive) {
  maybeOffensive = !!maybeOffensive;
  return `<span class="h6 pr-2"><span title="${maybeOffensive ? offensiveTextDisclaimer(value) : ''}" class="badge badge-pill badge-secondary tooltip-pointer ${maybeOffensive ? 'badge-maybe-offensive' : ''}" data-toggle="tooltip" data-placement="top">${value}</span></span>`;
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
      if (item['name']) {
        value += getBadgeFormattedValue(item.name, item['possibly_offensive']);
      } else {
        value += getBadgeFormattedValue(item, false);
      }
    });
  }
  return value;
}