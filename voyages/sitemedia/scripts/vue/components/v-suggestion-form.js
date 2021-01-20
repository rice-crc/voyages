var template = `
    <div class="card suggestion-card" :class="index > 0 && 'mt-3'">
      <div class="card-body p-4">
        <div class="card-title">
          <span class="font-weight-bold text-secondary">${gettext('Suggestion')} {{ index+1 }}</span>
          <b-dropdown v-if="canRemove || canReset" right no-caret variant="transparent" class="float-sm-right">
            <template #button-content>
              <i class="fas fa-ellipsis-v" />
            </template>
            <b-dropdown-item v-if="canReset" @click="reset" class="border-radius-top" :class="!canRemove && 'border-radius-bottom'">
              <span>Reset</span>
            </b-dropdown-item>
            <b-dropdown-item v-if="canRemove" @click="remove" class="border-radius-bottom" :class="!canReset && 'border-radius-top'">
              <span>Remove</span>
            </b-dropdown-item>
          </b-dropdown>
        </div>
        <h6 class="card-subtitle mb-2 text-muted">${gettext('Suggest a modern version of the name.')}</h6>
        <p class="card-text">
            <div class="row">
                <div class="col-lg-6">
                    <div class="form-group">
                        <label for="spelling">${gettext('Spelling')} *</label>
                        <input type="text" class="form-control" id="spelling-1" v-model="value.name" />
                    </div>
                    <div class="form-group">
                        <label for="comments">${gettext('Comments')}</label>
                        <textarea class="form-control" id="spelling-comments-1" v-model="value.notes"></textarea>
                    </div>
                </div>
                <div class="col-lg-6">
                    <v-recording v-model="value.recording" :label="gettext('Recording')"></v-recording>
                </div>
            </div>
        </p>
      </div>
    </div>
  `;

// v-suggestion-form
Vue.component('v-suggestion-form', {
  props: {
    index: {
      type: String,
      default: "0",
    },
    canRemove: {
      type: Boolean,
      default: false,
    },
    value: {
      type: Object,
      default: () => ({
        name: '',
        notes: '',
        recording: '',
      })
    }
  },
  template: template,

  methods: {
    reset() {
      this.value.name = "";
      this.value.notes = "";
      this.value.recording = null;
    },
    remove() {
      this.$emit('remove', this.index);
    }
  },
  computed: {
    canReset() {
      return this.value.name != "";
    }
  }

})
// v-suggestion-form
