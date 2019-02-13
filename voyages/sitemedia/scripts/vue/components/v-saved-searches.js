template = `
    <div class="v-form-group">

    <div class="flex-between">
        <div class="v-title">
          <span>{{title}}<span> ({{saved.length}})</span></span>
        </div>
        <div>
          <b-button variant="outline-secondary" v-if="saved.length" size="sm" @click="clear">` +
            gettext('Clear') +
          `</b-button>
          <b-button variant="info" size="sm" @click="click">` +
            gettext('Save') +
          `</b-button>
        </div>
      </div>
      
      <div class="v-description">
        <div v-if="saved.length">` +
          gettext('Here are the queries saved during this session.') +
        `</div>
        <div v-else>` +
          gettext('No query saved during this session.</div>') +
        `</div>

      <div class="flex-between v-saved-searches-header" v-if="saved.length">
        <div class="v-title">` +
          gettext('URL') +
        `</div>
      </div>

      <div class="flex-between v-saved-searches-item" v-if="saved.length" v-for="search in saved">
        <div :id="search.saved_query_id">
          {{search.saved_query_url}}
        </div>
        <div>
          <b-button variant="outline-secondary" size="sm" @click="load(search.saved_query_id)">` +
            gettext('Load') +
          `</b-button>
          <b-button variant="info" size="sm"
            v-clipboard:copy="search.saved_query_url"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError">` +
            gettext('Copy') +
          `</b-button>
        </div>
      </div>

    </div>
  `;

Vue.component('v-saved-searches', {
  props: ['title', 'description', 'saved'],
  template: template,

  methods: {
    load(saved_query_id) {
      this.$emit('load', saved_query_id);
    },
    click() {
      this.$emit('save');
    },
    clear() {
      this.$emit('clear');
    },
    onCopy: function (e) {
      alert(gettext('Your URL ') + e.text + gettext(" is copied"));
    },
    onError: function (e) {
      alert(gettext('Failed to copy URL'));
    }
  },

  created: function(){
  }

});
