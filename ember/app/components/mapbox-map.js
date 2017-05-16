import Ember from 'ember';
//import mapbox-gl mixin

export default Ember.Component.extend({

  defaultDescription: {
    title: "Role of Regions",
    description: "Click on names of designated regions on the map for descriptions of the role of each in the trans-Atlantic slave trade.",
  },

  clickedMarkerTitle: Ember.computed('clickedMarker', function() {
    if (this.get("clickedMarker")) {
      return `${this.get("clickedMarker")["title"]}`;
    } else {
      return this.get('defaultDescription')["title"];
    }
  }),

  clickedMarkerText: Ember.computed("clickedMarker", function(marker) {
    if (this.get("clickedMarker")) {
      return `${this.get("clickedMarker")["description"]}`;
    } else {
      return this.get('defaultDescription')["description"];
    }
  }),

  didInsertElement: function() {
    var _that = this;

    // locations
    var geos = {
      north_america: {
        title: "North America",
        longLat: [-97.723250, 48.395696],
        description: "The North American mainland played a relatively minor role in the trans-Atlantic slave trade. Its ports sent out less than five percent of all known voyages, and its slave markets absorbed less than four percent of all slaves carried off from Africa. An intra-American trade in slaves – originating in the Caribbean - supplied additional slaves, however. This region was exceptional in the Americas in that a positive rate of natural population growth began relatively early, thus reducing the dependence of the region on coerced migrants.",
      },
      caribbean: {
        title: "Caribbean",
        longLat: [-78.712509, 21.377507],
        description: "The Caribbean was one of the two major broad regional markets for slaves from Africa. Over the two centuries when the trade was at its height, the major locations for sugar production, and therefore the major slave markets, shifted from the eastern Caribbean to the west. Here, first Jamaica, then St. Domingue, and finally in the nineteenth century, Cuba, absorbed most of the slaves brought into the region. As this implies, few islands developed self-sustaining populations at any point in the slave trade era. Caribbean ports also sent out more slaving expeditions to Africa than did the North American mainland ports.",
      },
      europe: {
        title: "Europe",
        longLat: [15.2551, 54.5260],
        description: "Europe was the starting point for about half of all trans-Atlantic slaving voyages. This traffic dominated the West African to Caribbean section of the slave trade. The major ports were at first located in the Iberian peninsula, but by the eighteenth century northern European ports had become dominant. After 1807, France and the Iberian ports sent out the great majority of European-based slaving voyages. The European consumers’ demand for sugar was the driving force behind 350 years of trans-Atlantic slave trading.",
      },
      africa: {
        title: "Africa",
        longLat: [20.7832, 20.5085],
        description: "Sub-Saharan Africa lost over twelve and a half million people to the trans-Atlantic slave trade alone between 1525 and 1867. Perhaps as many again were carried off to slave markets across the Sahara and the Indian Ocean. Over forty percent of captives left from West-central Africa alone with most of the remainder leaving from the Bight of Benin, the Bight of Biafra, and the Gold Coast. About one in eight died on board the slave vessel and many others died prior to departure and after arrival. Departures were channeled through a dozen or so major embarkation points such as Whydah, Bonny, Loango, Luanda, and Benguela, though many smaller ports also supplied slaves.",
      },
      brazil: {
        title: "Brazil",
        longLat: [-46.689409, -0.120857],
        description: "Brazil was the center of the slave trade carried on under the Portuguese flag, both before and after Brazilian independence in 1822, and Portugal was by far the largest of the national carriers. Brazil dominated the slave trade in the sense that Rio de Janeiro and Bahia sent out more slaving voyages than any port in Europe, and certainly many times more than did Lisbon. Over nearly three centuries between 1560 and 1850, Brazil was consistently the largest destination for slaves in the Americas. Almost all the slaves coming into the region came from just two coastal areas in Africa: the Bight of Benin and West-central Africa.",
      },
    }

    mapboxgl.accessToken = 'pk.eyJ1IjoibXNsZWUiLCJhIjoiclpiTWV5SSJ9.P_h8r37vD8jpIH1A6i1VRg';
    var map = new mapboxgl.Map({
      attributionControl: false,
      container: 'map',
      style: 'mapbox://styles/mslee/cif5p01n202nisaktvljx9mv3',
      center: [-30, 17], // starting position
      zoom: 1, // starting zoom
      minZoom: 1,
      maxZoom: 1
    });
    map.scrollZoom.disable();

    // create the marker
    Object.keys(geos).forEach(function(key) {
      var longLat = geos[key]["longLat"];

      // create DOM element for the marker
      var el = document.createElement('div');
      el.class = 'mapbox-marker';

      // send click to an event handler
      $(el).on("click", function() {
        debugger;
        _that.set('clickedMarker', geos[key]);
      });

      var popup = new mapboxgl.Popup({
          offset: 25
        })
        .setText(geos[key]["title"]);

      new mapboxgl.Marker(el, {
          offset: [-25, -25]
        })
        .setLngLat(longLat)
        .setPopup(popup) // sets a popup on this marker
        .addTo(map);
    })
  },

  actions: {
    notify: function(item) {
      console.log(`item notified ${item}`)
    }
  }

});
