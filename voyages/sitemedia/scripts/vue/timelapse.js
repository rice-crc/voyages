// Dictionary that maps flag_id to filename
var FLAGNAMES = {
  1: "Spain",
  2: "Uruguay",
  3: "Spain_Uruguay",
  4: "Portugal",
  5: "Brazil",
  6: "Portugal_Brazil",
  7: "United-Kingdom",
  8: "Netherlands",
  9: "United-States",
  10: "France",
  11: "Denmark",
  13: "Sweden",
  15: "Mexico",
  17: "Norway",
  18: "Denmark_Baltic",
  19: "Argentina",
  20: "Russia"
};

// year label
Vue.component("v-voyage-info", {
  props: ["data", "isVisible"],
  template: `<div class="timelapse-info-container timelapse-info-card" v-if="isVisible">
              <div class='voyage-title-container'>
                <div class='voyage-info-title'>
                  {{shipName}}
                </div>
                <div class='voyage-info-close' @click="close">
                  <i class='fas fa-times'></i>
                </div>
              </div>

              <div class='voyage-nationality-container' v-if="nationalityName">
                <div class='voyage-nationality-title'>
                  {{nationalityName}}
                </div>
                <img :src="flagImgSrc" class='voyage-nationality-flag'>
              </div>

              <div class='voyage-description-container'>
                <p>
                  This <span v-if="shipTonnage">{{shipTonnage}} tons</span> ship 
                  left {{source}} with {{data.embarked}} enslaved people and 
                  arrived in {{destination}} with {{data.disembarked}}.
                </p>
              </div>

              <div class='voyage-actions-container'>
                <button type="button" class="btn btn-info btn-sm" @click="readMore">Read More</button>
              </div>

            </div>`,

  created() {},
  computed: {
    // compute ship name, which comes from the data object
    shipName() {
      var shipName = (this.data.ship_name || "").trim();
      shipName = shipName != "" ? shipName : gettext("Ship Name Unknown");
      return shipName;
    },

    // compute ship nationality, which comes from the data object
    nationalityName() {
      return this.data.ship_nationality_name || false;
    },

    // compute tonnage
    shipTonnage() {
      return this.data.ship_ton ? parseInt(this.data.ship_ton) : false;
    },

    source() {
      return gettext(this.data.source_name);
    },

    destination() {
      return gettext(this.data.destination_name);
    },

    // compute flag
    flag() {
      return "flag_" + this.data.nat_id;
    },

    // compute flag image source
    flagImgSrc() {
      var filename = FLAGNAMES[this.data.nat_id];
      var path = "/static/images/flags/";
      var extension = ".png";
      return path + filename + extension;
    }
  },
  methods: {
    close() {
      this.$emit("close-timelapse-info");
    },
    readMore() {
      $vm = this;
      var request = buildRequestBody(this.data.voyage_id, SV_MODE == "intra");
      axios({
        method: "POST",
        url: SEARCH_URL,
        data: request
      })
        .then(function(response) {
          console.log(response.data.data[0]);
          var processedResponse = processResponse(response.data);
          $vm.$emit("set-row-data", processedResponse);
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
});

// year label
Vue.component("v-year", {
  props: ["currentYear"],
  template: `<div class="timelapse-info-container" id="timelapse-year">
        <div class="timelapse-year">{{currentYear}}</div>
        </div>`
});

// speed shifter
Vue.component("v-speed", {
  props: ["speeds", "multiplier", "ui", "options", "control"],
  data: function() {
    return {
      currentIndex: 2
    };
  },
  template:
    '<button type="button" class="btn btn-sm btn-light margin" :class="{ active: isActive }" @click=shift>{{currentSpeed}}x</button>',
  methods: {
    setSpeed: function() {
      var multipliedSpeed = this.speeds[this.currentIndex] * this.multiplier;
      // console.log("multiplied speed is: " + multipliedSpeed);
      this.ui.monthsPerSecond = multipliedSpeed;
      this.control.setStepPerSec(
        multipliedSpeed * 10,
        Math.max(1.0, 12 / multipliedSpeed)
      );
    },

    shift: function() {
      // update UI display
      var next = this.currentIndex + 1;
      if (next < this.speeds.length) {
        Vue.set(this, "currentIndex", this.currentIndex + 1);
      } else {
        Vue.set(this, "currentIndex", 0);
      }

      // update animation speed
      this.setSpeed();
    }
  },
  computed: {
    // returns the currentSpeed as a text label
    currentSpeed: function() {
      return this.speeds[this.currentIndex];
    },

    // set this to active whenever it is not the default speed (2x)
    isActive: function() {
      return this.currentIndex != 2;
    }
  },
  updated: function() {
    this.setSpeed();
  }
});

// play/pause button
Vue.component("v-play", {
  props: ["ui", "control"],
  data: function() {
    return {
      play: false,
    };
  },
  template: `<button type="button" class="btn btn-sm btn-light" @click=toggle v-if="play"><i class="fas fa-play"></i></button>
  <button type="button" class="btn btn-sm btn-light" @click=toggle v-else><i class="fas fa-pause"></i></button>`,
  methods: {
    toggle: function() {
      this.play = !this.play;
      if (this.control.isPaused()) {
        this.ui.play();
      } else {
        this.ui.pause();
      }
    }
  }
});

// fullscreen toggle button
Vue.component("v-fullscreen", {
  data: function() {
    return {
      isFullscreen: false
    };
  },
  template: `<button type="button" class="btn btn-sm btn-light" @click=toggle><i class="fas fa-compress"></i></button>`,
  methods: {
    toggle: function() {
      if (document.fullscreen) {
        this.exitFullscreen();
        this.isFullscreen = false;
      } else {
        this.enterFullscreen();
        this.isFullscreen = true;
      }
    },

    // enter fullscreen based on browser
    enterFullscreen: function() {
      var map = document.getElementById("map");
      if (map.requestFullscreen) {
        map.requestFullscreen();
      } else if (map.mozRequestFullScreen) {
        /* Firefox */
        map.mozRequestFullScreen();
      } else if (map.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        map.webkitRequestFullscreen();
      } else if (map.msRequestFullscreen) {
        /* IE/Edge */
        map.msRequestFullscreen();
      }
    },

    // exit fullscreen based on browser
    exitFullscreen: function() {
      var map = document.getElementById("map");
      if (map.requestFullscreen) {
        document.exitFullscreen();
      } else if (map.mozRequestFullScreen) {
        /* Firefox */
        document.mozCancelFullScreen();
      } else if (map.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (map.msRequestFullscreen) {
        /* IE/Edge */
        document.msExitFullscreen();
      }
    }
  }
});
