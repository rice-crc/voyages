var template = `
  <div class="form-group">
    <audio ref="player" :src="audioURL"></audio>
    <label for="recording">{{ label }}</label>

    <div v-if="!isRecording && !isRecorded" class="btn btn-light btn-lg btn-block recording-button" @click="start">
      <div class="container ml-0">
      <div class="align-items-center">
      <i class="fas fa-microphone-alt cursor-pointer fa-lg d-block"></i>
      <span class="description">${gettext('Click to record a pronunciation for this name')}</span>
      </div>
      </div>
    </div>

    <div v-if="isRecording" class="btn btn-light btn-lg btn-block stop-recording-button" @click="stop">
      <div class="container ml-0">
      <div class="align-items-center">
      <i class="fas fa-stop cursor-pointer fa-lg d-block"></i>
      <span class="description">${gettext('Click again to stop the recording')}</span>
      </div>
      </div>
    </div>

    <div v-show="isRecorded" class="review-recording bg-light rounded">
      <div class="col-lg-12 p-0">
        <div class="audio-controls">
          <button type="button" class='play-button btn btn-transparent mr-1 px-1' :class="icon" @click="play"></button>
          <span>{{ duration }}</span>
          <button type="button" class="delete-button btn btn-transparent fas fa-trash-alt mr-1 px-1 float-right" @click="deleteRecording"></button>
        </div>
      </div>
    </div>
  </div>
`;

// v-recording
Vue.component('v-recording', {
  props: {
    label: {
      type: String,
      default: "",
    },
    value: {
      type: Blob,
      default: null,
    },
  },
  template: template,

  data: function() {
    return {
      mediaRecorder: null,
      track: null,
      isRecording: false,
      isStoped: true,
      stream: null,
      icon: 'fas fa-play-circle',
      duration: "0"
    }
  },

  computed: {
    audioURL() {
      if (this.isRecorded) {
        return window.URL.createObjectURL(this.value);
      }
    },
    isRecorded() {
      if (this.value instanceof Blob) {
        return true;
      }
    },
  },

  methods: {
    secondsTimeSpanToMS(s) {
      s = parseInt(s, 10);
      var m = Math.floor(s/60); //Get remaining minutes
      s -= m*60;
      return (m < 10 ? '0'+m : m)+":"+(s < 10 ? '0'+s : s); //zero padding on minutes and seconds
    },
    start() {
      let chunks = [];

      navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then(stream => {
        this.stream = stream;
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.start();
        this.mediaRecorder.ondataavailable = (e) => {
          chunks.push(e.data);
        };
        this.mediaRecorder.onstop = (e) => {
          const blob = new Blob(chunks, { 'type' : chunks[0].type });
          this.$emit('input', blob);

          chunks = [];
        };
        this.isRecording = true;

      })
      .catch(err => alert('Cannot start mic'));
    },
    stop() {
      this.track = this.stream.getTracks()[0];
      this.track.stop();
      this.mediaRecorder.stop();
      this.isRecording = false;
    },
    play() {
        var audio = this.$refs.player;

        if (this.isStoped) {
            this.icon = 'fas fa-stop'
            this.isStoped = false;
            audio.play();
        } else {
            this.icon = 'fas fa-play-circle'
            this.isStoped = true;
            audio.pause();
            audio.currentTime = 0;
        }

        // Prevent Default Action
        return false;
    },
    deleteRecording() {
      this.isRecording = false;

      this.$emit('input', null);

      return false;
    }
  },

  watch: {
    value: {
      handler: function(){
        if (this.value == null) {
          this.deleteRecording();
        }
      },
      deep: true,
    },

  },

  mounted() {
    this.$refs.player.addEventListener("loadedmetadata", () => {
      if(this.$refs.player.duration === Infinity) {
        this.$refs.player.currentTime = 1e101;
        this.$refs.player.ontimeupdate = () => {
          this.$refs.player.ontimeupdate = () => {
            return;
          }
          this.duration = this.secondsTimeSpanToMS(this.$refs.player.duration);
          this.$refs.player.currentTime = 0.1;
          this.$refs.player.currentTime = 0;
        }
      } else {
        this.duration = this.secondsTimeSpanToMS(this.$refs.player.duration);
      }
    });

    this.$refs.player.addEventListener('ended', () => {
      this.isStoped = true;
      this.icon = 'fas fa-play-circle';
    });
  }
})
// v-recording
