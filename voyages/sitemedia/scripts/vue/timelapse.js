// speed shifter
Vue.component("v-speed", {
  props: ["speeds"],
  data: function() {
    return {
      currentIndex: 0
    };
  },
  template:
    '<button type="button" class="btn btn-sm btn-light margin" :class="{ active: isActive }" @click=shift>{{currentSpeed}}</button>',
  methods: {
    shift: function() {
      var next = this.currentIndex + 1;
      if (next < this.speeds.length) {
        Vue.set(this, "currentIndex", this.currentIndex + 1);
      } else {
        Vue.set(this, "currentIndex", 0);
      }
    }
  },
  computed: {
    currentSpeed: function() {
      return this.speeds[this.currentIndex];
    },
    isActive: function() {
      return this.currentIndex != 0;
    }
  }
});

// play/pause button
Vue.component("v-play", {
  data: function() {
    return {
      play: true
    };
  },
  template: `<button type="button" class="btn btn-sm btn-light" @click=toggle v-if="play"><i class="fas fa-play"></i></button>
  <button type="button" class="btn btn-sm btn-light" @click=toggle v-else><i class="fas fa-pause"></i></button>`,
  methods: {
    toggle: function() {
     this.play = !this.play;
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
  template: `<button type="button" class="btn btn-sm btn-light" :class="{active : isFullscreen}" @click=toggle><i class="fas fa-compress"></i></button>`,
  methods: {
    toggle: function() {
      if (this.isFullscreen) {
        this.exitFullscreen();
      } else {
        this.enterFullscreen();
      }
      this.isFullscreen = !this.isFullscreen;
    },

    // enter fullscreen based on browser
    enterFullscreen: function() {
      var mapContainer = voyagesMap._map.getContainer();
      if (mapContainer.requestFullscreen) {
        mapContainer.requestFullscreen();
      } else if (mapContainer.mozRequestFullScreen) {
        /* Firefox */
        mapContainer.mozRequestFullScreen();
      } else if (mapContainer.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        mapContainer.webkitRequestFullscreen();
      } else if (mapContainer.msRequestFullscreen) {
        /* IE/Edge */
        mapContainer.msRequestFullscreen();
      }
    },

    // exit fullscreen based on browser
    exitFullscreen: function() {
      var mapContainer = voyagesMap._map.getContainer();
      if (mapContainer.requestFullscreen) {
        document.exitFullscreen();
      } else if (mapContainer.mozRequestFullScreen) {
        /* Firefox */
        document.mozCancelFullScreen();
      } else if (mapContainer.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (mapContainer.msRequestFullscreen) {
        /* IE/Edge */
        document.msExitFullscreen();
      }
    }
  }
});